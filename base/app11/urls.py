from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework.schemas import get_schema_view

from .views import UserViewSet, CoordsViewSet, LevelViewSet, ImagesViewSet, PerevalAddedViewSet
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title="tbase_api",
        default_version='v1',
        description="Description of your API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('coords', CoordsViewSet)
router.register('levels', LevelViewSet)
router.register('images', ImagesViewSet)
router.register('perevaladded', PerevalAddedViewSet)




urlpatterns = [
    path('swagger/', schema_view, name='schema-swagger-ui'),
    path('redoc/', schema_view, name='schema-redoc'),
    #path('submit/', PerevalAddedViewSet.as_view({'post': 'submitData'}), name='submit'),
    # path('', RedirectView.as_view(url='submit/')),
    path('', include(router.urls)),
    path('perevaladded/', PerevalAddedViewSet.as_view({'get': 'retrieve_perevaladded_object'}), name='perevaladded-detail'),
    path('patch/<int:id>/', PerevalAddedViewSet.as_view({'get': 'submitDataUpdate', 'patch': 'submitDataUpdate'}), name='perevaladded-detail'),
    path('email/<str:email>/', PerevalAddedViewSet.as_view({'get': 'submitDataByEmail'}), name='submit-by-email'),
]
