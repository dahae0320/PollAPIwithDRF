from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer


"""
    DRF의 CBV로 만든 Poll API
"""
# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         serializer = PollSerializer(polls, many=True)
#         return Response(serializer.data)
#
#
# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(poll)
#         return Response(serializer.data)


# 두 클래스의 내용이 똑같으므로 viewset으로 합친다.
# 이후 url에서 라우팅해준다.
#
# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer
#
#
# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class UserListCreate(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'error': 'Wrong Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    # queryset이나 serializer_class의 속성을 설정하거나
    # get_queryset(), get_serializer_class()를 재정의해야 한다.
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    serializer_class = ChoiceSerializer

    def post(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, pk)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer

    """
    Concrete view for creating a model instance.
    """
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
