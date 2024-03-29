import datetime

from flask import current_app
from google.cloud import storage
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.

    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, current_app.config['ALLOWED_EXTENSIONS'])
    filename = _safe_filename(filename)
    client = storage.Client.from_service_account_json(
    "D:\WinDev\keys\jupez-p-190b34beb77b.json"
)
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filename)

    blob.upload_from_string(file_stream, content_type=content_type)

    url = blob.public_url

    return url
