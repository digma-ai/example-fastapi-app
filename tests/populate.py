import datetime
import time
import requests
from digma.instrumentation.test_tools.helpers import TestHelpers


class DataScenarios:

    def normal_error(self, headers):
        requests.get('http://localhost:8000', headers=headers)

    def multi_ms(self, headers):
        requests.get('http://localhost:8001', headers=headers)

    def double_multi_ms(self, headers):
        requests.get('http://localhost:8002', headers=headers)

    def handled_exception(self, headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5'}, headers=headers)

    def rethrown_exception(self, headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4'}, headers=headers)

    def complex_exception(self, headers):
        requests.get('http://localhost:8000/validate/', params={'user_ids': '2,3,5,4,5'}, headers=headers)

    def unexpected_exception(self, headers):
        requests.get('http://localhost:8000/validateuser/', headers=headers)

    def fast_check(headers):
        requests.get('http://localhost:8001/check/2', headers=headers)

    def normal_check(headers):
        requests.get('http://localhost:8001/check/4', headers=headers)

    def slow_check(headers):
        requests.get('http://localhost:8001/check/6', headers=headers)


def iterate_over_error(function, message, iterations, headers=None):
    if headers == None:
        headers = {}
    print(message)
    for i in range(1, iterations):
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

    #
    # TestHelpers\
    #     .create_errors_over_timespan(scanarios.multi_ms, 'Generating multi-service error', 30,
    #                                      lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
    #                                                                             interval=one_minute,
    #                                                                             iteration=i))
    TestHelpers \
        .create_errors_over_timespan(scanarios.normal_error, 'Generating normal error', 30,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.complex_exception, 'Generating double ms error', 1,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=four_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.normal_error, 'Generating normal error', 2,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=two_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.rethrown_exception, 'Generating rethrown error', 20,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=two_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.rethrown_exception, 'Generating rethrown error', 100,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=one_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))

    TestHelpers \
        .create_errors_over_timespan(scanarios.double_multi_ms, 'Generating double ms error', 80,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=one_days_ago,
                                                                                interval=one_minute,
                                                                                iteration=i))
    TestHelpers \
        .create_errors_over_timespan(scanarios.complex_exception, 'Generating double ms error', 2,
                                     lambda i: TestHelpers.get_timestamp_header(initial_time=one_days_ago,
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
    print('Done generating errors!')


def popuplate_data_for_span_duration_insights():
    TestHelpers.create_errors_over_timespan(
        DataScenarios.slow_check,
        'run_check',
        30,
        lambda i: TestHelpers.get_timestamp_header(initial_time=datetime.timedelta(hours=-1),
                                                   interval=datetime.timedelta(minutes=1),
                                                   iteration=i))

    TestHelpers.create_errors_over_timespan(
        DataScenarios.fast_check,
        'run_check',
        30,
        lambda i: TestHelpers.get_timestamp_header(initial_time=datetime.timedelta(hours=-0.5),
                                                   interval=datetime.timedelta(minutes=1),
                                                   iteration=i))


if __name__ == "__main__":
    popuplate_data()
    # popuplate_data_for_span_duration_insights()
