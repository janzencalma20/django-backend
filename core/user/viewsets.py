
from core.user.serializers import UserSerializer
from core.user.models import CohereUser
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CohereUser.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = CohereUser.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj
