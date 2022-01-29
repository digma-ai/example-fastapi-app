import datetime
import time
import requests


class DataScenarios:

    def normal_error(self, headers):
        requests.get('http://localhost:8000', headers=headers)

    def multi_ms(self,headers):
        requests.get('http://localhost:8001', headers=headers)

    def double_multi_ms(self, headers):
        requests.get('http://localhost:8002', headers=headers)

    def handled_exception(self,headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5'}, headers=headers)

    def rethrown_exception(self,headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4'}, headers=headers)

    def complex_exception(self, headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4,5'}, headers=headers)

    def unexpected_exception(self, headers):
        requests.get('http://localhost:8000/validateuser/', headers=headers)

def iterate_over_error(function, message, iterations, headers=None):
    if headers==None:
        headers={}
    print(message)
    for i in range(1,iterations):
        print(f"iteration {i}", end='\r', flush=True)
        function(headers)
        time.sleep(0.2)
    print("\n")

def get_timestamp_header(delta : datetime.timedelta):
    new_time = datetime.datetime.now() + delta
    timestamp = str(int(datetime.datetime.timestamp(new_time)) * 1000000000)
    return {'x-simulated-time' : timestamp}

def popuplate_data():
    scanarios = DataScenarios()

    four_days_ago = datetime.timedelta(days=-4)
    iterate_over_error(scanarios.normal_error, 'Generating normal error', 5, headers=get_timestamp_header(four_days_ago))
    iterate_over_error(scanarios.unexpected_exception, 'Generating unexpected error', 10)
    iterate_over_error(scanarios.rethrown_exception, 'Generating unexpected error', 30)
    iterate_over_error(scanarios.multi_ms, 'Generating multi_ms error', 3)
    iterate_over_error(scanarios.double_multi_ms, 'Generating double_multi_ms error', 3)
    iterate_over_error(scanarios.handled_exception, 'Generating handled_exception error', 5)
    iterate_over_error(scanarios.complex_exception, 'Generating complex error', 1)
    print ('Done generating errors!')

if __name__ == "__main__":
    popuplate_data()