from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PostModel
from rest_framework.validators import ValidationError



class PostSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = PostModel
        fields = '__all__'

class RegisterSerializer (serializers.ModelSerializer) :

    class Meta :
        model = User
        fields = ['username','email','first_name','last_name','password']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']


        user = User.objects.create_user(username = username, email = email , password=password,first_name = first_name, last_name = last_name)
        user.save()
        
        return user

class LoginSeriailizer (serializers.ModelSerializer) : 
    class Meta : 
        model = User 
        fields = ['email','password']


