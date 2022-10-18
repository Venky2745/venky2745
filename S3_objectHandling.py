import boto3
from botocore.exceptions import ClientError
from Access_Keys.keys import AWS_ACCESS_ID, AWS_ACCESS_KEY, AWS_REGION


class CustomError(Exception):
    def __init__(self, define_err):
        self.define_err = define_err

    def __str__(self):
        return self.define_err


class Utils:
    @staticmethod
    def compareMetadata(dict1, dict2):
        for key, val in dict1.items():
            if key not in dict2 or dict2[key] != val:
                return False
            return True

    @staticmethod
    def compareTags(list1, list2):
        for dict1 in list1:
            if dict1 not in list2:
                return False
            return True

    @staticmethod
    def convertDicttostring(tags):
        return "&".join([k + "=" + v for k, v in tags.items()])

    @staticmethod
    def dictInput(itemsCount):
        dict1 = dict()
        for i in range(itemsCount):
            key_val = input("give keys in this format => key: value").split(":")
            dict1[key_val[0]] = key_val[1]
        return dict1

    @staticmethod
    def convertDicttosetofTags(dict1):
        list1 = []
        for key, val in dict1.items():
            dict2 = dict()
            dict2['key'] = key
            dict2['value'] = val
            list1.append(dict2)
        return list1


class S3objects:
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_ID, aws_secret_access_key=AWS_ACCESS_KEY,
                            region_name=AWS_REGION)
    s3 = session.resource("s3")
    s3Client = session.client("s3")

    def __init__(self, bucketName):
        try:
            self.bucket = S3objects.s3.Bucket(bucketName)
            if bucketName not in [bucket.name for bucket in
                                  S3objects.s3.buckets.all()]:  # checking if bucket already exists
                self.bucket.create(CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        except Exception as e:
            raise ClientError("Error in s3bucket.__init__(): " + str(e))

    def listexistingObjects(self):
        no_of_objs = 0
        try:
            print("object_key \t Metadata \t Tags")
            for objectSummary in self.bucket.objects.all():
                object = self.bucket.Object(objectSummary.key)
                objTags = S3objects.s3Client.get_object_tagging(Bucket=self.bucket.name, Key=object.key)['Tagset']
                print(object.key, '\t', object.metadata, '\t', objTags)
                no_of_objs += 1
                print('total objects present : ', no_of_objs)
        except Exception as err:
            raise CustomError("Error In S3objects.__init__(): " + str(err))

    def Delete_objects_basedOnMetadataTags(self, filterMetadata, filterTags):
        objectstoDel = []
        try:
            for objectSummary in self.bucket.objects.all():
                object = self.bucket.Object(objectSummary.key)
                objTags = S3objects.s3Client.get_object_tagging(Bucket=self.bucket.name, key=object.key)['TagSet']
                if Utils.compareMetadata(filterMetadata, object.metadata) and Utils.compareTags(filterTags, objTags):
                    objectstoDel.append({'Key': object.key, 'VersionId': 'null'})
            response = None
            if objectstoDel:
                response = self.bucket.delete_objects(Delete={'Objects': objectstoDel, 'Quiet': True})
            print("Successfully deleted", len(objectstoDel), 'objects!')
            return response
        except Exception as err:
            raise CustomError("Error in S3objects.Delete_objects_basedOnMetadataTags(): " + str(err))

    def upload_objects(self, object_name, metadata, filecontent, tags):
        try:
            responseDict = self.bucket.put_object(Key=object_name, Metadata=metadata, Body=filecontent, Tagging=tags)
            return responseDict
        except Exception as err:
            raise CustomError('Error in S3objects.upload_objects (): ' + str(err))


if __name__ == '__main__':
    try:
        while True:
            bucketName = input("Enter Bucket_name :")
            bucket = S3objects(bucketName)
            while True:
                prompt = input(" \nSelect the following: \n1. Put_objects\n2.Show_objects\n3.Delete_objects\n")
                if prompt == '1':
                    no_of_objects = input("Count No : of Objects ?")
                    while not no_of_objects.isnumeric():
                        no_of_objects = input("Only Integral values are allowed, enter again :")

                    no_of_objects = int(no_of_objects)
                    for i in range(no_of_objects):
                        object_name = input('Enter the key of Object :')
                        filecontent = ""
                        path = input("enter path of the file to upload")
                        with open(path, r'rb') as file_obj:
                            filecontent = file_obj.read()
                        metadatacount = int(input("Count object's Metadata : "))
                        metadata = Utils.dictInput(metadatacount)
                        tagscount = int(input("Count no_of_tags :"))
                        tags = Utils.dictInput(tagscount)
                        bucket.upload_objects(object_name, metadata, filecontent, Utils.convertDicttostring(tags))
                    print("succesfully uploaded the ", no_of_objects, 'objects ')
                elif prompt == '2':
                    bucket.listexistingObjects()
                elif prompt == '3':
                    metadatacount = int(input("count Object's Metadata :"))
                    metadata = Utils.dictInput(metadatacount)
                    tagscount = int(input("No_of_tags_counted : "))
                    tags_set = Utils.convertDicttosetofTags(Utils.dictInput(tagscount))
                    response = bucket.Delete_objects_basedOnMetadataTags(metadata, tags_set)
                    if response and response["Response_Metadata"]["HTTPS_status_code"] != 200:
                        print(" Something went wrong, check_Delete_objectClass")
                else:
                    print("Invalid prompt, select the correct Option(prompt)")
                    break

    except CustomError as error:
        print(error)
    except Exception as err:
        print("error:", err)

        '''bucket = S3objects.s3.Bucket('mybucket4pyprgm')
        client = boto3.client("s3")
        print('below is the list of objs :')
        for obj in bucket.objects.all():
            print(obj.key)

    def deleteObjects_tags_Mdata(self):

        response = self.bucket.delete_objects(
            Delete={
                'Objects':"Disconnectphoto",
                    
                        'Key': 'string','Quiet': True}) '''
