from django.urls import path
from rest_framework.routers import DefaultRouter
from auth_app.views import AuthViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = router.urls