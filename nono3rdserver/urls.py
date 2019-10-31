from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from .views import index

swagger_schema_view = get_swagger_view(title='Nono API')

schema_view = get_schema_view(
   openapi.Info(
      title="Nono API",
      default_version='v1',
      description="REST API for Nono mobile app",
      terms_of_service="https://www.shiptalent.com/terms/",
      contact=openapi.Contact(email="administrator@nono.com"),
      license=openapi.License(name="Nono.com"),
   ),
   # validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API urls
    url(r'^apis(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^swagger-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
    url(r'^api/v1/mailjet/', include('mailjet.urls')),
    # Admin urls
    path('admin/', admin.site.urls),
    # Default urls
    # path('/', index)  
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
