from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from polls import apiview


class TestPolls(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = apiview.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        user = get_user_model()
        return user.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='test',
        )

    # APIRequestFactory을 사용한 GET 메서드 테스트 함수
    def test_list(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {0}'.format(self.token.key)
        )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Expected Response Code 200, received {0} instead.'.format(response.status_code)
        )

    # APIClient을 사용한 GET 메서드 테스트 함수
    # url에 직접 GET, POST 요청을 하여 응답 받는다.
    def test_list2(self):
        self.client.login(
            username=self.user.username,
            password='test'
        )
        response = self.client.get(self.uri)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Expected Response Code 200, received {0} instead.'.format(response.status_code)
        )

    def test_create(self):
        self.client.login(username=self.user.username, password='test')
        params = {
            "question": "How are you?",
            "created_by": self.user.id,
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'Expected Response Code 201, received {0} instead.'.format(response.status_code)
        )
