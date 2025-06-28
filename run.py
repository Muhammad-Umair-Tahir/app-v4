import subprocess
import time

# Start backend
backend = subprocess.Popen(["uvicorn", "main:app", "--reload"])
time.sleep(5)  # Wait for backend to start

# Start Streamlit
streamlit = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for both to finish (Ctrl+C to stop)
backend.wait()
streamlit.wait()