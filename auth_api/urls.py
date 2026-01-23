from django.urls import path
from .views import ValidateAuth0TokenView

urlpatterns = [
    path('validate-token/', ValidateAuth0TokenView.as_view(), name='validate-token'),
]
