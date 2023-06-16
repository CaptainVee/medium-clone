from rest_framework.exceptions import APIException


class YouHaveAlreadyRated(APIException):
    status_code = 400
    default_detail = "You have already rated this, abeg no give me wahala"
    default_code = "bad_request"
