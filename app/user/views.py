"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

# CreateAPIView: Inherits from CreateModelMixin and GenericAPIView to
# support POST requests to create new instances of a model.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# sequence of Auth and token generation
# -----------------------------------------------------------------------------------------
# The HTTP request hits the server and Django matches the URL path to a corresponding
# view function or class in your urls.py. In your case, it'll match the request to CreateTokenView.

# Django REST Framework determines the type of request (POST in this case)
# and delegates it to the appropriate method in your view class. For CreateTokenView,
# that's the post() method inherited from ObtainAuthToken.

# The post() method creates an instance of your serializer class (AuthTokenSerializer)
# and passes the incoming request data to it.

# The __init__() method in AuthTokenSerializer is called, initializing an instance of the serializer.

# The is_valid() method is called on the serializer instance. This checks
# the request data against the fields defined in your serializer
# (email and password), and runs any field-level validation you've defined.

# If the data is valid, is_valid() calls the validate() method on the
# serializer, which contains your custom validation code. In your case,
# it attempts to authenticate the user.

# If validate() completes successfully, it adds the authenticated user
# to the attrs dictionary and returns it.

# The post() method in ObtainAuthToken then calls the serializer's
# validated_data property, which contains the validated data returned from validate().

# The post() method uses this validated data to create an auth token for the
# user and sends a response back to the client containing the token.

# If at any point the data is not valid or an error occurs
# (such as authentication failure), an appropriate HTTP error response is sent back to the client.

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):  # when you make a http get request to this endpoint, this method will be called
        """Retrieve and return the authenticated user."""
        return self.request.user
