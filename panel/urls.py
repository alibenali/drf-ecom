from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # For login
from .views import UserViewSet, StoreViewSet, StaffViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, OrderLogViewSet, PromoCodeViewSet, SubscriptionViewSet
from .views.auth_views import SignupAPIView, CustomLoginAPIView  # Import the new login view

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'order-logs', OrderLogViewSet)
router.register(r'promo-codes', PromoCodeViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomLoginAPIView.as_view(), name='api_login'),  # Replace obtain_auth_token
    path('auth/signup/', SignupAPIView.as_view(), name='api_signup'),  # Signup endpoint
]