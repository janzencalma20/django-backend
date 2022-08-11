from celery.utils.log import get_task_logger
from time import sleep
from celery import shared_task
import json
import boto3
import os

logger = get_task_logger(__name__)


@shared_task(name='lptn_solve_task')
def lptn_solve_task():
    sleep(10)
    with open('component_results.json') as file:
        data = json.load(file)
        return data


@shared_task(name='lptn_results_task')
def lptn_results_task(machine_id):
    s3 = boto3.resource('s3')
    bucket = os.environ["BUCKET_NAME"]
    s3_bucket = s3.Bucket(bucket)
    plots = s3_bucket.objects.filter(Prefix='Images/Results')
    for obj in plots:
        img_name = "/".join(obj.key.split('/')[-2:])
        source = {
            "Bucket": bucket,
            "Key": obj.key
        }
        s3.meta.client.copy(source, bucket, f"{machine_id}/Results/LPTN/{img_name}")

    results = {
        "img_generated": True,
        "img_uploaded": True,
        "error": None
    }
    return results
