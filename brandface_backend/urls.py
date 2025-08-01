from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Brandface API",
      default_version='v1',
      description="API documentation for Brandface system with Admin",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dhoomatech@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/<str:version>/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/<str:version>/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('users/api/<str:version>/', include('users_app.urls')),
   path('cards/api/<str:version>/', include('cards.urls')),
   path('social-media/api/<str:version>/', include('social_media.urls')),
   path('enquiries/api/<str:version>/', include('enquiries.urls')),


   # Swagger
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   path('integrations/', include('thirdparty_api.urls')),
   path('projectag/', include('projectag.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)