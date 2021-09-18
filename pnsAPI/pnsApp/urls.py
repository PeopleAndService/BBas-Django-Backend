from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.conf.urls import url 
from pnsApp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_patterns = [ 
    path('v1/', include('pnsApp.urls')), 
    ]
schema_view = get_schema_view( 
    openapi.Info( 
        title="Django API", 
        default_version='v1', 
        terms_of_service="https://www.google.com/policies/terms/",
         ), 
        public=True, 
        permission_classes=(permissions.AllowAny,), 
        patterns=schema_url_patterns, 
        )
#url(r'^pnsApp/(?P<slug>[-a-zA-Z0-9_]+)$', views.pns_detail),
urlpatterns = [ #POST형식으로 바꿔야함
    url(r'^pnsApp/(?P<pk>[0-9]+)$', views.pns_list, name="값 가져오기"),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^pnsApp/auth/signin', views.account_SignIn),
    url(r'^pnsApp/auth/signup', views.account_SignUp),
]