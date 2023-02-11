import sys


def read_input(filename: str):
    try:
        with open(filename, 'r') as input_file:
            file_input = input_file.readlines()
            passengers_array = file_input[0].replace('\n', '').replace(' ', '')
            seats_array = file_input[1].replace('\n', '').replace(' ', '')
            return passengers_array.split(','), seats_array.split(',')
    except FileNotFoundError:
        print('File not found')
    except IndexError:
        print('Incorrect Input Format')
    return [], []


def parse_to_int(passengers_array: list, seats_array: list):
    parsed_passengers_array = [int(passenger) for passenger in passengers_array]
    parsed_seats_array = [int(seat) for seat in seats_array]
    return parsed_passengers_array, parsed_seats_array


def get_output(passengers_array: list, seats_array: list):
    passengers_sum = sum(passengers_array)
    seats_array.sort(reverse=True)
    for bus_index, seat in enumerate(seats_array):
        passengers_sum -= seat
        if passengers_sum <= 0:
            return bus_index + 1
    return 0


passengers, seats = read_input(sys.argv[1])
if not (len(passengers) == 0 and len(seats) == 0):
    passengers, seats = parse_to_int(passengers, seats)
    output = get_output(passengers, seats)
    print(output)
