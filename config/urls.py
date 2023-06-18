from django.contrib import admin
from django.urls import path, include
from drf_yasg.openapi import Info, Contact, License
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

api_description = "API for the first service in Uzbekistan for watching movies, TV shows, and cartoons."

schema_view = get_schema_view(
	Info(
		"Movie Plus API", 'v1', api_description, "https://www.google.com/policies/terms/",
		Contact(email="contact@snippets.local"), License(name="BSD License")
	),
	public=True,
	permission_classes=[AllowAny]
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('movies.urls')),
	# Swagger
	path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
