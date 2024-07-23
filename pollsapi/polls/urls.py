from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .apiview import PollViewSet, ChoiceList, CreateVote, UserListCreate, LoginView


router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

# pollViewSetPattern = PollViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user_create'),
    # obtain_auth_token은 ObtainAuthToken.as_view()와 같다.
    # path('login/', views.obtain_auth_token, name='login'),
    # 아래의 path 대신 obtain_auth_token을 사용해도 된다. (동일)
    path('login/', LoginView.as_view(), name='login'),
    path('polls/', PollViewSet.as_view({'get': 'list', 'post': 'create'}), name='polls'),
    path('polls/<int:pk>/choices/', ChoiceList.as_view(), name='choice_list'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name='vote'),
]

urlpatterns += router.urls
