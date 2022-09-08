from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views import OrdersViewset, CommentView, CashViewset, CloseOrderView, OrderDoneView

router = DefaultRouter()
router.register('orders', OrdersViewset)
router.register('cash', CashViewset)


app_name = 'backend'

urlpatterns = [
    path('comment/', CommentView.as_view(), name='comment'),
    path('closeorder/', CloseOrderView.as_view(), name='closeorder'),
    path('orderdone/', OrderDoneView.as_view(), name='orderdone')

] + router.urls