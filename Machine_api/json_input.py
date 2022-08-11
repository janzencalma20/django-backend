import json
from rest_framework.decorators import api_view
# store the URL in url as
# parameter for urlopen
from urllib.request import urlopen

url = "http://127.0.0.1:8000/api/machine/dimensions/1/totalMachineInputs"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

# print the json response
print(data_json)

@api_view(['GET'])
def getMachines(request, pk, machines=None):
    machine=None
    for i in machines:
        if i['_id']==pk:
            machine=i
            break