from django.urls import path
from accounts.api.views import RegisterAPIView, LoginAPIView, ProfileAPIView, EditProfileAPIView, DataProfileAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
#
app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/<int:id>/', DataProfileAPIView.as_view(), name='profile2'),
    path('<int:id>/profile/edit/', EditProfileAPIView.as_view(), name='edit_profile'),
]
