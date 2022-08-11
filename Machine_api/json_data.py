import requests
from jsonmerge import merge

from StatorDimensions_Backend.Machine_api.models import Lamination

r=requests.get("http://127.0.0.1:8000/rotor/")
print(r.json())
housing_data = requests.get("http://127.0.0.1:8000/housing/")
rotor_data = requests.get("http://127.0.0.1:8000/rotor/")
stator_data = requests.get("http://127.0.0.1:8000/stator/")
losses_data = requests.get("http://127.0.0.1:8000/losses/")
cooling_data = requests.get("http://127.0.0.1:8000/cooling/")
machineInput = merge(housing_data,rotor_data,stator_data)
print(machineInput)



def getLaminationData(request):
    data=Lamination.objects.all()
