from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

class PostModel (models.Model) : 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) : 
        return f"{self.title}"
    


@receiver(post_save, sender = User)
def CreateTokenForUser(created, instance, **kwargs) : 
    if created : 
        Token.objects.create( user = instance)