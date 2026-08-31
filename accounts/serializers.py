from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only' : True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username or password')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid username or password')

        attrs['user'] = user
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
            'first_name',
            'last_name',
            'avatar',
        ]

        def update(self , instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.avatar = validated_data.get('avatar', instance.avatar)

            instance.save()
            return instance
    