import json
import sys
from json import JSONDecodeError

import requests

rides_url = 'https://www.jsonkeeper.com/b/DM5F'
payments_url = 'https://www.jsonkeeper.com/b/9QRZ'


class Date:
    def __init__(self, date: str):
        date_separate = date.replace(' ', '').split('/')
        self.date = int(date_separate[1])
        self.month = int(date_separate[0])
        self.year = int(date_separate[2])

    def __str__(self):
        return '{:02d}/{:02d}/{:02d}'.format(self.date, self.month, self.year)


class Trip:
    def __init__(self, trip_date: Date, fare: float):
        self.trip_date = trip_date
        self.fare = fare

    def __str__(self):
        return self.trip_date.__str__() + ',' + str(self.fare)


class Payments:
    def __init__(self, amount_paid: float, payment_date: Date):
        self.amount_paid = amount_paid
        self.payment_date = payment_date

    def __str__(self):
        return self.payment_date.__str__() + ',' + str(self.amount_paid)


class Driver:
    def __init__(self, driver_id: str, joining_date: str):
        self.driver_id = driver_id
        self.joining_date = Date(joining_date)
        self.record = {}

    def set_info(self, payments: list, trips: list):
        self.record = {
            'payments': payments,
            'trips': trips
        }

    def __str__(self):
        return self.driver_id + ',' + self.joining_date.__str__()


def read_input(filename: str) -> list:
    try:
        with open(filename, 'r') as input_file:
            drivers_info = []
            no_of_inputs = int(input_file.readline())
            for i in range(no_of_inputs):
                temp_driver = get_driver(input_file.readline())
                drivers_info.append(temp_driver)
            return drivers_info
    except FileNotFoundError:
        print('File not found')
    except IndexError:
        print('Incorrect Input Format')
    return []


def get_driver(input_line: str) -> Driver:
    valid_input_line = input_line.replace('\n', '').replace(' ', '')
    driver_id = valid_input_line.split(',')[0]
    joining_date = valid_input_line.split(',')[1]
    return Driver(driver_id, joining_date)


def get_trips(driver_id: int, rides: dict):
    trips = []
    for ride_info in rides:
        if ride_info['driver_id'] == driver_id:
            trip_date = Date(ride_info['trip_date'])
            trip_fare = ride_info['trip_details']['fare']
            trips.append(Trip(trip_date, trip_fare))
    return trips


def get_payments(driver_id: int, payments: dict):
    trips = []
    for payment in payments:
        if payment['driver_id'] == driver_id:
            payment_date = Date(payment['date'])
            payment_amount = payment['amount']
            trips.append(Payments(payment_amount, payment_date))
    return trips


def calculate_payment_for_driver(driver_: Driver):
    payment_sum, percent_paid = 0, 0
    for trip in driver_.record['trips']:
        if trip.trip_date.month == driver_.joining_date.month + 1:
            percent_paid += trip.fare * 10 / 100
        elif trip.trip_date.month > driver_.joining_date.month + 1:
            percent_paid += trip.fare * 20 / 100
    for payment in driver_.record['payments']:
        payment_sum += payment.amount_paid
    return round(payment_sum - percent_paid, 1)


try:
    rides_response = requests.get(rides_url).json()
    payments_response = requests.get(payments_url).json()
    drivers = read_input(sys.argv[1])
    if not (len(drivers) == 0):
        for driver in drivers:
            driver_trips = get_trips(int(driver.driver_id), rides_response)
            driver_payments = get_payments(int(driver.driver_id), payments_response)
            driver.set_info(driver_payments, driver_trips)
            print(calculate_payment_for_driver(driver))
except JSONDecodeError:
    print('Json Response Error')
