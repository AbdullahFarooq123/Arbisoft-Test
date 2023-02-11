import sys


def get_output(num_step, merges, buildings, total_floor_per_building):
    outputs = []

    for building_index, building in enumerate(buildings):
        my_floors = 0
        for curr_floor in range(len(building)):
            my_step = 1
            prev_sum = get_prev_sum(building, curr_floor)
            my_merges = 0
            my_floor_unaffected = len(building)
            for next_floor in range(curr_floor + 1, len(building)):
                if prev_sum > building[next_floor] and my_merges < merges:
                    my_floor_unaffected = next_floor
                    my_merges += 1
                prev_sum += building[next_floor]
                my_step += 1
                if my_step >= num_step:
                    break
            my_floors = len(destroy_all_previous_floors(building, len(building) - my_floor_unaffected))
            building = buildings[building_index]
        outputs.append(my_floors)
    print_output(outputs)


def get_prev_sum(building: list, index: int):
    total_sum = 0
    for building_index in range(index + 1):
        total_sum += building[building_index]
    return total_sum


def destroy_all_previous_floors(building: list, floor: int):
    if floor == 0:
        return building
    new_building = []
    prev_sum = 0
    for floor_index, weight in enumerate(building):
        if floor_index <= floor:
            prev_sum += weight
    new_building.append(prev_sum)
    for index in range(floor + 1, len(building)):
        new_building.append(building[index])
    return new_building


def parse_to_int(buildings: list):
    parsed_buildings = []
    for building in buildings:
        int_weights = []
        for weight in building:
            int_weights.append(int(weight))
        parsed_buildings.append(int_weights)
    return parsed_buildings


def transpose(buildings: list, floors: int):
    transpose_matrix = []
    for col in range(len(buildings[0])):
        my_building = []
        for row in range(floors):
            my_building.append(buildings[row][col])
        transpose_matrix.append(my_building)
    return transpose_matrix


def print_output(output_sizes: list):
    for i in range(len(output_sizes)):
        print(output_sizes[i], end='')
        if i < len(output_sizes) - 1:
            print(',', end='')


def read_input(filename: str):
    try:
        with open(filename, 'r') as input_file:
            x = int(input_file.readline().replace('\n', '').replace(' ', ''))
            y = int(input_file.readline().replace('\n', '').replace(' ', ''))
            r = int(input_file.readline().replace('\n', '').replace(' ', ''))
            array = []
            for i in range(r):
                row = input_file.readline().replace('\n', '').replace(' ', '').split(',')
                array.append(row)
            return x, y, r, parse_to_int(array)
    except FileNotFoundError:
        print('File not found')
    except IndexError:
        print('Incorrect Input Format')
    return 0, 0, 0, []


no_of_steps, consecutive_merges, num_floors, buildings_data = read_input(sys.argv[1])
buildings_data = transpose(buildings_data, num_floors)
get_output(no_of_steps, consecutive_merges, buildings_data, num_floors)
