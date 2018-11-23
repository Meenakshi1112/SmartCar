from SmartCarAPI import app
import unittest
import json

# Tests various status codes of API


class ApiTestsStatusCodes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_vehicleAPI_status_code(self):
        result = self.app.get('/vehicles/:1234')
        self.assertEqual(result.status_code, 200)

    def test_security_status_code(self):
        result = self.app.get('/vehicles/:1234/doors')
        self.assertEqual(result.status_code, 200)

    def test_fuel_status_code(self):
        result = self.app.get('/vehicles/:1234/fuel')
        self.assertEqual(result.status_code, 200)

    def test_battery_status_code(self):
        result = self.app.get('/vehicles/:1234/battery')
        self.assertEqual(result.status_code, 200)

    def test_engine_status_code(self):
        data = {"action": "STOP"}
        result = self.app.post('/vehicles/:1234/engine', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(result.status_code, 200)

    #Invalid Link with status code 404.
    def test_security_status_code_400(self):
        result = self.app.get('/vehicles/:1234/invalidlink')
        self.assertEqual(result.status_code, 404)

# Tests various reponse messages of API


class ApiTestsContents(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_vehicleAPI_content(self):
        data = {"vin": "123123412412", "color": "Metallic Silver", "doorCount": 4, "driveTrain": "v8"}
        result = self.app.get('/vehicles/:1234')
        self.assertEqual(json.loads(result.get_data()), data)

    def test_securityAPI_content(self):
        result_4door = self.app.get('/vehicles/:1234/doors')
        self.assertAlmostEqual(len(json.loads(result_4door.get_data())), 4)
        result_2door = self.app.get('/vehicles/:1235/doors')
        self.assertAlmostEqual(len(json.loads(result_2door.get_data())), 2)

    def test_fuel_content(self):
        result = self.app.get('/vehicles/:1234/fuel')
        assert 'percent' in (json.loads(result.get_data()))

    def test_battery_content(self):
        result = self.app.get('/vehicles/:1234/battery')
        assert 'percent' in (json.loads(result.get_data()))

    #invalid car number
    def test_invalid_car(self):
        error = {"status": "404", "reason": "Vehicle id: 123455 not found."}
        result = self.app.get('/vehicles/:123455')
        self.assertEqual(json.loads(result.get_data()), error)

    #invalid keyword
    def test_invalid_post(self):
        data = {"action_invalid": "STOP"}
        result = self.app.post('/vehicles/:1234/engine', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(json.loads(result.get_data()), "action key not present")
        data = {"action": "STOP_INVALID"}
        result = self.app.post('/vehicles/:1234/engine', data=json.dumps(data),
                               content_type='application/json')
        error_message = {"status": "400", "reason": "Unknown command: null"}
        self.assertEqual(json.loads(result.get_data()), error_message)


if __name__ == "__main__":
    unittest.main()