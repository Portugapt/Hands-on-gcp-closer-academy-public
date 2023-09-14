# Install dependencies
poetry install --with dev,cloudfunctions,model_train

# Activate environment
sh ./.venv/bin/activate

# Install pre-commit hooks
pre-commit install

# Login into GCP
gcloud auth login
gcloud config set project closeracademy-handson
