from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from userapp.serializers import LoginSerializer, UserDataSerializer, UserSerializer


class UserViewSet(
    viewsets.GenericViewSet,
    APIView,
):
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        elif self.action == "modify":
            return UserDataSerializer
        elif self.action == "retrieve_me":
            return UserDataSerializer
        return super().get_serializer_class()

    @action(methods=["post"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["get"], detail=False)
    def retrieve_me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=["put"], detail=False)
    def modify(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["delete"], detail=False)
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
