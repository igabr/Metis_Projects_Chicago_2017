#created by Ibrahim Gabr
import os
import boto3
import botocore

ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]

SECRET_KEY = os.environ['AWS_SECRET_KEY']

def view_all_buckets():
    """
    There are no inputs to this function.
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    response = s3.list_buckets()

    buckets = [bucket['Name'] for bucket in response['Buckets']]

    print("Here are all your buckets on Amazon S3:\n")
    print(buckets)
    print()

    return buckets

def create_bucket(name_of_bucket):
    """
    Enter the name of the bucket to be created.
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    created = s3.create_bucket(Bucket=name_of_bucket)

    if created:
        print("Bucket {} created!".format(name_of_bucket))


def view_keys_in_bucket(name_of_bucket):
    """
    Enter the name of the bucket.
    """
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket = s3.Bucket(name_of_bucket)

    print("Here are all the files stored in your bucket:\n")
    for key in bucket.objects.all():
        print(key.key)
        print()

def upload_to_bucket(name_of_file, key, bucket_name):
    """
    Name of file, key, bucket name
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    check_s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket = bucket_name

    filename = name_of_file

    try:
        check_s3.meta.client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("{0} bucket does not exist".format(bucket_name))

    s3.upload_file(filename, bucket, key)

    print("{0} uploaded to {1} bucket with a key of {2}".format(name_of_file, bucket_name, key))

def upload_multiple_files(files, keys, bucket_name):
    """
    list of files, list of keys, bucket name
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    check_s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket = bucket_name

    try:
        check_s3.meta.client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("{0} bucket does not exist".format(bucket_name))

    for index, filename in enumerate(files):
        s3.upload_file(filename, bucket, keys[index])
        print("Uploaded {0} to {1} bucket with the key {2}".format(filename, bucket, keys[index]))
        print()

def download_from_bucket(bucket_name, key, local_filename):
    """
    bucket name, key, local filename
    """
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = bucket_name 
    key_id = key

    try:
        download = s3.Bucket(bucket).download_file(key_id, local_filename)
        print("{0} file/object downloaded from {1} bucket as {2}.\n\nFile/object can be found here: {3}".format(key, bucket_name, local_filename, os.getcwd()))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The file/object does not exist - do you have the right bucket?")
        else:
            raise

def download_bucket(bucket_name):
    """
    Downloads an entire bucket!

    Just provide the bucket_name
    """

    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket_obj = s3.Bucket(bucket_name)
    
    all_files = []

    for key in bucket_obj.objects.all():
        all_files.append(key.key)

    for key in all_files:
        download = s3.Bucket(bucket_name).download_file(key, key)
        print("{0} file/object downloaded from {1} bucket as {2}.\n\nFile/object can be found here: {3}".format(key, bucket_name, key, os.getcwd()))
        print()

    print("The entire {} bucket has been downloaded!".format(bucket_name))

def delete_key(key, bucket_name):
    """
    key, bucket name
    """
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket = s3.Bucket(bucket_name)

    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("{0} bucket does not exist".format(bucket_name))

    for key_id in bucket.objects.all():
        if key_id.key == key:
            key_id.delete()
            print("{0} file/object deleted! from {1} bucket".format(key, bucket_name))

def delete_bucket(bucket_name):
    """
    bucket name
    """
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    bucket = s3.Bucket(bucket_name)

    view_keys_in_bucket(bucket_name)

    answer = input("To delete a bucket, you must delete all the keys inside that bucket first. Do you want to continue? [y/n]: ")

    if answer == 'y':
        check = input("Are you sure? [y/n]")

        if check == 'y':

            for key in bucket.objects.all():
                print("deleting {0}".format(key.key))
                print()
                key.delete()
            bucket.delete()

            print("{0} bucket has been deleted".format(bucket_name))
        else:
            print()
            print("delete_bucket function exited")
    else:
        print()
        print("delete_bucket function exited")
