from rest_framework.routers import SimpleRouter
from core.user.viewsets import UserViewSet
from core.auth.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet

# router=routers.DefaultRouter()
# router.register(r'login',LoginViewSet,basename='auth-login')
# router.register(r'register',RegistrationViewSet,basename='auth-register')
# router.register(r'user',UserViewSet,basename='user')
# urlpatterns=[
#     path('',include(router.urls))
# ]
#
routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]

# from django.urls import path,include
# from rest_framework import routers
# from .views import HousingViewsets,WaterjacketViewsets
# router=routers.DefaultRouter()
# router.register(r'housing',HousingViewsets)
# router.register(r'waterjacket',WaterjacketViewsets)
# urlpatterns=[
#     path('',include(router.urls))
# ]