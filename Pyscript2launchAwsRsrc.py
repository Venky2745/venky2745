import boto3
import logging
from botocore.exceptions import ClientError
import boto3.session

s3 = boto3.resource('s3')


def create_bucket(bucket_name, region="Asia Pacific (Mumbai) ap-south-1"):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)

        return False

    return True


create_bucket('bucketbypycode', 'ap-south-1')

my_session = boto3.session.Session(aws_access_key_id="AKIA4VYYHEBZKSTHCONI",
                                   aws_secret_access_key="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")
session = my_session.resource('s3')

s3.Object('bucketbypycode', 'Prgm2CopyFiles.zip').upload_file(
    r"C:\Users\venkateshbabu.g\Desktop\Work progress-tasks\Task1\Prgm2CopyFiles.zip")
with open(r"C:\Users\venkateshbabu.g\Desktop\Work progress-tasks\Task1\Prgm2CopyFiles.zip", "r") as f:
    print(f.read())

cloudformation = boto3.resource('cloudformation')
stack = cloudformation.create_stack(
    StackName='stackbycode',
    TemplateURL='s3://bucketbypycode/Prgm2CopyFiles.zip',

)

''' def check_existing_buckets():
    s3_resource = boto3.resource('s3')
    print("Hello, listing your existing buckets:")
    # print(sys.version)
    for bucket in s3_resource.buckets.all():
        print(f"{bucket.name}")


if __name__ == '__main__':
    check_existing_buckets()'''
