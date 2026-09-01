from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = (BASE_DIR / "data").resolve()
MODEL_DIR = (BASE_DIR / "models").resolve()

DATASET_PATH = (DATA_DIR / "laptops_backend_ready.csv").resolve()
FRONTEND_OPTIONS_PATH = (DATA_DIR / "frontend_options.json").resolve()
MODEL_PATH = (MODEL_DIR / "naive_bayes_laptop_pipeline.joblib").resolve()
MODEL_METADATA_PATH = (MODEL_DIR / "model_metadata.json").resolve()

# Backward-compatible aliases for modules created during the initial scaffold.
BACKEND_DIR = BASE_DIR
MODELS_DIR = MODEL_DIR
LAPTOPS_DATASET_PATH = DATASET_PATH
NAIVE_BAYES_MODEL_PATH = MODEL_PATH

ARTIFACT_PATHS = {
    "dataset": DATASET_PATH,
    "frontend_options": FRONTEND_OPTIONS_PATH,
    "model": MODEL_PATH,
    "model_metadata": MODEL_METADATA_PATH,
}
