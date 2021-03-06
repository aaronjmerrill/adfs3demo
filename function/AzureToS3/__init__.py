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
    
    data = file_client.download_file().content_as_bytes()
    logging.info('read file')

    s3 = boto3.resource(
        endpoint_url='https://s3.us-west-002.backblazeb2.com',
        service_name='s3',
        aws_access_key_id='002fdf2ee4eb9b00000000004',
        aws_secret_access_key='K002eu2wpB+ig0bBhmpO8D2Wc74U5tY'
    )
    logging.info('created S3 resource')

    try:
        s3.Object('adfs3demoinput', 'goesToS3.json').put(Body=data)
        logging.info('uploaded file to S3')
    except Exception as e: 
        logging.info(e)
        return func.HttpResponse(
            e,
            status_code=500
        )

    return func.HttpResponse(
        "Successfully wrote to S3 bucket.",
        status_code=200
    )
