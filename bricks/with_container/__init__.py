# put your python code here
import requests

def ping():
    url = "http://pingpong:8080/ping-pong-api"
    response = requests.get(url)
    return response

def getMetric():
    url = "http://pingpong:8080/ping-pong-api/getMetric"
    response = requests.get(url)
    
    # This converts the JSON response into a Python dictionary
    return response.json()
    