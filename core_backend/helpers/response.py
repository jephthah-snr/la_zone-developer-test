from rest_framework.response import Response


def success_response(message, status_code, *args):
    response_data = {
        'status': True,
        'message': message,
        'response': args
    }
    return Response(response_data, status=status_code)

def error_response(message, status_code):
    response_data = {
        'status': False,
        'message': message,
    }
    return Response(response_data, status=status_code)