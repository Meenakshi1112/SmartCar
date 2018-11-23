from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)
base_url = 'http://gmapi.azurewebsites.net/'

class VehicleInfo(Resource):
    def get(self, car_id):
        return_info = {}
        url = '{}getVehicleInfoService'.format(base_url)
        payload = {"id": "{}".format(car_id), "responseType": "JSON"}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        contents = json.loads(r.content)
        if contents["status"] == "200":
            if contents["data"]["fourDoorSedan"]["value"] == "True":
                doorCount = 4
            elif contents["data"]["twoDoorCoupe"]["value"] == "True":
                doorCount = 2
            else:
                doorCount = None
            return_info["vin"] = contents["data"]["vin"]["value"]
            return_info["color"] = contents["data"]["color"]["value"]
            return_info["doorCount"] = doorCount
            return_info["driveTrain"] = contents["data"]["driveTrain"]["value"]
            return return_info
        else:
            return contents  # Returns error message if status code is not 200.

class SecurityInfo(Resource):
    def get(self, car_id):
        return_info = []
        url = '{}getSecurityStatusService'.format(base_url)
        payload = {"id": "{}".format(car_id), "responseType": "JSON"}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        contents = json.loads(r.content)
        if contents["status"] == "200":
            door_list = contents["data"]["doors"]["values"]
            for i in range(0, len(door_list)):
                door = {}
                for key, val in door_list[i].items():
                    door[key] = val["value"]
                return_info.append(door)
            return return_info
        else:
            return contents  # Returns error message if status code is not 200.

class FuelInfo(Resource):
    def get(self, car_id):
        return_info = {}
        url = '{}getEnergyService'.format(base_url)
        payload = {"id": "{}".format(car_id), "responseType": "JSON"}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        contents = json.loads(r.content)
        if contents["status"] == "200":
            fuel_value = contents["data"]["tankLevel"]["value"]
            return_info["percent"] = fuel_value
            return return_info
        else:
            return contents  # Returns error message if status code is not 200.

class BatteryInfo(Resource):
    def get(self, car_id):
        return_info = {}
        url = '{}getEnergyService'.format(base_url)
        payload = {"id": "{}".format(car_id), "responseType": "JSON"}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        contents = json.loads(r.content)
        if contents["status"] == "200":
            fuel_value = contents["data"]["batteryLevel"]["value"]
            return_info["percent"] = fuel_value
            return return_info
        else:
            return contents  # Returns error message if status code is not 200.

class StartStopEngine(Resource):
    def post(self, car_id):
        return_dict = {}
        data_sent = request.get_json()
        if "action" in data_sent:
            command = data_sent["action"]
            if command == "START":
                request_command = "START_VEHICLE"
            elif command == "STOP":
                request_command = "STOP_VEHICLE"
            else:
                request_command = None
        else:
            return "action key not present"

        url = '{}actionEngineService'.format(base_url)
        payload = {"id": "{}".format(car_id), "command": request_command, "responseType": "JSON"}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        contents = json.loads(r.content)
        if contents["status"] == "200":
            if contents["actionResult"]["status"] == "FAILED":
                return_dict["status"] = "success"
            elif contents["actionResult"]["status"] == "EXECUTED":
                return_dict["status"] = "error"
            return return_dict
        else:
            return contents # Returns error message if status code is not 200.

api.add_resource(VehicleInfo, '/vehicles/:<int:car_id>')
api.add_resource(SecurityInfo, '/vehicles/:<int:car_id>/doors')
api.add_resource(FuelInfo, '/vehicles/:<int:car_id>/fuel')
api.add_resource(BatteryInfo, '/vehicles/:<int:car_id>/battery')
api.add_resource(StartStopEngine, '/vehicles/:<int:car_id>/engine')

if __name__ == '__main__':
    app.run(debug=True)