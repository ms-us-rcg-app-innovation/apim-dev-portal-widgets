# make api call with requests to rest endpoint with headers
import requests
import json
import json
import os
import requests
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
import shutil


# Retrieve the IDs and secret to use with ServicePrincipalCredentials
tenant_id = "<YOUR TENANT ID>"
client_id = "<YOUR CLIENT ID>"
client_secret = "<YOUR CLIENT SECRET>"

dev_url = "https://management.azure.com/subscriptions/<YOUR SUBSCRIPTION ID>/resourceGroups/<YOUR RESOURCE GROUP>/providers/Microsoft.ApiManagement/service/<YOUR APIM NAME>"
prod_url = "https://management.azure.com/subscriptions/<YOUR SUBSCRIPTION ID>/resourceGroups/<YOUR RESOURCE GROUP>/providers/Microsoft.ApiManagement/service/<YOUR APIM NAME>"


# Azure Identity and Subscription Details
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

# Function to get access token
def get_token():
    token = credential.get_token('https://management.azure.com/.default')
    return token.token

# Function to create headers for API requests
def create_headers():
    token = get_token()
    headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
    return headers

## Function to delete all files in a directory while preserving directory structure
# def delete_files_in_directory(directory_path):
#     for root, _, files in os.walk(directory_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)

def delete_directory_content(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # remove the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # remove dir and all contains

def remove_files_if_exists(*filenames):
    """Remove files if they exist."""
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)

def get_content_types(base_url, headers):
    response = requests.get(f"{base_url}/contentTypes?api-version=2022-09-01-preview", headers=headers)
    return response.json()['value']


def get_all_content_items(base_url, headers, content_types):
    content_item_ids = []
    for ct in content_types:
        ct_id = ct['id'].split('/')[-1]
        content_items_url = f"{base_url}/contentTypes/{ct_id}/contentItems?api-version=2022-08-01"
        response = requests.get(content_items_url, headers=headers)
        content_items = response.json()['value']
        content_item_ids.extend(content_items)
    return content_item_ids


def get_content_item_details(base_url, headers, content_item_ids):
    content_item_list = []
    for ci in content_item_ids:
        content_item_detail_url = f"{base_url}/{ci['id']}?api-version=2022-08-01"
        response = requests.get(content_item_detail_url, headers=headers)
        content_item_detail = response.json()
        content_item_list.append(content_item_detail)
    return content_item_list


# Function to export content from Azure DEV APIM
def export(base_url, headers):


    content_types = get_content_types(base_url, headers)
    content_item_ids = get_all_content_items(base_url, headers, content_types)
    content_item_list = get_content_item_details(base_url, headers, content_item_ids)

    remove_files_if_exists('content_types.json', 'content_item_list.json')

    with open('content_types.json', 'w') as f:
        json.dump(content_types, f)
        
    with open('content_item_list.json', 'w') as f:
        json.dump(content_item_list, f)

    media_dir = "media/"
    delete_directory_content(media_dir)
    # Function to download media from Azure DEV APIM
    download_media(base_url, headers, media_dir)


def download_media(base_url, headers, media_dir):
    sas = requests.post(f"{base_url}/portalSettings/mediaContent/listSecrets?api-version=2021-08-01", headers=headers).json()['containerSasUrl']
    container_client = ContainerClient.from_container_url(sas)
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)
        download_path = os.path.join(media_dir, blob.name)
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open(download_path, "wb") as file:
            blob_client.download_blob().readinto(file)

def delete_all_content_items(base_url, headers, content_item_ids):
    for ci in content_item_ids:
        content_item_delete_url = f"{base_url}/{ci['id']}?api-version=2022-08-01"
        response = requests.delete(content_item_delete_url, headers=headers)
        # Consider adding error handling here, depending on the response status

# Function to import content to Azure PROD APIM
def import_function(base_url, headers):

    # Baclup old prod content
    content_types = get_content_types(base_url, headers)
    content_item_ids = get_all_content_items(base_url, headers, content_types)
    content_item_list = get_content_item_details(base_url, headers, content_item_ids)

    remove_files_if_exists('oldProd/content_types.json', 'oldProd/content_item_list.json')

    with open('oldProd/old_prod_content_types.json', 'w') as f:
        json.dump(content_types, f)
        
    with open('oldProd/old_prod_content_item_list.json', 'w') as f:
        json.dump(content_item_list, f)

    media_dir = "oldProd/media/"
    delete_directory_content(media_dir)
    download_media(base_url, headers, media_dir)

    # Delete all content from prod
    delete_all_content_items(base_url, headers, content_item_ids)

    # Import new content to prod
    with open('content_types.json') as f:
        content_types = json.load(f)

    with open('content_item_list.json') as f:
        content_item_list = json.load(f)

    for ct in content_types:
        requests.put(f"{base_url}{ct['id']}?api-version=2022-09-01-preview", headers=headers, json=ct)
    for ci in content_item_list:
        requests.put(f"{base_url}{ci['id']}?api-version=2022-08-01", headers=headers, json=ci)
    upload_media(base_url, headers)

# Function to upload media to Azure PROD APIM
def upload_media(base_url, headers):
    sas = requests.post(f"{base_url}/portalSettings/mediaContent/listSecrets?api-version=2021-08-01", headers=headers).json()['containerSasUrl']
    container_client = ContainerClient.from_container_url(sas)

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)
        if blob_client.exists():
            blob_client.delete_blob()

    media_directory = "media/"
    for root, _, files in os.walk(media_directory):
        for filename in files:
            blob_name = os.path.join(os.path.relpath(root, media_directory), filename)
            blob_client = container_client.get_blob_client(blob_name)
            if blob_client.exists():
                blob_client.delete_blob()
            with open(os.path.join(root, filename), "rb") as data:
                blob_client.upload_blob(data)

# Auth Header for API calls
headers = create_headers()

# Export content from DEV (Source)
export(dev_url, headers)

# Import content into PROD (Destination)
import_function(prod_url, headers)
