from rest_framework import serializers
from .models import *
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class GetProjectSerializer(serializers.ModelSerializer):
    owner = UserCreateSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class HousingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = '__all__'


class RotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rotor
        fields = '__all__'


class StatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stator
        fields = '__all__'


class CoolingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooling
        fields = '__all__'


class LossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loss
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class WindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winding
        fields = '__all__'


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'


class HoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hole
        fields = '__all__'


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


class CreateLPTNSerializer(serializers.ModelSerializer):
    class Meta:
        model = LPTN
        fields = '__all__'


class CompleteOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class GetOrgProjectsSerializer(serializers.ModelSerializer):
    projects = GetProjectSerializer(allow_null=True, read_only=True, many=True)

    class Meta:
        model = Project
        fields = ['projects']


class CompleteRotorSerializer(serializers.ModelSerializer):
    slot = SlotSerializer(allow_null=True, read_only=True)
    winding = WindingSerializer(allow_null=True, read_only=True)
    conductor = ConductorSerializer(allow_null=True, read_only=True)
    hole = HoleSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Rotor
        fields = '__all__'


class CompleteStatorSerializer(serializers.ModelSerializer):
    slot = SlotSerializer(allow_null=True, read_only=True)
    winding = WindingSerializer(allow_null=True, read_only=True)
    conductor = ConductorSerializer(allow_null=True, read_only=True)
    hole = HoleSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Stator
        fields = '__all__'


class CompleteHousingSerializer(serializers.ModelSerializer):
    housing = HousingSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Housing
        fields = '__all__'


class CompleteSlotSerializer(serializers.ModelSerializer):
    slot = SlotSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Slot
        fields = '__all__'


class CompleteConductorSerializer(serializers.ModelSerializer):
    conductor = ConductorSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Conductor
        fields = '__all__'


class CompleteCoolingSerializer(serializers.ModelSerializer):
    cooling = CoolingSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Cooling
        fields = '__all__'


class CompleteLossSerializer(serializers.ModelSerializer):
    loss = LossSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Loss
        fields = '__all__'


class GetLPTNSerializer(serializers.ModelSerializer):
    class Meta:
        model = LPTN
        fields = '__all__'


class GetMachineSerializer(serializers.ModelSerializer):
    project = GetProjectSerializer(allow_null=True, read_only=True)
    stator = CompleteStatorSerializer(allow_null=True, read_only=True)
    rotor = CompleteRotorSerializer(allow_null=True, read_only=True)
    housing = CompleteHousingSerializer(allow_null=True, read_only=True)
    cooling = CompleteCoolingSerializer(allow_null=True, read_only=True)
    loss = CompleteLossSerializer(allow_null=True, read_only=True)
    lptn = GetLPTNSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Machine
        fields = '__all__'
