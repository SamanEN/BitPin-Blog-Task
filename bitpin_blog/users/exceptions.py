from rest_framework.exceptions import APIException

class UserIsRepetitive(APIException):
    status_code = 400
    default_detail = 'The input username already exists.'
    default_code = 'bad_request'