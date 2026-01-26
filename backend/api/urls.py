from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DatasetViewSet, health_check

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('datasets/<int:pk>/report/', DatasetViewSet.as_view({'get': 'report'}), name='dataset-report'),
    path('datasets/<int:pk>/summary/', DatasetViewSet.as_view({'get': 'summary'}), name='dataset-summary'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('health/', health_check, name='health_check'),
]