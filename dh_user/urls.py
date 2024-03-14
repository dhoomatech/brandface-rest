from rest_framework import routers
from dh_user.views import UserViewSet,AddressViewSet
from django.urls import include, path
# from . import views

app_name = "users"

router = routers.DefaultRouter()
router.register(f"address", AddressViewSet)
router.register("", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]