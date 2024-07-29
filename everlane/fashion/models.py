from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

<<<<<<< HEAD
# Create your models here.
=======
>>>>>>> bf058002dd74e9957049c46f595a36a81cfb08e8
