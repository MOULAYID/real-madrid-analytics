/* Compatibility adapter for the retained React build.
 * Its original source is absent from this repository. Only its legacy analytics
 * requests are served from data exported by scripts/build_static_dashboard.py.
 * Unrelated fetch calls and popups retain their normal browser behaviour.
 */
(() => {
  "use strict";
  const nativeFetch = window.fetch.bind(window);
  const nativeOpen = window.open.bind(window);
  const dataURL = new URL("./data/analytics.json", document.baseURI);
  let snapshotPromise;
  function reportError() {
    if (document.getElementById("dashboard-data-error")) return;
    const alert = document.createElement("p");
    alert.id = "dashboard-data-error";
    alert.setAttribute("role", "alert");
    alert.textContent = "Dashboard data could not be loaded. Please refresh the page or try again later.";
    Object.assign(alert.style, { padding: "1rem", margin: "1rem", border: "1px solid #ef4444", borderRadius: "8px", color: "#fca5a5", background: "#111827" });
    document.body.prepend(alert);
  }
  function snapshot() {
    if (!snapshotPromise) snapshotPromise = nativeFetch(dataURL).then(response => {
      if (!response.ok) throw new Error("Dashboard dataset unavailable");
      return response.json();
    }).catch(error => {
      snapshotPromise = undefined;
      reportError();
      throw error;
    });
    return snapshotPromise;
  }
  function legacyURL(input) {
    const raw = input instanceof Request ? input.url : String(input);
    const url = new URL(raw, document.baseURI);
    return (url.hostname === "localhost" || url.hostname === "127.0.0.1")
      && url.port === "8000" && url.pathname.startsWith("/api/") ? url : null;
  }
  window.fetch = async function(input, init) {
    const url = legacyURL(input);
    if (!url) return nativeFetch(input, init);
    const method = (init?.method || (input instanceof Request ? input.method : "GET")).toUpperCase();
    if (method !== "GET") return new Response("Read-only portfolio dataset", { status: 405 });
    const data = await snapshot();
    const endpoint = url.pathname.slice("/api/".length);
    const season = url.searchParams.get("season");
    const payload = endpoint === "overview" && season
      ? data.overviewBySeason[season]
      : data.endpoints[endpoint];
    if (payload === undefined) return new Response(JSON.stringify({ detail: "Dataset not found" }), { status: 404, headers: { "Content-Type": "application/json" } });
    return new Response(JSON.stringify(payload), { status: 200, headers: { "Content-Type": "application/json" } });
  };
  window.open = function(url, ...args) {
    const legacy = url == null ? null : legacyURL(url);
    if (legacy?.pathname === "/api/export/financials" && legacy.searchParams.get("format") === "csv") {
      const link = document.createElement("a");
      link.href = new URL("./data/exports/financials.csv", document.baseURI).href;
      link.download = "financials.csv";
      document.body.append(link);
      link.click();
      link.remove();
      return null;
    }
    return nativeOpen(url, ...args);
  };
})();
