from django.contrib import admin

from packageapp import models


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "price",
    ]


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]


@admin.register(models.SubscribeItem)
class SubscribeItemAdmin(admin.ModelAdmin):
    list_display = [
        "subscribe",
        "package",
    ]


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date",
    ]


@admin.register(models.SubscriptionItem)
class SubscriptionItemAdmin(admin.ModelAdmin):
    list_display = [
        "subscription",
        "package",
        "item_price",
    ]
