import datetime
import time
import requests

from test_instrumentation import TestHelpers


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
        time.sleep(0.5)
    print("\n")


def popuplate_data():
    scanarios = DataScenarios()
    seven_days_ago = datetime.timedelta(days=-7)

    one_days_ago = datetime.timedelta(days=-1)

    two_days_ago = datetime.timedelta(days=-2)
    four_days_ago = datetime.timedelta(days=-4)
    one_minute = datetime.timedelta(minutes=1)
    one_hour = datetime.timedelta(hours=1)
    one_day = datetime.timedelta(days=1)



    TestHelpers\
        .create_errors_over_timespan(scanarios.multi_ms, 'Generating multi-service error', 100,
                                         lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))
    TestHelpers\
        .create_errors_over_timespan(scanarios.normal_error, 'Generating normal error', 20,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
                                                                                interval=one_hour,
                                                                                iteration=i))

    TestHelpers\
        .create_errors_over_timespan(scanarios.normal_error, 'Generating normal error', 2000,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=two_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))
    TestHelpers\
        .create_errors_over_timespan(scanarios.complex_exception, 'Generating complex error', 7,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=seven_days_ago,
                                                                                interval=one_day,
                                                                                iteration=i))
    TestHelpers \
        .create_errors_over_timespan(scanarios.rethrown_exception, 'Generating rethrown error', 100,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=two_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.rethrown_exception, 'Generating rethrown error', 1000,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=one_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.double_multi_ms, 'Generating double ms error', 200,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    # create_errors_over_timespan(scanarios.multi_ms, 'Generating normal error', 50,
    #                             lambda i: get_timestamp_header(initial_time=four_days_ago,
    #                                                            interval=one_hour,
    #                                                            iteration=i))
    #         # iterate_over_error(scanarios.unexpected_exception, 'Generating unexpected error', 10)
    # iterate_over_error(scanarios.rethrown_exception, 'Generating unexpected error', 30)
    # iterate_over_error(scanarios.multi_ms, 'Generating multi_ms error', 3)
    # iterate_over_error(scanarios.double_multi_ms, 'Generating double_multi_ms error', 3)
    # iterate_over_error(scanarios.handled_exception, 'Generating handled_exception error', 5)
    # iterate_over_error(scanarios.complex_exception, 'Generating complex error', 1)
    print ('Done generating errors!')

if __name__ == "__main__":
    popuplate_data()