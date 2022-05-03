import logging

import azure.functions as func
from azure.storage.fileshare import ShareFileClient

import boto3

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Entered function')

    file_client = ShareFileClient.from_connection_string(
        conn_str='DefaultEndpointsProtocol=https;AccountName=saajmdemoadfs3;AccountKey=sTkr8MR+vXfcFsArmUWYIbnkZ1S/VQNSyCn/gJct+pvNbzAmF9NjUD7VAIEu16rlb1SVT07ahzja+AStgL1KoQ==;EndpointSuffix=core.windows.net',
        share_name='output',
        file_path='goesToS3.json'
    )
    logging.info('created az file client')

    # with open("goesToS3.json", "wb") as file_handle:
    #     data = file_client.download_file()
    #     data.readinto(file_handle)
    data = file_client.download_file()
    logging.info('read file')

    s3 = boto3.resource(
        endpointUrl='https://s3.us-west-002.backblazeb2.com',
        service_name='s3',
        aws_access_key_id='002fdf2ee4eb9b00000000004',
        aws_secret_access_key='K002eu2wpB+ig0bBhmpO8D2Wc74U5tY'
    )
    logging.info('created S3 resource')

    s3.Object('adfs3demoinput').Put(Body=data)
    logging.info('uploaded file to S3')

    return func.HttpResponse(
        "Successfully wrote to S3 bucket.",
        status_code=200
    )
