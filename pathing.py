import data
from random import random, choice


class Individual:
    def __init__(self, stations, time, lines, fitness=0, transfer_time=0):
        self.stations = stations
        self.time = time
        self.transfer_time = transfer_time
        self.lines = lines
        self.fitness = fitness

    def __eq__(self, other):
        return self.stations == other.stations


class Hour:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __add__(self, other):
        minute_res = other + self.minute
        hour_add = 0
        if minute_res > 59:
            hour_add = int(minute_res / 60)
            minute_res = minute_res % 60
        hour_res = self.hour + hour_add
        if hour_res > 23:
            hour_res = hour_res % 24
        return Hour(hour_res, minute_res)

    def __sub__(self, other):
        minute_res = self.minute - other
        hour_sub = 0
        if minute_res < 0:
            hour_sub = int(minute_res / 60) * (-1)
            minute_res = minute_res % 60
        hour_res = self.hour - hour_sub - 1
        if hour_res < 0:
            hour_res = hour_res + 24
        return Hour(hour_res, minute_res)


metro_map = data.get_map()

metro_times = data.get_times()

colors = ["Red", "Black", "Blue", "Yellow", "Brown", "Gray", "Green", "Orange", "Purple", "Pink"]


def add_time(forward, time, station):
    if forward:
        time.append(station.forthTime)
    else:
        time.append(station.backTime)
    return time


def check_end_line(station, forward):
    if (forward and station.forthTime == 0) or (not forward and station.backTime == 0):
        forward = not forward
    return forward


def get_line_and_index(connections, station_name):
    # Gets 1 random line from all available
    current_line = metro_map[choice(connections)]
    # Gets index of the station on the current line
    index = data.get_station_index(current_line, station_name)
    return [current_line, index]


def get_line_changes(lines):
    if lines is None:
        return None
    changes = 0
    line = lines[0]
    for i in range(1, len(lines)):
        if line != lines[i]:
            changes += 1
        line = lines[i]
    return changes


def get_departure_minute(time, interval, interval_index, line_index, index):
    shift = 0
    if isinstance(interval, (list,)):
        [real_interval, shift] = interval
    else:
        real_interval = interval

    if real_interval is False:
        index = index + 1
        if index == 24:
            index = 0
        return get_departure_minute(time, metro_times[line_index][index][interval_index], interval_index,
                                    line_index, index) + 60
    if real_interval == 0:
        if index > time.hour or index < 4:
            return 0 + shift
        else:
            index = index + 1
            if index == 24:
                index = 0
            return get_departure_minute(time, metro_times[line_index][index][interval_index], interval_index,
                                        line_index, index) + 60
    limit = 60 / real_interval - 1
    value = (time.minute - shift) / real_interval
    if value == limit:
        if ((time.minute - shift) % real_interval) != 0:
            index = index + 1
            if index == 24:
                index = 0
            return get_departure_minute(time, metro_times[line_index][index][interval_index], interval_index,
                                        line_index, index) + 60
        else:
            return (int(value)) * real_interval + shift
    if ((time.minute - shift) % real_interval) != 0:
        return (int(value) + 1) * real_interval + shift
    else:
        return (int(value)) * real_interval + shift


def auxiliary_transfer_time(individual, initial_time, transfer_time, index):

    [first_station, second_station] = individual.stations[index:index+2]
    line_index = colors.index(individual.lines[index])
    first_line = metro_map[line_index]

    auxiliary_time = initial_time + (sum(individual.time[:index]) + transfer_time)

    station_index = data.get_station_index(first_line, first_station)

    # Goes forward, we have to look for previous stations
    if station_index < data.get_station_index(first_line, second_station):
        interval_index = 0
        while station_index != 0:
            auxiliary_time -= first_line[station_index].backTime
            station_index -= 1
    # Goes backwards, we have to look for next stations
    else:
        interval_index = 1
        while station_index != len(first_line):
            auxiliary_time -= first_line[station_index].forthTime
            station_index += 1

    return [auxiliary_time, line_index, interval_index]


def get_transfer_time(individual, initial_time):

    transfer_time = 0

    [auxiliary_time, line_index, interval_index] = auxiliary_transfer_time(individual, initial_time,
                                                                           transfer_time, 0)

    interval = metro_times[line_index][auxiliary_time.hour][interval_index]
    departure_minute = get_departure_minute(auxiliary_time, interval, interval_index, line_index,
                                            auxiliary_time.hour)

    transfer_time += departure_minute - auxiliary_time.minute

    for i in range(1, len(individual.lines)):

        if individual.lines[i-1] != individual.lines[i]:

            [auxiliary_time, line_index, interval_index] = auxiliary_transfer_time(individual, initial_time,
                                                                                   transfer_time, i)

            interval = metro_times[line_index][auxiliary_time.hour][interval_index]
            departure_minute = get_departure_minute(auxiliary_time, interval, interval_index, line_index,
                                                    auxiliary_time.hour)

            transfer_time += departure_minute - auxiliary_time.minute

    return transfer_time


def path_finding(source_station, destination_station):

    if source_station == destination_station:
        return Individual([source_station], [], [])

    stations_path = []
    time = []
    lines = []

    # Gets different lines on source station
    connections = data.get_station_connections(metro_map, source_station)

    if not connections:
        print("Station " + source_station + " does not exist on this map.")
        return Individual([], [], [])

    if not data.get_station_connections(metro_map, destination_station):
        print("Station " + destination_station + " does not exist on this map.")
        return Individual([], [], [])

    [current_line, index] = get_line_and_index(connections, source_station)

    # Random true or false
    forward = random() < 0.5

    # Gets current station instance
    current_station = current_line[index]

    # Adds current station name to result list
    stations_path.append(current_station.name)

    # Checks for end of line and switches direction if necessary
    forward = check_end_line(current_station, forward)

    while current_station.name != destination_station and current_station.code != destination_station:

        connections = data.get_station_connections(metro_map, current_station.name)

        if len(connections) != 1 and len(time) != 0:
            old_line = metro_map.index(current_line)
            [current_line, index] = get_line_and_index(connections, current_station.name)
            current_station = current_line[index]
            # Checks if line has changed
            if old_line != metro_map.index(current_line):
                forward = random() < 0.5
                forward = check_end_line(current_station, forward)

        if forward:
            index += 1
        else:
            index -= 1

        time = add_time(forward, time, current_station)
        current_station = current_line[index]
        stations_path.append(current_station.name)
        lines.append(colors[metro_map.index(current_line)])
        forward = check_end_line(current_station, forward)

    return Individual(stations_path, time, lines)


# individual = path_finding("Brigadeiro", "Hospital Saboia")
# print(individual.stations, "\n", individual.time, "\n", individual.lines, "\n", individual.fitness)

