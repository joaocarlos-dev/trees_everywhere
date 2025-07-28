from django.contrib import admin
from django.urls import include, path, re_path
from users.views import CustomAuthTokenQueryParamView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Trees Everywhere API",
        default_version='v1',
        description="API para listar árvores plantadas pelo usuário",
        contact=openapi.Contact(email="seu-email@dominio.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('trees.urls')),
    path('api-token-auth/', CustomAuthTokenQueryParamView.as_view(),
         name='api_token_auth'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
