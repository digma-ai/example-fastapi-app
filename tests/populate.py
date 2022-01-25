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


def popuplate_data():

    scanarios = DataScenarios()
    for i in range(1,3):
        scanarios.normal_error()

    for i in range(1,5):
        scanarios.multi_ms()

    for i in range(1,2):
        scanarios.double_multi_ms()

    for i in range(1,10):
        scanarios.handled_exception()

    for i in range(1,2):
        scanarios.complex_exception()


if __name__ == "__main__":
    popuplate_data()