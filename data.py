class Station:
    def __init__(self, name, code, forth_time, back_time):
        self.name = name
        self.code = code
        self.forthTime = forth_time
        self.backTime = back_time


colors = ["Red", "Black", "Blue", "Yellow", "Brown", "Gray", "Green", "Orange", "Purple", "Pink"]


def get_station_connections(m_map, station):
    res = []
    for line in m_map:
        for s in line:
            if station == s.name or station == s.code:
                res.append(m_map.index(line))
    return res
    # return [colors[i] for i in res]


def get_station_index(line, station):
    for s in line:
        if s.name == station or s.code == station:
            return line.index(s)


# All the different lines with their respective stations (Vila Calma is a missing station in the data)
red_line = [Station("Belém", 38, 2, 0), Station("Vila Madalena", 58, 8, 2), Station("Utinga", 54, 4, 8),
            Station("Panamby", 52, 4, 4), Station("Hebraica-Rebouças", 50, 4, 4), Station("Sao Lucas", 48, 8, 4),
            Station("Berrini", 44, 2, 8), Station("Américo Mourano", 64, 4, 2),
            Station("Cidade Universitária", 104, 2, 4), Station("Estádio Morumbi", 124, 10, 2),
            Station("Presidente Altino", 224, 0, 10)]

black_line = [Station("Moema", 328, 8, 0), Station("Villa Lobos-Jaguaré", 332, 10, 8),
              Station("Vila Clarice", 232, 2, 10), Station("Brigadeiro", 231, 4, 2), Station("Borba Gato", 229, 10, 4),
              Station("Presidente Altino", 224, 2, 10), Station("Pirituba", 223, 4, 2),
              Station("Vila Tolstói", 263, 0, 4)]

blue_line = [Station("Domingos de Moraes", 262, 2, 0), Station("Vila Tolstói", 263, 10, 2),
             Station("Campo Limpo", 363, 0, 10)]

yellow_line = [Station("Tatuapé", 170, 2, 0), Station("Vila Prudente", 171, 6, 2), Station("Brigadeiro", 231, 2, 6),
               Station("Vila Clarice", 232, 2, 2), Station("Camilo Haddad", 233, 2, 2),
               Station("Vila Calma", 234, 4, 2), Station("Hospital Saboia", 236, 4, 4), Station("Saude", 238, 2, 4),
               Station("Vila Paulista", 239, 4, 2), Station("República", 279, 2, 4), Station("Vila Mariana", 280, 0, 2)]

brown_line = [Station("Vila Cardosa", 14, 4, 0), Station("Utinga", 54, 4, 4), Station("Panamby", 52, 2, 4),
              Station("Osasco", 72, 0, 2)]

gray_line = [Station("Sao Judas", 10, 4, 0), Station("Hebraica-Rebouças", 50, 4, 4), Station("Sao Lucas", 48, 8, 4),
             Station("Berrini", 44, 2, 8), Station("Américo Mourano", 64, 2, 2),
             Station("Imperatriz Leopoldina", 65, 0, 2)]

green_line = [Station("Tucuruvi", 28, 2, 0), Station("Sao Lucas", 48, 8, 2), Station("Berrini", 44, 2, 8),
              Station("Américo Mourano", 64, 4, 2), Station("Cidade Universitária", 104, 2, 4),
              Station("Hospital Sao Paulo", 105, 0, 2)]

orange_line = [Station("Jardim Sao Paulo", 128, 4, 0), Station("Agua Branca", 126, 4, 4),
               Station("Estádio Morumbi", 124, 10, 4), Station("Presidente Altino", 224, 10, 10),
               Station("Borba Gato", 229, 4, 10), Station("Pedro II", 189, 0, 4)]

purple_line = [Station("Vila das Belezas", 352, 2, 0), Station("Villa Lobos-Jaguaré", 332, 10, 2),
               Station("Vila Clarice", 232, 2, 10), Station("Camilo Haddad", 233, 2, 2),
               Station("Vila Calma", 234, 4, 2), Station("Hospital Saboia", 236, 2, 4), Station("Carandiru", 256, 0, 2)]

pink_line = [Station("Joao Paulo I", 213, 2, 0), Station("Camilo Haddad", 233, 2, 2), Station("Vila Calma", 234, 4, 2),
             Station("Hospital Saboia", 236, 4, 4), Station("Saude", 238, 2, 4), Station("Vila Paulista", 239, 4, 2),
             Station("República", 279, 2, 4), Station("Vila Mariana", 280, 0, 2)]

# Whole map is a list of lines
metro_map = [red_line, black_line, blue_line, yellow_line, brown_line, gray_line, green_line, orange_line,
             purple_line, pink_line]

# Each tuple is an hour, first value of each tuple is the frequency of trains exiting the first station of its line
# going forward, second value is the same but backwards. If the value inside a tuple is a list then the
# frequency does not start on the minute 0 of the hour, instead it's divided in [frequency in minutes,
# minute of first train] i.e: [20, 10] = 10, 30, 50
red_times = [(30, 30), (30, 30), (30, 30), (15, 15), (10, 15), (5, 10), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5),
             (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (10, 5), (15, 5), (15, 15), (30, 15), (30, 30), (30, 30)]

black_times = [(30, 30), (30, 30), (30, 30), (15, 15), (10, 15), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10),
               (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (15, 10),
               (15, 15), (30, 15), (30, 30), (30, 30)]

blue_times = [(False, False), (False, False), (30, False), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30),
              (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30), (30, 30),
              (30, 30), (30, 30), (False, 30), (False, 30), (False, False)]

yellow_times = [(30, 30), (30, 30), (30, 30), (5, 15), (5, 15), (5, 10), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5),
                (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 15), (30, 15), (30, 30), (30, 30)]

brown_times = [(False, False), (False, False), (20, False), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30),
               (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30), (20, 30),
               (False, 30), (False, 30), (False, 0), (False, 0), (False, False)]

gray_times = [(False, False), (False, False), (30, False), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20),
              (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20), (30, 20),
              (30, 20), (30, 20), (False, 20), (False, 20), (False, False)]

green_times = [(False, False), (False, False), ([30, 15], False), ([30, 15], [20, 10]), ([30, 15], [20, 10]),
               ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]),
               ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]),
               ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]),
               ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], [20, 10]), ([30, 15], 30), (False, 30),
               (False, False), (False, False)]

orange_times = [(30, 30), (30, 30), (30, 30), (30, 15), ([20, 10], 15), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20),
                ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20),
                ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20), ([20, 10], 20),
                ([20, 10], 20), (30, 20), (30, 30), (30, 30)]

purple_times = [(False, False), (False, False), (0, False), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]),
                (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]),
                (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]), (0, [0, 30]),
                (False, [0, 30]), (False, [0, 30]), (False, False)]

pink_times = [(30, 30), (30, 30), (30, 30), (15, 15), (10, 15), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10),
              (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (15, 10),
              (15, 15), (30, 15), (30, 30), (30, 30)]

metro_times = [red_times, black_times, blue_times, yellow_times, brown_times, gray_times, green_times, orange_times,
               purple_times, pink_times]


def get_map():
    return metro_map


def get_times():
    return metro_times
