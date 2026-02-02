import mlflow
import mlflow.pytorch
import torch
from transformers import AutoModel
import time
import os

# Configuration
TRACKING_URI = "http://localhost:5010"
EXPERIMENT_NAME = "chameleon-s3-test-vm"
MODEL_NAME = "facebook/opt-2.7b"  # ~5.4GB Model

print(f"Connecting to MLflow at {TRACKING_URI}...")
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

print(f"Downloading model {MODEL_NAME} (approx 5GB)...")
try:
    # Load model
    start_load = time.time()
    model = AutoModel.from_pretrained(MODEL_NAME)
    load_time = time.time() - start_load
    print(f"Model loaded successfully in {load_time:.2f}s.")

    with mlflow.start_run(run_name="xl_model_opt_2.7b") as run:
        print(f"Logging XL model to MLflow (S3)... Run ID: {run.info.run_id}")
        start_time = time.time()
        
        # Log model
        mlflow.pytorch.log_model(model, "model")
        
        duration = time.time() - start_time
        print(f"✅ Success! XL Model Upload took {duration:.2f} seconds.")
        
except Exception as e:
    print(f"❌ XL Model Test FAILED: {str(e)}")
    # Print memory stats on failure
    os.system("free -h")
    exit(1)
