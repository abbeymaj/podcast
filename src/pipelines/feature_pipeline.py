# Importing packages
from src.components.data_ingestion import DataIngestion
from src.components.transform_data import TransformData
from src.components.create_feature_store import CreateFeatureStore

# Transforming the raw data and creating the feature store
if __name__ == '__main__':
    
    # Ingesting the data and creating the artifacts folder
    ingest_data = DataIngestion()
    train_path, test_path = ingest_data.initiate_data_ingestion()
    
    # Transforming the data and creating the preprocessor objec
    transform_data = TransformData()
    train_data, test_data, _ = transform_data.initiate_data_transformation(train_path, test_path)
    
    # Creating the feature store
    create_feature_store = CreateFeatureStore()
    create_feature_store.create_and_store_features(train_data, test_data)