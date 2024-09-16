from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status


class AppException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'An unknown error occurred.'
    default_code = 'invalid'

    def __init__(self, detail=None, status_code=None):
        self.detail = detail
        self.status_code = status_code
        super(AppException, self).__init__(detail, None)
