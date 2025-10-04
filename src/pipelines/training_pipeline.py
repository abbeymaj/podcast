# Importing packages
import dagshub
import mlflow
from mlflow import MlflowClient
from src.components.train_model import TrainModel
from src.utils import save_run_params

# Initiating the training process and storing the trained model
if __name__ == '__main__':
    
    # Instantiating the dagshub client
    dagshub.init(repo_owner='abbeymaj', repo_name='podcast', mlflow=True)
    
    # Setting the URI for the dagshub mlflow repo
    model_uri = 'https://dagshub.com/abbeymaj/podcast.mlflow'
    mlflow.set_tracking_uri(model_uri)
    
    # Establishing the mlflow client
    client = MlflowClient()
    
    # Setting the experiment ID
    experiment_id = client.create_experiment('podcast_training_3')
    
    # Initiating the model training run
    run_params = {}
    with mlflow.start_run(run_name='training_pipeline_3', experiment_id=experiment_id) as run:
        # Initiating the model trainer
        trainer = TrainModel()
        # Obtaining the best model and the best params
        best_model, best_params = trainer.initiate_model_training()
        # Logging the best params
        mlflow.log_params(best_params)
        # Logging the best model
        model_info = mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path='models/training_model_3',
            registered_model_name='training_model_3'
        )
        
        # Fetch model metadata to store as run_params
        run_id = run.info.run_id
        latest_version_info = client.get_latest_versions(name='training_model_3', stages=['None'])[0]
        model_name = latest_version_info.name
        latest_version = latest_version_info.version
        model_uri = model_info.model_uri
        
        # Storing the model metadata in the run_params dictionary
        run_params['model_uri'] = model_uri
        run_params['model_name'] = model_name
        run_params['latest_version'] = latest_version
        run_params['run_id'] = run_id
    
    # Saving the run parameters
    save_run_params(run_params)