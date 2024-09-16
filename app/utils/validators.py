from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
import pylibmagic
import magic

from app.exceptions import AppException


def file_size_validator(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


def validate_file_type(file: any, allowed_mime_types: list):
    # Open the file in binary mode and read its content
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(1024))  # Read a small portion of the file

    # Reset the file pointer to the start
    file.seek(0)

    # Check if the file's MIME type is in the allowed list
    if file_mime_type not in allowed_mime_types:
        raise AppException(f'Invalid file type. Allowed types are: {", ".join(allowed_mime_types)}',
                           status_code=status.HTTP_400_BAD_REQUEST)


def validate_columns(columns: list, allowed_columns: list):
    if len(columns) != len(allowed_columns):
        raise AppException(f'Column numbers do not match allowed columns.', status_code=status.HTTP_400_BAD_REQUEST)
    for column in columns:
        if column not in allowed_columns:
            raise AppException(f'Column not found. Allowed columns are {", ".join(allowed_columns)}', status_code=status.HTTP_400_BAD_REQUEST)
