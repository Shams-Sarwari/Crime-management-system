from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email = username)
            
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(licence_num = username)
            except UserModel.DoesNotExist:
                return None

        if user is not None:
            if user.password == password:
                return user
        
        
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist: 
            return None
        