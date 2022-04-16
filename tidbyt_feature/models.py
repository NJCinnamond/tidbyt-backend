from django.db import models

# Create your models here.
class TidbytFeature(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey('user.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class FeatureType(models.TextChoices):
        MORNING_MESSAGE = 'MM', ('Morning Message')
        PICTURE_OF_DAY = 'POD', ('Picture of Day')

    feature_type = models.CharField(
        max_length=3,
        choices=FeatureType.choices,
    )