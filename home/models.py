from django.db import models

# Create your models here.


class pics(models.Model):
    img=models.ImageField(upload_to='test')