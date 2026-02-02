# MLflow Object Storage Test on Chameleon Cloud

This repository contains the configuration and scripts used to test MLflow's ability to save large model checkpoints directly to Chameleon S3 storage (Swift/OpenStack), bypassing the need for a local MinIO container.

The goal was to verify if large models (up to 5.4GB) can be logged without encountering the checksum or timeout issues often reported when using S3-compatible backends on Chameleon.

## Repository Structure

- `docker-compose.yml`: Current recommended setup using MLflow 3.9.0 and PostgreSQL 18.
- `docker-compose-legacy.yml`: Setup using Professor's version (MLflow 2.20.2 and PostgreSQL 16).
- `test_opt_1.3b.py`: Script to test logging facebook/opt-1.3b (~2.6GB).
- `test_opt_2.7b.py`: Script to test logging facebook/opt-2.7b (~5.4GB).

## Results

I performed tests on a Chameleon VM and confirmed that both the 1.3B and 2.7B models upload successfully using the standard configurations provided here.

| Model | Parameters | Size | Upload Time | Result |
| :--- | :--- | :--- | :--- | :--- |
| facebook/opt-1.3b | 1.3B | 2.6 GB | ~65s | Success |
| facebook/opt-2.7b | 2.7B | 5.4 GB | ~140s | Success |

## Technical Notes

### Version Compatibility

The modern MLflow client (v3.x) is not backward compatible with the older MLflow server (v2.20.2) for some logging endpoints. If you use the legacy docker-compose setup, make sure to downgrade your local python environment to match:
`pip install mlflow==2.20.2`

### Checksum Issues

I investigated the known boto3 checksum calculation issue related to OpenStack Swift (detailed in [chameo issue #7](https://github.com/A7med7x7/chameo/issues/7)). In my testing on the Chameleon VM environment, the standard multipart upload worked without needing the `AWS_REQUEST_CHECKSUM_CALCULATION` environment variable. Both versions (2.20 and 3.9) persisted artifacts to the bucket correctly out of the box.

## How to use

1. Update the environment variables in the docker-compose file with your Chameleon S3 credentials.
2. Start the services: `docker-compose up -d`
3. Run the test script: `python3 test_opt_1.3b.py`
