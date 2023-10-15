from django.db import transaction
from django.utils.translation import gettext
from rest_framework import serializers

from packageapp import models


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = "__all__"


class SimplePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = ["id", "name"]


class SubscribeItemSerializer(serializers.ModelSerializer):
    package = PackageSerializer()

    class Meta:
        model = models.SubscribeItem
        fields = ["id", "package"]


class AddSubscribeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeItem
        fields = ["id", "package"]

    def save(self, **kwargs):
        self.instance = models.SubscribeItem.objects.filter(
            package=self.validated_data["package"], subscribe=self.context["subscribe"]
        ).first()

        if self.instance is not None:
            raise serializers.ValidationError(gettext("Already Added"))
        else:
            return models.SubscribeItem.objects.create(
                subscribe=self.context["subscribe"], package=self.validated_data["package"]
            )


class UpdateSubscribeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeItem
        fields = ["package"]


class SubscriptionItemSerializer(serializers.ModelSerializer):
    package = SimplePackageSerializer()

    class Meta:
        model = models.SubscriptionItem
        fields = ["id", "package", "item_price"]


class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_items = SubscriptionItemSerializer(many=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = models.Subscription
        fields = [
            "id",
            "date",
            "subscription_items",
            "total",
        ]

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")


class CreateSubscriptionSerializer(serializers.Serializer):
    def save(self, **kwargs):
        subscribe = self.context["subscribe_id"]
        user = self.context["user"]

        if subscribe != models.Subscribe.objects.filter(user=user).values_list("id", flat=True)[0]:
            raise serializers.ValidationError(gettext("You don't have permission for this action"))

        elif not models.SubscribeItem.objects.filter(subscribe=subscribe).exists():
            raise serializers.ValidationError(gettext("Nothing is selected"))

        with transaction.atomic():
            subscribeitems = models.SubscribeItem.objects.select_related("package").filter(
                subscribe=subscribe
            )
            total = sum(item.package.price for item in subscribeitems)
            subscription = models.Subscription.objects.create(user=user, total=total)
            subscriptionitems = [
                models.SubscriptionItem(
                    subscription=subscription,
                    package=item.package,
                    item_price=item.package.price,
                )
                for item in subscribeitems
            ]
            models.SubscriptionItem.objects.bulk_create(subscriptionitems)
            models.SubscribeItem.objects.filter(subscribe=subscribe).delete()
            return subscription
