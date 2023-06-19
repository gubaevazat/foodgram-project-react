from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from serializers import UserSerializer
import djoser

# User = settings.AUTH_USER_MODEL


