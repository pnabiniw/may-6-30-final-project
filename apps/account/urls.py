from django.urls import path
from .views import UserRegistrationView, UserLoginView, user_logout, user_account_activation, \
    UserProfileView, UserProfileUpdateView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('activate/<str:username>/<str:key>/', user_account_activation, name='user_account_activation'),

    path('user-profile/', UserProfileView.as_view(), name="user_profile"),
    path('user-profile-update/', UserProfileUpdateView.as_view(), name="user_profile_update"),
]
