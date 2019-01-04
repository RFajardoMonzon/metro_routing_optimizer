import data
from random import random, choice


metro_map = data.getMap()


def add_time(forward, time, station):
    if forward:
        time += station.forthTime
    else:
        time += station.backTime
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


def path(source_station, destination_station):
    if source_station == destination_station:
        return []

    res = []
    time = 0
    change_line = 0

    # Gets different lines on source station
    connections = data.get_station_connections(metro_map, source_station)

    [current_line, index] = get_line_and_index(connections, source_station)

    # Random true or false
    forward = random() < 0.5

    # Gets current station instance
    current_station = current_line[index]

    # Adds current station name to result list
    res.append(current_station.name)

    # Checks for end of line and switches direction if necessary
    forward = check_end_line(current_station, forward)

    # Adds appropriate time
    time = add_time(forward, time, current_station)

    while current_station.name != destination_station and current_station.code != destination_station:
        if forward:
            index += 1
        else:
            index -= 1

        current_station = current_line[index]
        res.append(current_station.name)
        forward = check_end_line(current_station, forward)
        time = add_time(forward, time, current_station)

        connections = data.get_station_connections(metro_map, current_station.name)

        if len(connections) != 1:
            old_line = metro_map.index(current_line)
            [current_line, index] = get_line_and_index(connections, current_station.name)
            current_station = current_line[index]
            # Checks if line has changed
            if old_line != metro_map.index(current_line):
                change_line += 1
                forward = random() < 0.5
                forward = check_end_line(current_station, forward)

    return [res, time, change_line]


[path, time, change_line] = path("Vila Prudente", "Saude")
print(path, time, change_line)

# print(check_end_line(metro_map[0][], False))
