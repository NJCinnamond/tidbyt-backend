from django.db import models

# Create your models here.
class TidbytDevice(models.Model):
    device_id = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)
    auth_code = models.TextField()
    owner = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
