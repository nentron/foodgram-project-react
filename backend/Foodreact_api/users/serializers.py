from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}
        read_only = ['is_subscribed']

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSetSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context.get('request').user
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        if not user.check_password(current_password):
            raise serializers.ValidationError('Wrong current password')
        user.set_password(new_password)
        user.save()
        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
        else:
            raise serializers.ValidationError(
                'Wrong password or email.'
            )
        data['user'] = user
        return data