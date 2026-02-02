import mlflow
import mlflow.pytorch
import torch
from transformers import AutoModel
import time

# Configuration
TRACKING_URI = "http://localhost:5010"
EXPERIMENT_NAME = "chameleon-s3-test-vm"
MODEL_NAME = "facebook/opt-1.3b"

print(f"Connecting to MLflow at {TRACKING_URI}...")
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

print(f"Downloading model {MODEL_NAME}...")
try:
    # Load model
    model = AutoModel.from_pretrained(MODEL_NAME)
    print("Model loaded successfully.")

    with mlflow.start_run(run_name="large_model_NO_FIXES") as run:
        print(f"Logging model to MLflow (uploads to Chameleon S3)... Run ID: {run.info.run_id}")
        start_time = time.time()
        
        # Log model
        mlflow.pytorch.log_model(model, "model")
        
        duration = time.time() - start_time
        print(f"✅ Success! Upload took {duration:.2f} seconds.")
        
except Exception as e:
    print(f"❌ Large Model Test FAILED: {str(e)}")
    exit(1)
