from rest_framework.response import Response
from rest_framework.exceptions import APIException

from rest_framework.response import Response
from rest_framework import status




class CustomErrorResponse(Response):
    def __init__(self, data=None, status=None):
        super().__init__(data, status=status)

    @property
    def status_code(self):
        if self.data and 'status_code' in self.data:
            return self.data['status_code']
        return super().status_code

    def render(self):
        return super().render()


class CustomSuccessResponse(Response):
    def __init__(self, data=None, status=None):
        super().__init__(data, status)

    def render(self):
        return super().render()

class CustomError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Custom error occurred.'
    default_code = 'custom_error'