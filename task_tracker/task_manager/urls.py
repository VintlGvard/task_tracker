from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, CommentViewSet
from projects.views import ProjectViewSet
from user.views import UserViewSet

router = DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]