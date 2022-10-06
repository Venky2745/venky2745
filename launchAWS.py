import boto3
import boto3.ec2
import json
import sys
import boto3.utils
import botocore.exceptions
ec2= boto3.client("ec2","ap-south-1",aws_access_key_id='AKIA4VYYHEBZKSTHCONI', aws_secret_access_key= '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')
output=ec2.describe_instances()
print(output)
'''createInstance=ec2.run_instances(InstanceType="t2.small",MaxCount=1,MinCount=1,ImageId='ami-01216e7612243e0ef')
print(createInstance)
stopInst=ec2.stop_instances(InstanceIds=list('4dc96ad53ebe90de''f13c0f565d132a6b''78759a62a62690e8'))
 try:
except Exception er1:
 error= "error: %s" % str(er1)
 print (error)
 sys.exit(0)'''
print(stopInst)


''' def lambda_handler(event, context):
    instances = event["instances"].split(',')
    action = event["action"]

    if action == 'Running':
        print("Runnung  your instances: " + str(instances))
        ec2.running_instances(InstanceIds=instances)
        response = "Successfully  instances are running: " + str(instances)
    elif action == 'Stop':
        print("STOPping your instances: " + str(instances))
        ec2.stop_instances(InstanceIds=instances)
        response = "Successfully stopped instances: " + str(instances)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
'''