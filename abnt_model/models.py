from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='image')
    image = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.user.username  # or self.user.email, or another string attribute of User

