from django.contrib.auth.models import Permission
from rest_framework import serializers

from question.models import Question
from user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # questions = serializers.HyperlinkedRelatedField(many=True, view_name='question-detail', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# class PermissionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Permission
#         fields = ('name',)
