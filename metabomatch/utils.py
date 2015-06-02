import boto
import os
try:
    from metabomatch.private_keys import S3_KEY, S3_BUCKET, S3_SECRET, S3_UPLOAD_DIRECTORY
except ImportError:
    S3_UPLOAD_DIRECTORY, S3_SECRET, S3_BUCKET, S3_KEY = '', '', '', ''

from werkzeug.utils import secure_filename


def s3_upload(source_file, destination_filename, acl='public-read'):
    """ Uploads WTForm File Object to Amazon S3

        Expects following app.config attributes to be set:
            S3_KEY              :   S3 API Key
            S3_SECRET           :   S3 Secret Key
            S3_BUCKET           :   What bucket to upload to
            S3_UPLOAD_DIRECTORY :   Which S3 Directory.

        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    """

    source_filename = secure_filename(source_file.data.filename)
    source_extension = os.path.splitext(source_filename)[1]

    # Connect to S3 and upload file.
    conn = boto.connect_s3(os.environ.get('S3_KEY') or S3_KEY, os.environ.get("S3_SECRET") or S3_SECRET)
    b = conn.get_bucket(os.environ.get("S3_BUCKET") or S3_BUCKET)

    sml = b.new_key("/".join([os.environ.get("S3_UPLOAD_DIRECTORY") or S3_UPLOAD_DIRECTORY, destination_filename]))
    sml.set_contents_from_string(source_file.data.read())
    sml.set_acl(acl)

    return destination_filename


def s3_upload_from_server(source_file, destination_filename, acl='public-read'):
    """
    Directly upload a file existing on the server
    :param source_file:
    :param destination_filename:
    :param acl:
    :return:
    """
    conn = boto.connect_s3(os.environ.get('S3_KEY') or S3_KEY, os.environ.get("S3_SECRET") or S3_SECRET)
    b = conn.get_bucket(os.environ.get("S3_BUCKET") or S3_BUCKET)

    sml = b.new_key("/".join([os.environ.get("S3_UPLOAD_DIRECTORY") or S3_UPLOAD_DIRECTORY, destination_filename]))
    sml.set_contents_from_filename(source_file)
    sml.set_acl(acl)


def s3_delete(key):
    """
    delete a key from config bucket
    :param key: here it will be a software name for example
    :return:
    """
    conn = boto.connect_s3(os.environ.get('S3_KEY') or S3_KEY, os.environ.get("S3_SECRET") or S3_SECRET)
    b = conn.get_bucket(os.environ.get("S3_BUCKET") or S3_BUCKET)
    return b.delete_key(key)


def mean(l):
    return float(sum(l)) / len(l)
