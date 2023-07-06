import os
import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd

# setup azure blob connection
AZURE_STORAGE_CONNECTION_STRING = "your azure storage connection string"
container_name = "your container name"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(container_name)

# website to scrape
url = 'https://data.sba.gov/dataset/ppp-foia'

# send a HTTP request to the URL and save 
# the response from server in a response object called r
r = requests.get(url)

# create a BeautifulSoup object
soup = BeautifulSoup(r.text, 'html.parser') 

# Find all the links on the webpage
links = soup.find_all('a')

# Filter the link sending with .csv
csv_links = [link.get('href') for link in links if link.get('href').endswith('.csv')]

# download each csv and upload to azure blob storage
for csv_link in csv_links:
    # Load the CSV data directly into pandas dataframe
    df = pd.read_csv(csv_link)

    # Save the dataframe as CSV to a string
    csv_data = df.to_csv(index=False)

    # Generate blob name from the link
    blob_name = os.path.basename(csv_link)
    
    # Get blob client
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    
    # Upload the data to Azure Blob Storage
    blob_client.upload_blob(csv_data)
