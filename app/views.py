from rest_framework import generics, status, decorators, permissions, authentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, PostSerializer,LoginSeriailizer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import PostModel






@decorators.api_view(['GET',"POST"])
@decorators.authentication_classes([authentication.TokenAuthentication])
@decorators.permission_classes([permissions.IsAuthenticatedOrReadOnly])
def ViewPosts (request) : 
    posts = PostModel.objects.order_by('-created_at')

    if request.method == "GET" : 
        seializer = PostSerializer(posts,many=True)
        return Response(seializer.data,status=status.HTTP_200_OK)
    
    if request.method == "POST" : 
        seializer = PostSerializer(data=request.data)
        if seializer.is_valid():
            if request.user == seializer.validated_data['user'] :
                seializer.save()
                return Response(seializer.data,status=status.HTTP_201_CREATED)
        return Response(seializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

        



@decorators.api_view(['GET',"PUT","DELETE"])
@decorators.authentication_classes([authentication.TokenAuthentication])
def UserPost (request, postid) :
    post = get_object_or_404(PostModel, id = postid)

    if request.method == 'GET' : 
        serilizer = PostSerializer(post)
        return Response(serilizer.data,status=status.HTTP_200_OK)

    if request.user == post.user : 
        if request.method == "PUT" :
            serilizer = PostSerializer(post,data=request.data)

            if serilizer.is_valid() :
                serilizer.save()
                return Response(serilizer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        if request.method == "DELETE" : 
            post.delete()
            return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class RegisterView (generics.GenericAPIView) : 

    
    serializer_class = RegisterSerializer

    def post (self, request) : 
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            username = serializer.data['username']
            user = User.objects.get(username = username)

            token = Token.objects.get(user=user).key
            
            
            data = serializer.data
            data['token'] = token
            
            data.pop('password')


            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView (generics.GenericAPIView) : 
    serializer_class = LoginSeriailizer

    def post (self, request) : 
        
        email = request.POST['email']
        password = request.POST['password']

        user = get_object_or_404(User, email = email)
        context = {}

        
        if not user.check_password(password)  :
            msg = {'msg':'invalid passowrd'}
            return Response(msg,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        


        data = RegisterSerializer(user).data

        data['token'] = Token.objects.get(user=user).key
        data.pop('password')
        
        return Response(data,status=status.HTTP_200_OK)
    


