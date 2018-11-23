### Smartcar Backend Coding Challenge

#### Smartcar API

`This API has been developed using the Flask framework. There are two files in this repository`: 

`1. SmartCarAPI.py`

`2. test.py. `

`SmartCarAPI provides the classes where all the API code is written. test.py provides 
tests for the API classes.`


`To use the API, open two terminal tabs.`

`In the first tab, cd into the SmartCar project folder and run _python SmartCarAPI.py_
This will host the SmartCar API on your local host. Get the server url or simply use localhost/ to access specific API's.`

For example:

#### Vehicle Info

##### Request:

_curl http://localhost:5000/vehicles/:1234_

##### Response:

{

    "vin": "123123412412",
    "color": "Metallic Silver",
    "doorCount": 4,
    "driveTrain": "v8"
}

#### Security

##### Request:

_curl http://localhost:5000/vehicles/:1235/doors_

##### Response:

[

    {
        "location": "frontRight",
        "locked": "False"
    },
    {
        "location": "frontLeft",
        "locked": "False"
    }
]

#### Fuel Range

##### Request:

_curl http://localhost:5000/vehicles/:1234/fuel_

##### Response:

{

    "percent": "94.99"
}

#### Battery Range

##### Request:

_curl http://localhost:5000/vehicles/:1235/battery_

##### Response:

{

    "percent": "24.08"
}

#### Start/Stop Engine

##### Request:

_curl http://localhost:5000/vehicles/:1234/engine -X POST -H 'Content-Type: application/json' -d '{"action": "STOP"}'_

##### Response:

{

    "status": "success"
}

##### To run the test file, run _python test.py_ in a terminal. This file has test cases to check bahavior of API when invalid car id is supplied, wrong action etc.
