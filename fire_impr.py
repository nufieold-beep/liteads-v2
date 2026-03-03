import urllib.request
url = 'http://173.208.137.202:8000/api/v1/event/track?type=impression&req=TEST12345&ad=ad_0_999999&env=ctv&bp=1.5'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    print('Status:', response.status)
