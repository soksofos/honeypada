
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .hashers import HoneywordHasher

class HoneywordsBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if self.user_can_authenticate(user):
                hasher = HoneywordHasher()
                status = hasher.verify(password, user.password)
                if status == 'CORRECT':
                    return user
                elif status == 'BADWORD':
                    user.is_active = False
                    user.save()
