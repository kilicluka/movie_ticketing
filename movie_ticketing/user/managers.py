from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password):
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        return self._create_user(email, password, is_superuser=True, is_staff=True)
