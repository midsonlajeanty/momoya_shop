import os
import uuid
import datetime
from django.utils.deconstruct import deconstructible

@deconstructible
class uploder(object):
    """Upload file to path

    Args:
        path (string): path to upload file

    Returns:
        string: path to file
    """

    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, instance, filename):
        ext = tuple(filename.split("."))[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        dirname = datetime.datetime.now().strftime(str(self.prefix))
        return os.path.join(dirname, filename)