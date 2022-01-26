import time
import requests


class DataScenarios:

    def normal_error(self):
        requests.get('http://localhost:8000')

    def multi_ms(self):
        requests.get('http://localhost:8001')

    def double_multi_ms(self):
        requests.get('http://localhost:8002')

    def handled_exception(self):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5'})

    def rethrown_exception(self):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4'})

    def complex_exception(self):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4,5'})

    def unexpected_exception(self):
        requests.get('http://localhost:8000/validateuser/')

def iterate_over_error(function, message, iterations):
    print(message)
    for i in range(1,iterations):
        print(f"iteration {i}", end='\r', flush=True)
        function()
        time.sleep(0.2)
    print("\n")

def popuplate_data():
    scanarios = DataScenarios()

    iterate_over_error(scanarios.normal_error, 'Generating normal error', 5)
    iterate_over_error(scanarios.unexpected_exception, 'Generating unexpected error', 10)
    iterate_over_error(scanarios.rethrown_exception, 'Generating unexpected error', 20)
    iterate_over_error(scanarios.multi_ms, 'Generating multi_ms error', 3)
    iterate_over_error(scanarios.double_multi_ms, 'Generating double_multi_ms error', 3)
    iterate_over_error(scanarios.handled_exception, 'Generating handled_exception error', 5)
    iterate_over_error(scanarios.complex_exception, 'Generating complex error', 1)
    print ('Done generating errors!')

if __name__ == "__main__":
    popuplate_data()