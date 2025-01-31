from rest_framework.exceptions import APIException
from rest_framework import status

class BlogIsAlreadyRated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User has already rated this blog.'
    default_code = 'bad_request'

class TooManyRatingRequests(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'This blog post has received too many rating requests.'
    default_code = 'too_many_requests'