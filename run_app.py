"""
Master Application Launcher for Real Madrid Financial Intelligence Platform.
Runs Data Pipeline, FastAPI Backend, and Streamlit Dashboard.
"""
import sys
import subprocess
import argparse
import time

def run_pipeline():
    """Runs data ingestion and ML forecasting scripts."""
    print("🚀 [1/2] Running Data Ingestion Pipeline...")
    res1 = subprocess.run([sys.executable, "data_pipeline/ingest_data.py"])
    if res1.returncode != 0:
        print("❌ Data ingestion failed.")
        return False

    print("🧠 [2/2] Running ML Forecasting Pipeline...")
    res2 = subprocess.run([sys.executable, "data_pipeline/forecasting.py"])
    if res2.returncode != 0:
        print("❌ ML forecasting failed.")
        return False

    print("✅ Pipeline execution completed successfully!")
    return True

def run_backend():
    """Launches FastAPI backend server."""
    print("🌐 Starting FastAPI REST API backend on http://127.0.0.1:8000 ...")
    subprocess.run([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])

def run_dashboard():
    """Launches Streamlit dashboard UI."""
    print("👑 Starting Streamlit Executive Dashboard on http://localhost:8501 ...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"])

def run_all():
    """Runs data pipeline and starts backend + dashboard concurrently."""
    run_pipeline()
    print("⚡ Launching Backend API & Streamlit Dashboard...")
    backend_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(2)
    dashboard_proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"])
    
    try:
        backend_proc.wait()
        dashboard_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_proc.terminate()
        dashboard_proc.terminate()

def main():
    parser = argparse.ArgumentParser(description="Real Madrid Financial Analytics Platform Control CLI")
    parser.add_argument("--pipeline", action="store_true", help="Run data ETL and ML forecasting pipelines")
    parser.add_argument("--backend", action="store_true", help="Start FastAPI REST API server")
    parser.add_argument("--dashboard", action="store_true", help="Start Streamlit Executive Dashboard")
    args = parser.parse_args()

    if args.pipeline:
        run_pipeline()
    elif args.backend:
        run_backend()
    elif args.dashboard:
        run_dashboard()
    else:
        run_all()

if __name__ == "__main__":
    main()
