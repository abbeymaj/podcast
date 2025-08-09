# Importing packages
from src.components.data_ingestion import DataIngestion

# Transforming the raw data and creating the feature store
if __name__ == '__main__':
    
    # Ingesting the data and creating the artifacts folder
    ingest_data = DataIngestion()
    train_path, test_path = ingest_data.initiate_data_ingestion()