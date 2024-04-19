from google.cloud import storage
from uuid import uuid4
## TODO: Need to set the credentials in k8s deployment
async def save_file_to_gcs(file) -> str:
    """
    Uploads a file to Google Cloud Storage and returns the file URL.
    """
    client = storage.Client()
    bucket_name = 'image_bucket_map'
    bucket = client.bucket(bucket_name)
    blob_name = f"{uuid4()}-{file.filename}"
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        await file.read(),
        content_type=file.content_type
    )

    return blob.public_url
