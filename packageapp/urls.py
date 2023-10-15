from django.urls import include, path
from rest_framework.routers import DefaultRouter

from packageapp import views

router = DefaultRouter()
router.register("packages", views.PackageView)
router.register("subscribe", views.SubscribeItemView, basename="subscribe")
router.register("subscription", views.SubscriptionView, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),
]
