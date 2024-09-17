import hashlib
import uuid
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django_restql.fields import DynamicSerializerMethodField
from reportlab.rl_settings import verbose
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import django_filters.rest_framework

from Shop.utils.viewset import CustomModelViewSet
from Shop.utils.serializers import CustomModelSerializer
from Shop.utils.json_response import SuccessResponse, DetailResponse, ErrorResponse
from Shop.utils.validator import CustomUniqueValidator