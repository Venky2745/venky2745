import logging

import boto3
from Access_Keys.keys import AWS_ACCESS_ID, AWS_ACCESS_KEY, AWS_REGION

from botocore.exceptions import ClientError




class Launchaws:
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_ID, aws_secret_access_key=AWS_ACCESS_KEY,
                            region_name=AWS_REGION)


def create_bucket(bucket_name, region=None):  # Creating Bucket
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


create_bucket("demobucket-demo1", 'ap-south-1')  # calling the function


def check_existing_buckets():  # to list the buckets
    s3_resource = boto3.resource('s3')
    print("Hello, listing your existing buckets:")
    # print(sys.version)
    for bucket in s3_resource.buckets.all():
        print(f"{bucket.name}")


if __name__ == '__main__':
    check_existing_buckets()


def list_stacks():
    cfn = boto3.resource('cloudformation', region_name='ap-south-1')
    Stack_status = ['ROLLBACK_COMPLETE', 'CREATE_COMPLETE', 'UPDATE_COMPLETE']
    for stack in cfn.stacks.all():
        StackStatus = stack.stack_status
        Createdtime = stack.creation_time
        StackName = stack.stack_name
        print(" The below is the lit of existing stacks :")
        print(StackName, " ", Createdtime, " ", StackStatus)


if __name__ == '__main__':
    list_stacks()


def Create_stack(TemplateURL, Capabilities, StackName=None):
    try:
        if StackName is None:
            client = boto3.client('cloudformation', region_name='ap-south-1')
            client.create_stack(StackName=StackName)
        else:
            client = boto3.client('cloudformation', region_name='ap-south-1')
            client.create_stack(StackName=StackName,
                                TemplateURL=TemplateURL,
                                Capabilities=Capabilities)
    except Exception as err:
        raise ClientError("An existing stack is found with stack name you've given , provide unique name for stack", +str(err))


Create_stack("newstackbygvb2",'https://gvbbucket1.s3.ap-south-1.amazonaws.com/demoCLDFORMtemplate1.yml','CAPABILITY_NAMED_IAM')
