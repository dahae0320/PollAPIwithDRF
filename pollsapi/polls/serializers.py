from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Poll, Choice, Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # create 메서드를 재정의한 이유는 '사용자의 비밀번호를 해싱하여 저장하기 위해서'이다.
    # `set_password` 메서드는 비밀번호를 해싱하여 안정하게 저장해주는 기능을 제공한다.
    def create(self, validated_data):
        # User 객체를 생성하면서 username과 email을 설정
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        # 비밀번호를 해싱하여 설정
        user.set_password(validated_data['password'])
        # User 객체를 데이터베이스에 저장
        user.save()
        # user에 대한 Token 생성
        Token.objects.create(user)
        return user
