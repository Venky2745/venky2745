import boto3
import urllib.parse


def lambda_handler(event, context):
    srcBucketName = urllib.parse.unquote(event['Records'][0]['s3']['bucket']['name'])
    srcBucketObjKey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    destinationBucket = 'mybucket4pyprgm-destiny'
    copy_source = {'Bucket': srcBucketName, 'Key': srcBucketObjKey}
    try:
        s3 = boto3.client('s3')
        s3.copy_object(Bucket=destinationBucket, Key=srcBucketObjKey, CopySource=copy_source)
        print(f"succesfully uploaded file to {destinationBucket} bucket")
    except Exception as err:
        print("Error -" + str(err))


"""
What characters are allowed in a bucket or object name?
	- A key is a sequence of Unicode characters whose UTF-8 encoding is at most 1024 bytes long.
	- Bucket names can consist only of lowercase letters, numbers, dots (.), and hyphens (-).
		Bucket names must begin and end with a letter or number.


dummy input data&%#!%   =>   dummy+input+data%26%25%23%21%25.txt

URL encoding converts non-ASCII characters into a format that can be transmitted over the Internet. 
URL encoding replaces non-ASCII characters with a "%" followed by hexadecimal digits. 
URLs cannot contain spaces. URL encoding normally replaces a space with a plus (+) sign, or %20.

HTML Encoding escapes special characters in strings used in HTML documents 
whereas URL Encoding replaces special characters with characters so that they can sent within url.
"""

"""
s3.copy_object: paramters
	1. Bucket (string) -- [REQUIRED] The name of the destination bucket.
	2. Key (string) -- [REQUIRED] The key of the destination object.
	3. CopySource (str or dict) -- [REQUIRED] The name of the source bucket, key name of the source object, and optional version ID of the source object. You can either provide this value as a string or a dictionary. The string form is {bucket}/{key} or {bucket}/{key}?versionId={versionId} if you want to copy a specific version. 
	You can also provide this value as a dictionary. The dictionary format is recommended over the string format because it is more explicit. The dictionary format is: {'Bucket': 'bucket', 'Key': 'key', 'VersionId': 'id'}. 
	Note that the VersionId key is optional and may be omitted. To specify an S3 access point, provide the access point ARN for the Bucket key in the copy source dictionary. If you want to provide the copy source for an S3 access point as a string instead of a dictionary, the ARN provided must be the full S3 access point object ARN (i.e. {accesspoint_arn}/object/{key})
"""
"""
import json

# convert to string
input = json.dumps({'id': id })

# load to dict
my_dict = json.loads(input) 
"""
"""
urllib.parse.unquote(string, encoding='utf-8', errors='replace')
	Replace %xx escapes with their single-character equivalent. 
	The optional `encoding` and `errors` parameters specify how to decode percent-encoded sequences into Unicode characters, 
		as accepted by the bytes.decode() method.
	string may be either a str or a bytes object.
	encoding defaults to 'utf-8'. errors defaults to 'replace', meaning invalid sequences are replaced by a placeholder character.
		Example: unquote('/El%20Ni%C3%B1o/') yields '/El Niño/'.
	Changed in version 3.9: string parameter supports bytes and str objects (previously only str).
	=> https://docs.microfocus.com/OMi/10.62/Content/OMi/ExtGuide/ExtApps/URL_encoding.htm
	=> https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
urllib.parse.unquote_plus(string, encoding='utf-8', errors='replace')
	Like unquote(), but also replace plus signs with spaces, as required for unquoting HTML form values.
	string must be a str.
	Example: unquote_plus('/El+Ni%C3%B1o/') yields '/El Niño/'.
"""