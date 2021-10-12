# BBas-Django-Backend
### Structure
![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dffd9f91-7a7f-4c1e-93f6-8cd3d93c45b5/Untitled.png)

### DB-Schema
![Blank diagram (1).png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/eeb03c28-53af-4dd1-b878-a3e3b7bb38c8/Blank_diagram_(1).png)

DB-Schema

### API-Schema
- 172.18.3.23:8000/v1/pnsApp/passenger
    
    ## 172.18.3.23:8000/v1/pnsApp/passenger
    
    [GET,PUT,DELETE]
    
    ### GET - parameter
    
    ```json
    {
    	"uid": String(255) (need)
    }
    ```
    
    ```json
    {
    	"success": true, 
    	"result": {
    		"uid": "String",
    		"name": "String",
    		"pushToken": "String",
    	  "pushSetting": Boolean,
    	  "emergencyPhone": "String,
    	  "cityCode": Integer,
    	  "lfBusOption": Boolean
    						}
    }
    ```
    
    ## PUT - parameter
    
    ```json
    {
    	"uid":String(255), (need)
    	"name": String(20), (option)
    	"pushToken": String(255), (option)
    	 "pushSetting": Boolean, default = False, (option)
    	 "emergencyPhone": String(13), (option)
    	 "cityCode": Integer, (option)
    	 "lfBusOption": Boolean, default = False, (option)
    }
    ```
    
    ```json
    {
    	"success": true, 
    	"result": {
    		"uid": "String",
    		"name": "String",
    		"pushToken": "String",
    	  "pushSetting": Boolean,
    	  "emergencyPhone": "String,
    	  "cityCode": Integer,
    	  "lfBusOption": Boolean
    						}
    }
    ```
    
    ## DELETE - parameter
    
    ```json
    {
    	"uid" : String(255) (need)
    }
    ```
    
    ```json
    {
    	"success" : true,
    	"result" : null
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/passengerSign
    
    ## 172.18.3.23:8000/v1/pnsApp/passengerSign
    
    [POST]
    
    ### POST-parameter
    
    ```json
    {
        "uid" : String(255), (need)
        "name" : String(10) (need)
    }
    ```
    
    ```json
    {
        "success": true,
        "result": {
            "uid": "String",
            "name": "String",
            "pushToken": null,
            "pushSetting": false,
            "emergencyPhone": null,
            "cityCode": null,
            "lfBusOption": false
        }
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/driver
    
    ## 172.18.3.23:8000/v1/pnsApp/driver
    
    [GET,PUT,DELETE]
    
    ### GET - parameter
    
    ```json
    {
    	"did": String(255) (need)
    }
    ```
    
    ```json
    {
    	"success": true, 
    	"result": {
    		"did": "String",
    		"name": "String",
    		"pushToken": "String",
    	  "pushSetting": Boolean,
    	  "verified": Boolean,
    	  "vehicleId": "String",
    	  "busRouteId": "String"
    						}
    }
    ```
    
    ## PUT - parameter
    
    ```json
    {
    	"did":String(255), (need)
    	"name": String(20), (option)
    	"pushToken": String(255), (option)
    	 "pushSetting": Boolean, default = False, (option)
    	 "verified": Boolean, default = False, (option)
    	 "vehicleId": String(50), (option)
    	 "busRouteId": String(20), (option)
    }
    ```
    
    ```json
    {
    	"success": true, 
    	"result": {
    		"did": "String",
    		"name": "String",
    		"pushToken": "String",
    	  "pushSetting": Boolean,
    	  "verified": Boolean,
    	  "vehicleId": "String",
    	  "busRouteId": "String"
    						}
    }
    ```
    
    ## DELETE - parameter
    
    ```json
    {
    	"did" : String(255) (need)
    }
    ```
    
    ```json
    {
    	"success" : true,
    	"result" : null
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/driverSign
    
    ## 172.18.3.23:8000/v1/pnsApp/driverSign
    
    [POST]
    
    ### POST-parameter
    
    ```json
    {
        "did" : String(255), (need)
        "name" : String(10) (need)
    }
    ```
    
    ```json
    {
    	"success": true, 
    	"result": {
    		 "did": "String", 
    		 "name": "String", 
    		 "pushToken": null, 
    		 "pushSetting": false, 
    		 "verified": false, 
    		 "vehicleId": null, 
    		 "busRouteId": null
    						}
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/queue/'uid'
    
    ## 172.18.3.23:8000/v1/pnsApp/queue/'uid'
    
    [GET,POST,DELETE]
    
    ### GET
    
    172.18.3.23:8000/v1/pnsApp/queue/uid 값 
    → uid값의 신청 데이터만 반환
    172.18.3.23:8000/v1/pnsApp/queue/0  
    → 전체값 반환
    
    ### POST - parameter
    
    172.18.3.23:8000/v1/pnsApp/queue/0
    
    ```json
    {
        "stbusStopId": String(50),
        "edbusStopId":String(50),
        "vehicleId":String(50),
        "uid":String(255) / passengerAccount에 존재하는 값이여야 합니다.
    		"stNodeOrder":Integer,
    		"edNodeOrder":Integer
    }
    ```
    
    ```json
    {
        "success": true,
        "result": {
            "id": Integer,
            "uid": "String",
            "stbusStopId": "String",
            "edbusStopId": "String",
            "vehicleId": "String",
            "boardingCheck": Boolean,
    				"stNodeOrder" : Integer,
    				"edNodeOrder" : Integer
        }
    }
    ```
    
    ### PUT
    
    ```json
    {   
        "uid":String(255),
        "boardingCheck" : Integer
    }
    ```
    
    ```json
    {
        "success": true,
        "result": {
            "uid": "test",
            "stbusStopId": "JJB381241006",
            "edbusStopId": "JJB381246002",
            "vehicleId": "경남71자5878",
            "boardingCheck": 0,
            "busRouteId": "JJB381012010",
            "stNodeOrder": 40,
            "edNodeOrder": 46
        }
    }
    ```
    
    ### DELETE
    
    172.18.3.23:8000/v1/pnsApp/queue/uid값
    → 빈JSON 값 반환
    {
        "success": true,
        "result": {}
    }
    
- 172.18.3.23:8000/v1/pnsApp/queueInfo
    
    ## 172.18.3.23:8000/v1/pnsApp/queueInfo
    
    [POST]
    
    ### POST
    
    ```json
    {
        "cityCode" : String(20),
        "busRouteId" : String(20),
        "vehicleId": String(50)
    }
    ```
    
    ```json
    Queue에 데이터가 있을 때
    {
        "success": boolean,
        "result" : [
            {
                "stationName" : "String",
                "waiting" : boolean
            }
        ],
        "message"{
            "recentResult" : {
                "stationName" : "String",
                "queueTime" : "String"
            }
        }
    }
    Queue에 데이터가 없을 때
    {
        "success": boolean,
        "result" : [
            {
                "stationName" : "String",
                "waiting" : boolean
            }
        ],
        "message"{}
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/getStationInfo
    
    ## 172.18.3.23:8000/v1/pnsApp/getStationInfo
    
    [POST]
    
    ### POST
    
    ```json
    {
        "gpsLati" : Float,
        "gpsLong" : Float
    }
    ```
    
    ```json
    {
        "success": boolean,
        "result" : {
                "stationName" : "String",
                "distance" : "String", //meter값으로 반환
                "routeData" : [
                    {
                        "lfBus" : "String",
                        "routeNo" : Integer,
                        "destination" : "String"
                    }
                ]           
        }
    }
    ```
    
- 172.18.3.23:8000/v1/pnsApp/rating/'did'
    
    ## 172.18.3.23:8000/v1/pnsApp/rating/'did'
    
    [POST]
    
    ```json
    {
    		"vehicleId": String(50),
    		"ratingData": Double
    }
    ```
    
    ```json
    {
    		"success" : Boolean,
    		"result" : {}
    }
    ```
