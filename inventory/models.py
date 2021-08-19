from django.db import models

from django.contrib.auth.models import User

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.TextField(blank=True)
    desc = models.TextField(blank=True)
    qrcode = models.ImageField(upload_to='images/', blank=True)
    tag = models.CharField(max_length=100)

    Private = 'Private'
    Public = 'Public'

    PRIVACY = [
        (Private, 'Private'),
        (Public, 'Public'),
    ]
    
    privacy = models.CharField(
            max_length=10,
            choices=PRIVACY,
            default=Private,
        )

    def __str__(self):
        return self.name