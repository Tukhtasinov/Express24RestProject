from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Role(models.Model):
    name = models.CharField(max_length=20)


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)



