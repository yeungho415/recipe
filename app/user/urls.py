"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]

# 1. A client sends a POST request to your application's "/create/" URL.

# 2. Django looks up this URL in your URL mappings and sees that it should
# use the CreateUserView to handle the request.

# 3. The CreateUserView uses the UserSerializer to validate the incoming
# JSON data and convert it into a Python dictionary that can be used to create a User instance.

# 4. The CreateUserView calls the UserSerializer's create method to create
# a new User instance and save it to the database.

# 5. The CreateUserView uses the UserSerializer to convert the newly
# created User instance into JSON format and sends this JSON data back to the client in an HTTP response.