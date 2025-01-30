from rest_framework.exceptions import APIException

class BlogIsAlreadyRated(APIException):
    status_code = 400
    default_detail = 'User has already rated this blog.'
    default_code = 'bad_request'