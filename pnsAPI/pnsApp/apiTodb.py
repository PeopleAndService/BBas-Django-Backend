from django.http import response
import requests
from .serializers import nodeSerializer

def insert_nextStation():
    cityCode = ["38010","38030","38050","38070","38080","38090","38100","38310","38320","38330","38340","38350","38360","38370","38380","38390","38400"]
    for code in cityCode:
        call_getSttnNoList(cityCode=code)


def call_getSttnNoList(cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/BusSttnInfoInqireService/getSttnNoList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&numOfRows=999&cityCode="+str(cityCode)
    req = requests.get(url)
    res = req.json()
    items = res['response']['body']['items']['item']
    for i in items:
        call_getSttnAcctoArvlPrearngeInfoList(cityCode=cityCode, nodeId=i['nodeId'] )


def call_getSttnAcctoArvlPrearngeInfoList(nodeId, cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&cityCode="+cityCode +"&nodeId="+nodeId
    req = requests.get(url)
    res = req.json()
    item = res['response']['body']['items']['item'][0]['routeid']
    call_getRouteAcctoThrghSttnList(nodeId=nodeId, routeId=item)


def call_getRouteAcctoThrghSttnList(nodeId, routeId, cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteAcctoThrghSttnList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&cityCode="+cityCode+"&routeId="+routeId+"&numOfRows=1000&pageNo=1"
    req = requests.get(url)
    res = req.json()
    item = res['response']['body']['items']['item']
    filteredItem = ""
    for i in range(len(item)):
        if item[i]['nodeid'] == nodeId :
            filteredItem = item[i+1]['nodenm']
    print(filteredItem)
    insert_API_DATA(nodeid=nodeId, cityCode=cityCode, nextStation=filteredItem)        
    

def insert_API_DATA(cityCode, nodeid, nextStation):
    dataa = {'cityCode' : cityCode, 'nodeid' : nodeid, 'nextStation': nextStation}

    serializers = nodeSerializer(data=dataa)
    if serializers.is_valid():
        serializers.save()
    else:
        print(serializers.errors)


if __name__ == '__main__':
    insert_nextStation()

'''
getSttnNoList 으로 nodeid 반환
'''
'''
updowncd = 0 - 상행
그 다음 순서 
updowncd = 1 - 하행
'''
'''
getSttnAcctoArvlPrearngeInfoList 여기서 routeID 반환
'''

'''
getRouteAcctoThrghSttnList nodeId를 필터로 사용해서 다음 순번을 찾아서 정류소명 반환
'''
# 그 다음 nodeid, cityCode, nextStation을 저장

'''
    id                      = models.AutoField(primary_key=True)
    cityCode                = IntegerField(null=False)
    nodeid                  = CharField(max_length=20 ,null=False)
    nextStation             = CharField(max_length=20, null=False)
'''
'''

<citycode>38010</citycode>
<cityname>창원시</cityname>
</item>
<item>
<citycode>38030</citycode>
<cityname>진주시</cityname>
</item>
<item>
<citycode>38050</citycode>
<cityname>통영시</cityname>
</item>
<item>
<citycode>38070</citycode>
<cityname>김해시</cityname>
</item>
<item>
<citycode>38080</citycode>
<cityname>밀양시</cityname>
</item>
<item>
<citycode>38090</citycode>
<cityname>거제시</cityname>
</item>
<item>
<citycode>38100</citycode>
<cityname>양산시</cityname>
</item>
<item>
<citycode>38310</citycode>
<cityname>의령군</cityname>
</item>
<item>
<citycode>38320</citycode>
<cityname>함안군</cityname>
</item>
<item>
<citycode>38330</citycode>
<cityname>창녕군</cityname>
</item>
<item>
<citycode>38340</citycode>
<cityname>고성군</cityname>
</item>
<item>
<citycode>38350</citycode>
<cityname>남해군</cityname>
</item>
<item>
<citycode>38360</citycode>
<cityname>하동군</cityname>
</item>
<item>
<citycode>38370</citycode>
<cityname>산청군</cityname>
</item>
<item>
<citycode>38380</citycode>
<cityname>함양군</cityname>
</item>
<item>
<citycode>38390</citycode>
<cityname>거창군</cityname>
</item>
<item>
<citycode>38400</citycode>
<cityname>합천군</cityname>
'''