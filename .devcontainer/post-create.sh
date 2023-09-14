# Install dependencies
poetry install --with dev,cloudfunctions,model_train

# Activate environment
sh ./.venv/bin/activate

# Install pre-commit hooks
pre-commit install

