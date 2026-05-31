import os
from azure.identity import DefaultAzureCredential
from azure.ai.translation.document import DocumentTranslationClient
from azure.storage.blob import BlobServiceClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

credential = DefaultAzureCredential()

account_url = "https://doctranslate1409.blob.core.windows.net"
cognitive_endpoint = "https://speech-ep-resource.cognitiveservices.azure.com/"

blob_service_client = BlobServiceClient(account_url, credential=credential)
client = DocumentTranslationClient(cognitive_endpoint, credential=credential)

input_blob_container_name = "doc-translate"
input_blob_container_client = blob_service_client.get_container_client(
    container=input_blob_container_name
)

output_blob_container_name = "doc-translate-output"
output_blob_container_client = blob_service_client.get_container_client(
    container=output_blob_container_name
)

input_folder = os.path.join(os.path.dirname(__file__), "input")
output_folder = os.path.join(os.path.dirname(__file__), "output")


def list_blobs_flat(blob_container_client: ContainerClient):
    blob_list = list(blob_container_client.list_blobs())
    for blob in blob_list:
        print(f"Blob name: {blob.name}")

    return blob_list


def upload_blob_file(blob_container_client: ContainerClient, file_path: str):
    blob_name = os.path.basename(file_path)

    with open(file=file_path, mode="rb") as data:
        blob_container_client.upload_blob(name=blob_name, data=data, overwrite=True)


def download_blob_to_file(blob_container_client: ContainerClient, blob_name: str):
    blob_client = blob_container_client.get_blob_client(blob=blob_name)
    output_path = os.path.join(output_folder, blob_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(file=output_path, mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())


def delete_blob_snapshots(blob_container_client: ContainerClient, blob_name: str):
    blob_client = blob_container_client.get_blob_client(blob=blob_name)
    blob_client.delete_blob(delete_snapshots="include")


def clear_container(blob_container_client: ContainerClient):
    for blob in blob_container_client.list_blobs():
        delete_blob_snapshots(blob_container_client, blob.name)


# push files to input container
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    if os.path.isfile(file_path):
        upload_blob_file(input_blob_container_client, file_path)

# list files from input
input_blob_list = list_blobs_flat(input_blob_container_client)

# run translation using azure blob storage container
source_url = os.environ["SOURCE_URL"]
target_url = os.environ["TARGET_URL"]
target_language = "en"

poller = client.begin_translation(source_url, target_url, target_language)
result = poller.result()

# download to output
output_blob_list = list_blobs_flat(output_blob_container_client)
for blob in output_blob_list:
    download_blob_to_file(output_blob_container_client, blob.name)

# clear input and output
clear_container(input_blob_container_client)
clear_container(output_blob_container_client)

print("Done!")
