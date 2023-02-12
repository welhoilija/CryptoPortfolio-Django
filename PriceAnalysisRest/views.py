# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from .auth_helpers import authenticate_user
import random
import string
import web3 as w3


def generate_message():
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    # Convert the string to hexadecimal
    message = w3.toHex(text=random_string)
    return message


class Auth(APIView):
    def get(self, request):
        # Generate a message and send it to the client
        message = generate_message()
        return Response({'message': message})

    def post(self, request):
        data = request.data['data']
        signature = request.data['signature']
        if authenticate_user(data['public_key'], signature, data):
            # User is authenticated, allow access to protected resources
            return Response({'status': 'success'})
        else:
            # User is not authenticated, return an error
            return Response({'status': 'error'}, status=401)
