from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db import models
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    repeat_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    phone_number = serializers.CharField()
    avatar = serializers.FileField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'avatar', 'phone_number', 'password', 'repeat_password')
        extra_kwargs = {'password': {'write_only': True},
                        'repeat_password': {'write_only': True}
                        }
        depth = 1

    def save(self):
        print(self.validated_data['avatar'])
        gave_avatar = any([keys == 'avatar' for keys in self.validated_data.keys()])
        if not gave_avatar:
            self.validated_data['avatar'] = None

        try:

            check = User.objects.filter(username=self.validated_data['username'])
            if check:
                raise IntegrityError
            else:
                user = User.objects.create_user(username=self.validated_data['username'],
                                                email=self.validated_data['email'],
                                                first_name=self.validated_data['first_name'],
                                                last_name=self.validated_data['last_name'],
                                                phone_number=self.validated_data['phone_number'],
                                                avatar=self.validated_data['avatar'])

                password1 = self.validated_data['password']
                password2 = self.validated_data['repeat_password']

                if password1 != password2:
                    raise serializers.ValidationError({'password': 'Passwords do not match!'})
                user.set_password(password1)
                user.save()

        except (IntegrityError, Http404):
            raise serializers.ValidationError({'username': 'username already taken!'})

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True,
                                     trim_whitespace=False)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, validated_data):
        try:
            username = validated_data['username']
            password = validated_data['password']
            users = User.objects.get(username=username)
            user = users
            if not username:
                raise serializers.ValidationError({'username': 'Username is not registered.'})
            if not password:
                raise serializers.ValidationError({'password': 'Password is incorrect.'})
            else:
                if user.is_active:
                    user = authenticate(request=self.context.get('request'), username=username, password=password)
                    if not user:
                        raise serializers.ValidationError({'Message': 'Wrong username or password'})
                    validated_data['user'] = user
        except models.ObjectDoesNotExist:
            raise serializers.ValidationError({"username": "Not registered. Please register yourself first"})

        return validated_data


class EditProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, style={'input_type': 'password'}, write_only=True)
    repeat_password = serializers.CharField(required=False, style={'input_type': 'password'}, write_only=True)
    avatar = serializers.ImageField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'password', 'repeat_password')
        extra_kwargs = {'password': {'write_only': True},
                        'repeat_password': {'write_only': True}}
        # depth = 1

    # def validate_phone_number(self, data):
    #     if len(data) < 10:
    #         raise serializers.ValidationError({"Message": "Phone Number length must be 10"})

    def save(self, _id):
        print(self.validated_data)
        keys = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'password', 'repeat_password']
        for k in keys:
            if k not in self.validated_data.keys():
                print(k)
                self.validated_data[k] = ""

        # gave_avatar = any([keys == 'avatar' for keys in self.validated_data.keys()])
        # if not gave_avatar:
        #     self.validated_data['avatar'] = 'profile_avatars/default.jpg'

        try:
            user = get_object_or_404(User, pk=_id)
            if user:
                # User.objects.update_or_create()
                print(user)
                print(self.validated_data)
                if self.validated_data['username'] != "":
                    user.username = self.validated_data['username']

                if self.validated_data['email'] != "":
                    user.email = self.validated_data['email']

                if self.validated_data['first_name'] != "":
                    user.first_name = self.validated_data['first_name']

                if self.validated_data['last_name'] != "":
                    user.last_name = self.validated_data['last_name']

                if self.validated_data['phone_number'] != "":
                    print(self.validated_data['phone_number'])
                    user.phone_number = self.validated_data['phone_number']

                if len(self.validated_data['password']) != len(self.validated_data['repeat_password']):
                    raise serializers.ValidationError({'password': 'Passwords do not match!'})
                if self.validated_data['avatar'] != "":
                    print(self.validated_data['avatar'])
                    user.avatar = self.validated_data['avatar']

                if self.validated_data['password'] != self.validated_data['repeat_password']:
                    raise serializers.ValidationError({'password': 'Passwords do not match!'})

                if self.validated_data['password'] == "" and self.validated_data['repeat_password'] != "":
                    pass

                if self.validated_data['password'] != "" and self.validated_data['repeat_password'] != "" \
                        and self.validated_data['password'] == self.validated_data['repeat_password']:
                    user.set_password(self.validated_data['password'])
                    user.save(_id)
                user.save()

        except Http404:
            raise serializers.ValidationError({'username': 'useranme already taken!'})

        user.save()
        return user
