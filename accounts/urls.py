from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view({'post': 'create'}), name='signup_url')
]
