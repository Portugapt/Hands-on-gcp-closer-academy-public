simple-mlops-requirements:
	poetry export -f requirements.txt --output functions/simple_mlops/a_ingest_data/app/requirements.txt --without-hashes --with cloudfunctions
	poetry export -f requirements.txt --output functions/simple_mlops/b_update_facts/app/requirements.txt --without-hashes --with cloudfunctions
	poetry export -f requirements.txt --output functions/simple_mlops/c_train_model/app/requirements.txt --without-hashes --with cloudfunctions,model_train
	poetry export -f requirements.txt --output functions/simple_mlops/d_predictions_endpoint/app/requirements.txt --without-hashes --with model_train
