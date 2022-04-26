import requests as requests

for i in range(50):
   res = requests.get('http://localhost:8000/delay/0.2')
   res = requests.get('http://localhost:8000/delay/0.15')

for i in range(100):
   res = requests.get('http://localhost:8000/delay400')


