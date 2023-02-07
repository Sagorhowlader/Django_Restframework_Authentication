from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializers, UserRegistrationSerializer, UserLoginSerializer


# Create your views here.

class UserListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        users = User.objects.all()
        pagination = LimitOffsetPagination()
        result_data = pagination.paginate_queryset(users, request)
        if result_data is None:
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        serializers = UserSerializers(result_data, many=True)
        return pagination.get_paginated_response(serializers.data)


class ViewUserRegistration(APIView):
    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewUserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)


class ViewUserDetails(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializers(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data="User not found", status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializers(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data="User not found", status=status.HTTP_400_BAD_REQUEST)
