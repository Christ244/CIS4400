import os
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

# setup azure blob connection
AZURE_STORAGE_CONNECTION_STRING = "your azure storage connection string"
container_name = "your container name"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(container_name)

# Get the list of all blobs in the container
blob_list = container_client.list_blobs()

# Initialize a list to hold dataframes
df_list = []

# Loop over blobs and download as dataframe
for blob in blob_list:
    # Only process .csv files
    if blob.name.endswith('.csv'):
        # Download blob to a string
        blob_data = blob_service_client.get_blob_client(container_name, blob.name).download_blob().readall()

        # Convert the string data to BytesIO and read as dataframe
        df = pd.read_csv(BytesIO(blob_data))

        # Append the dataframe to the list
        df_list.append(df)

# Concatenate all dataframes in the list
merged_df = pd.concat(df_list)

# Convert the dataframe to a CSV string
merged_csv = merged_df.to_csv(index=False)

# Prepare the new blob name
new_blob_name = 'processed/merged.csv'

# Get blob client
blob_client = blob_service_client.get_blob_client(container_name, new_blob_name)

# Upload the data to Azure Blob Storage
blob_client.upload_blob(merged_csv)
