import traceback
import glob
import json
import os

from celery import current_app
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action

from django.http import JsonResponse
from django.conf import settings

from .serializers import *
from .models import *
from utils.plot import create_axial_slice
from .tasks import lptn_solve_task, lptn_results_task


class OrganisationViewSet(ModelViewSet):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.order_by('-id').all()

    @action(detail=True, methods=['GET'])
    def get_org_projects(self, request, pk=None):
        organisation = self.get_object()
        get_org_projects_serializer = GetOrgProjectsSerializer(organisation)
        return Response(get_org_projects_serializer.data)


class ProjectViewSet(ModelViewSet):
    serializer_class = CreateProjectSerializer
    queryset = Project.objects.order_by('-id').all()

    def create(self, request, *args, **kwargs):
        org_id = self.request.data.get('organisation')
        data = self.request.data
        data['owner'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()

        project = Project.objects.get(id=serializer.data['id'])
        org = Organisation.objects.get(id=org_id)
        org.projects.add(project)

        get_project_serializer = GetProjectSerializer(project)
        return Response(get_project_serializer.data)


class UserViewSet(ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.order_by('-id').all()

    @action(detail=False, methods=['PUT'])
    def change_password(self, request):
        user_id = self.request.data.get('id')
        new_password = self.request.data.get('new_password')

        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            return JsonResponse('success', safe=False)
        except User.DoesNotExist:
            return JsonResponse('failure', safe=False)


class MachineViewset(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.order_by('-id').all()

    def create(self, request, *args, **kwargs):
        coming_data = request.data
        serializer = self.serializer_class(data=coming_data)
        serializer.is_valid()
        serializer.save()

        new_machine = Machine.objects.get(id=serializer.data['id'])
        get_machine_serializer = GetMachineSerializer(new_machine)
        return Response(get_machine_serializer.data)

    @action(detail=False, methods=['GET'], url_path="project/(?P<project_id>[^/.]+)/get_machines")
    def get_all(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        machines = Machine.objects.filter(project_id=project_id)
        get_machines_serializer = GetMachineSerializer(machines, many=True)
        return Response(get_machines_serializer.data)

    @action(detail=False, methods=['POST'], url_path="projects/get-machines")
    def get_projects_machines(self, request, *args, **kwargs):
        project_ids = request.data.get('project_ids')
        machines = Machine.objects.filter(project_id__in=project_ids)
        get_machines_serializer = GetMachineSerializer(machines, many=True)
        return Response(get_machines_serializer.data)

    @action(detail=True, methods=['GET'])
    def total(self, request, pk=None):
        machine = self.get_object()
        serializer = GetMachineSerializer(machine)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'POST'])
    def get_housing_type(self, request, pk=None):
        housingType = Housing.objects.values('type').get(id=pk)['type']
        return JsonResponse(housingType, safe=False)

    @action(detail=False, methods=['GET'])
    def list_total(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        qs = super().get_queryset()
        res_dict = {}
        for machine in qs:
            res_dict[machine.id] = GetMachineSerializer(machine).data
        return JsonResponse(res_dict)

    @action(detail=False, methods=['GET', 'POST'])
    def get_slot_type(self, request, pk=None):
        slotType = Slot.objects.values('type')
        return JsonResponse(slotType, safe=False)

    @action(detail=False, methods=['GET', 'POST'])
    def get_conductor_type(self, request, pk=None):
        conductorType = Conductor.objects.values('type').get(id=pk)['type']
        return JsonResponse(conductorType, safe=False)

    @action(detail=True, methods=['GET', 'POST'])
    def lptn_solve(self, request, pk=None):
        """Dummy: Solves LPTN model"""
        res = {}
        task = lptn_solve_task.delay()
        res['task_id'] = task.id
        res['task_status'] = task.status
        return JsonResponse(res)

    @action(detail=False, methods=['GET'], url_path="(?P<machine_id>[^/.]+)/lptn_solve_task/(?P<task_id>[^/.]+)")
    def get_lptn_solve_task(self, request, *args, **kwargs):
        machine_id = int(kwargs.get('machine_id'))
        task_id = kwargs.get('task_id')
        task = current_app.AsyncResult(task_id)
        response_data = {'task_id': task.id, 'task_status': task.status}

        if task.status == 'SUCCESS':
            result = task.get()
            response_data['result'] = result

            machine = Machine.objects.get(id=machine_id)
            if machine.lptn_id:  # LPTN result update
                lptn = LPTN.objects.get(id=machine.lptn_id)
                lptn.result = result
                lptn.save()
            else:  # LPTN result insert
                lptn_serializer = CreateLPTNSerializer
                data = {
                    'result': task.get()
                }
                serializer = lptn_serializer(data=data)
                serializer.is_valid()
                serializer.save()

                machine.lptn_id = serializer.data['id']
                machine.save()
            # execute lptn_results_task
            lptn_results_task.delay(machine_id)

        return JsonResponse(response_data)

    @action(detail=False, methods=['GET'], url_path="(?P<machine_id>[^/.]+)/get_result")
    def get_machine_result(self, request, *args, **kwargs):
        machine_id = int(kwargs.get('machine_id'))
        machine = Machine.objects.get(id=machine_id)

        if machine.lptn_id:
            return JsonResponse(machine.lptn.result)
        else:
            return JsonResponse(None, safe=False)

        # try:
        #     lptn = LPTN.objects.get(machine=machine_id)
        #     return JsonResponse(lptn.result)
        # except LPTN.DoesNotExist:
        #     return JsonResponse(None, safe=False)

    @action(detail=True, methods=['GET', 'POST'])
    def get_rotor_type(self, request, pk=None):
        rotorType = Rotor.objects.values('type').get(id=pk)['type']
        return JsonResponse(rotorType, safe=False)

    @action(detail=True)
    def create_machine_image(self, request, pk=None):
        """
        Checks if machine input is valid and generates 2D axial view of machine

        Parameters
        ----------
        request: HttpRequest

        Returns
        -------
        response: JsonResponse
            Contains S3 image location, validity of machine dimensions, error msg (optional)
        """
        # Convert HttpRequest to json
        machine = self.get_object()
        data = GetMachineSerializer(machine).data
        # res_dict = {"error": None}
        res_dict = {"machine": data,
                    "error": None}

        # #Debug
        # machine_json = json.dumps(data, indent=4, sort_keys=True)
        # os.makedirs('Debug', exist_ok=True)
        # with open(os.path.join("Debug", "machine.json"), 'w') as file:
        #     file.write(machine_json)

        res_status = 200
        # Create image
        try:
            img_dict = create_axial_slice(data)
            # if not img_dict["valid_machine"]:
            #     res_status = 400
            res_dict.update(img_dict)
            response = JsonResponse(res_dict, status=res_status)
        except Exception as err:
            if settings.DEBUG:
                err = traceback.format_exc()
            res_dict["error"] = str(err)
            response = JsonResponse(res_dict, status=res_status)
        return response

    @action(detail=False, methods=['GET'])
    def get_materials(self, request, *args, **kwargs):
        files = glob.glob('Machine_api/Materials/*', recursive=True)
        response = {}

        for single_file in files:
            with open(single_file, 'r') as file:
                try:
                    materials = []
                    data = json.load(file)
                    file_name = os.path.basename(file.name)
                    response_key = file_name.split('.')[0]
                    if response_key == 'AWG' or response_key == 'SWG':
                        keys = [int(key) for key in data.keys()]
                        for k in keys:
                            materials.append(k)
                    else:
                        for key in data.keys():
                            materials.append(key)
                    response[response_key] = list(set(materials))
                except KeyError:
                    print(f'Skipping {single_file}')

        return JsonResponse(response, safe=False)

    @action(detail=False, methods=['POST'])
    def get_material_dict(self, request, *args, **kwargs):
        filename = request.data.get('filename')
        material = request.data.get('material')

        with open('Machine_api/Materials/{}.json'.format(filename)) as file:
            data = json.load(file)
            response = {
                'Thermal Conductivity': float(data[material].get('Thermal Conductivity')),
                'Specific Heat': float(data[material].get('Specific Heat')),
                'Density': float(data[material].get('Density'))
            }

        return JsonResponse(response, safe=False)


class ResultsViewset(ModelViewSet):
    serializer_class = ResultsSerializer
    queryset = Results.objects.order_by('-id').all()


class HousingViewset(ModelViewSet):
    serializer_class = HousingSerializer
    queryset = Housing.objects.order_by('-id').all()
    @action(detail=True, methods=['GET', 'POST'])
    def total(self, request, pk=None):
        housing = self.get_object()
        housingSerializer = CompleteHousingSerializer(housing)
        return Response(housingSerializer.data)


class StatorViewset(ModelViewSet):
    serializer_class = StatorSerializer
    queryset = Stator.objects.order_by('-id').all()
    @action(detail=True, methods=['GET', 'POST'])
    def total(self, request, pk=None):
        stator = self.get_object()
        stator_serializer = CompleteStatorSerializer(stator)
        return Response(stator_serializer.data)


class RotorViewset(ModelViewSet):
    serializer_class = RotorSerializer
    queryset = Rotor.objects.order_by('-id').all()
    @action(detail=True, methods=['GET', 'POST'])
    def total(self, request, pk=None):
        rotor = self.get_object()
        rotor_serializer = CompleteRotorSerializer(rotor)
        return Response(rotor_serializer.data)


class CoolingViewset(ModelViewSet):
    serializer_class = CoolingSerializer
    queryset = Cooling.objects.order_by('-id').all()
    @action(detail=True, methods=['GET', 'POST'])
    def total(self, request, pk=None):
        cooling = self.get_object()
        cooling_serializer = CompleteCoolingSerializer(cooling)
        return Response(cooling_serializer.data)


class HoleViewset(ModelViewSet):
    serializer_class = HoleSerializer
    queryset = Hole.objects.order_by('-id').all()


class LossViewset(ModelViewSet):
    serializer_class = LossSerializer
    queryset = Loss.objects.all()


class WindingViewSet(ModelViewSet):
    serializer_class = WindingSerializer
    queryset = Winding.objects.order_by('-id').all()


class ConductorViewset(ModelViewSet):
    serializer_class = ConductorSerializer
    queryset = Conductor.objects.order_by('-id').all()


class SlotViewset(ModelViewSet):
    serializer_class = SlotSerializer
    queryset = Slot.objects.order_by('-id').all()


