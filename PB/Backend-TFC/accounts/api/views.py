from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import User
from django.contrib.auth import login
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404, RetrieveAPIView, UpdateAPIView
from accounts.api.serializers import RegisterSerializer, LoginSerializer, EditProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get(self, request):
        return Response({"Message": "Register to start"})

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Profile was successfully created!'
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['email'] = user.email
            data['phone_number'] = user.phone_number
            data['avatar'] = str(user.avatar)
        else:
            data = serializer.errors
        return Response(data)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"Message": "Login"})

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"Response": "Login was successful!"})


class ProfileAPIView(RetrieveAPIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated, AllowAny]
    permission_classes = [AllowAny]

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request, *args, **kwargs):
        data = {}
        user = get_object_or_404(self.get_queryset(), pk=request.user.id)
        if user:
            data['id'] = request.user.id
            data['username'] = user.username
            # data['first_name'] = user.first_name
            # data['last_name'] = user.last_name
            # data['phone_number'] = user.phone_number
            # data['email'] = user.email
            # data['avatar'] = user.avatar
        return Response(data)


class DataProfileAPIView(RetrieveAPIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,AllowAny]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    queryset = User.objects.all()


#
class EditProfileAPIView(UpdateAPIView):
    serializer_class = EditProfileSerializer
    # permission_classes = [IsAuthenticated, AllowAny]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    queryset = User.objects.all()

    def get_queryset(self):
        user = User.objects.filter(id=self.kwargs['id'])
        print(user)
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EditProfileSerializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save(self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['id'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        serializer = EditProfileSerializer(instance)
        return Response(serializer.data)
