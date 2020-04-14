import requests

message = {'mqtt_key': '123', 'user': 'sinegordon', 'language': 'python3', 'course': 'Numerical analysis', 
            'problem': '1', 'variant': '6', 'code': 'print(input())'}
resp = requests.post('http://localhost:8000/add_transaction', json=message)
print(resp.json())