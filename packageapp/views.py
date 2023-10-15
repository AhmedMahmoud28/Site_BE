from django.utils.translation import gettext
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from packageapp import models, serializers


class PackageView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["^name"]
    ordering_fields = ["price"]


class SubscribeItemView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    serializer_class = serializers.SubscribeItemSerializer

    def get_queryset(self):
        return models.SubscribeItem.objects.select_related("package").filter(
            subscribe=self.request.user.subscribe
        )

    def get_serializer_context(self):
        return {"subscribe": self.request.user.subscribe}

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddSubscribeItemSerializer
        elif self.action == "update":
            return serializers.UpdateSubscribeItemSerializer
        return super().get_serializer_class()


class SubscriptionView(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    serializer_class = serializers.SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {gettext("Subscription is Completed")},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        return {
            "user": self.request.user,
            "subscribe_id": self.request.user.subscribe.id,
        }

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateSubscriptionSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return models.Subscription.objects.prefetch_related(
            "subscription_items", "subscription_items__package"
        ).filter(user=self.request.user)
