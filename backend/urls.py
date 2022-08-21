from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views import OrderViewset, CommentView

router = DefaultRouter()
router.register('orders', OrderViewset)



app_name = 'backend'

urlpatterns = [
    path('comment/', CommentView.as_view(), name='comment'),

] + router.urls
