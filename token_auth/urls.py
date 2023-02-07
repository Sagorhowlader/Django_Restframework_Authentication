from django.urls import path

from token_auth.views import UserListView, ViewUserRegistration, ViewUserLogin, ViewUserDetails

urlpatterns = [
    path('user/get-list/', UserListView.as_view(), name='token-user-list'),
    path('user/registration/', ViewUserRegistration.as_view(), name='token-user-registration'),
    path('user/login/', ViewUserLogin.as_view(), name='token-user-login'),
    path('user/<int:id>/', ViewUserDetails.as_view(), name='token-user-details')
]
