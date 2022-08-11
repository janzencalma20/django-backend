
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'organisation', views.OrganisationViewSet, basename='organisation')
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'dimensions', views.MachineViewset, basename='machine')
# Dynamic URL to get the latest post with an id
# router.register(r'dimensions/<int:id>',views.MachineViewset,basename='MachineInput')
router.register(r'housing', views.HousingViewset, basename='housing')
router.register(r'stator', views.StatorViewset, basename='stator')
router.register(r'rotor', views.RotorViewset, basename='rotor')
router.register(r'loss', views.LossViewset, basename='loss')
router.register(r'winding', views.WindingViewSet, basename='winding')
router.register(r'conductor', views.ConductorViewset, basename='conductor')
router.register(r'slot', views.SlotViewset, basename='slot')
router.register(r'cooling', views.CoolingViewset, basename='cooling')
router.register(r'hole', views.HoleViewset, basename='hole')

urlpatterns = router.urls
