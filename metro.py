import eel
from structures import Graph
import queue
from geopy.distance import geodesic
import time

eel.init('web', allowed_extensions=['.js', '.html'])

DIST_INTERCHANGE = 1

VERDE = '#65a15e'
ROJO = '#ff3334'
AMARILLO = '#ffcc66'
GRIS = '#8e8e8e'

metro = Graph()

interchange_stations = {
    'Shinjuku' : [(35.690142, 139.700905),   {'Shinjuku_a' : 0, 'Shinjuku_r' : 0, 'Shinjuku_v' : 0}],
    'Yoyogi' : [(35.683188, 139.701838),     {'Yoyogi_a' : 0, 'Yoyogi_v' : 0}],
    'Ochanomizu' : [(35.700785, 139.763734), {'Ochanomizu_r' : 0, 'Ochanomizu_a' : 0}]}

#line[ station ] = [coordinates (real), neighbors = {neighbor_1 : dist(station, neighbor_1), ...}] 
yamanote_line = {
                'Mejiro' : [(35.720882, 139.706446),        {'Ikebukuro': 1.08, 'Takadanobaba' : 0.86479}],
                'Ikebukuro' : [(35.729694, 139.710717),     {'Otsuka' : 2.03, 'Mejiro' : 1.08}],
                'Otsuka' : [(35.731622, 139.728111),        {'Sugamo' : 1.05, 'Ikebukuro' : 2.03}],
                'Sugamo' : [(35.733341, 139.739617),        {'Komagome' : 0.77, 'Otsuka' : 1.05}],
                'Komagome' : [(35.737177, 139.748937),      {'Tabata' : 1.45, 'Sugamo' : 0.77}],
                'Tabata' : [(35.737906, 139.761062),        {'Nishi-Nippori' : 0.8347, 'Komagome' : 1.45}],
                'Nishi-Nippori' : [(35.732538, 139.766770), {'Nippori' : 0.5512,'Tabata' : 0.8347}],
                'Nippori' : [(35.728453, 139.770268),       {'Uguisudani' : 0.99055, 'Nishi-Nippori' : 0.5512}],
                'Uguisudani' : [(35.721598, 139.778207),    {'Ueno' : 0.91145, 'Nippori' : 0.99055}],
                'Ueno' : [(35.714290, 139.777488),          {'Okachimachi' : 0.77642, 'Uguisudani' : 0.91145}],
                'Okachimachi' : [(35.707312, 139.774666),   {'Akihabara' : 1.04, 'Ueno' : 0.77642}],
                'Akihabara' : [(35.698078, 139.772977),     {'Kanda' : 0.76525, 'Okachimachi' : 1.04, 'Ochanomizu_a' : 0.71711}],
                'Kanda' : [(35.691891, 139.771065),         {'Tokyo' : 1.21, 'Akihabara' : 0.76525}],
                'Tokyo' : [(35.681689, 139.766721),         {'Yurakucho' : 0.88781, 'Kanda' : 1.21, 'Ochanomizu_r' : 2.23}],
                'Yurakucho' : [(35.674464, 139.762311),     {'Shimbashi' : 1.03, 'Tokyo' : 0.88781}],
                'Shimbashi' : [(35.665617, 139.758320),     {'Hamamatsucho' : 1.25, 'Yurakucho' : 1.03}],
                'Hamamatsucho' : [(35.655671, 139.757065),  {'Tamachi' : 1.37, 'Shimbashi' : 1.25}],
                'Tamachi' : [(35.645989, 139.747875),       {'Shinagawa' : 2.19, 'Hamamatsucho' : 1.37}],
                'Shinagawa' : [(35.628123, 139.739378),     {'Osaki' : 2.09, 'Tamachi' : 2.19}],
                'Osaki' : [(35.620183, 139.727706),         {'Gotanda' : 0.8027, 'Shinagawa' : 2.09}],
                'Gotanda' : [(35.626366, 139.723339),       {'Meguro' : 1.15, 'Osaki' : 0.8027}],
                'Meguro' : [(35.634345, 139.715775),        {'Ebisu' : 1.48, 'Gotanda' : 1.15}],
                'Ebisu' : [(35.646901, 139.710325),         {'Shibuya' : 1.47, 'Meguro' : 1.48}],
                'Shibuya' : [(35.658356, 139.701763),       {'Harajuku' : 1.47, 'Ebisu' : 1.47}],
                'Harajuku' : [(35.670028, 139.702321),      {'Yoyogi_v' : 1.4, 'Shibuya' : 1.47}],
                'Yoyogi_v' : [(35.683188, 139.701838),      {'Shinjuku_v' : 0.7704, 'Harajuku' : 1.4, 'Yoyogi_a' : DIST_INTERCHANGE}],
                'Shinjuku_v' : [(35.690142, 139.700905),    {'Shin-Okubo' : 1.19, 'Yoyogi_v' : 0.7704, 'Shinjuku_a': DIST_INTERCHANGE, 'Shinjuku_r': DIST_INTERCHANGE}],
                'Shin-Okubo' : [(35.701242, 139.700322),    {'Takadanobaba' : 1.34, 'Shinjuku_v' : 1.19}],
                'Takadanobaba' : [(35.712696, 139.703658),  {'Mejiro' : 0.86479, 'Shin-Okubo' : 1.34}]
                }

chuo_line = {
            'Shinjuku_r' : [(35.690142, 139.700905),    {'Ochanomizu_r' : 7.77, 'Shinjuku_a': DIST_INTERCHANGE, 'Shinjuku_v': DIST_INTERCHANGE}],
            'Ochanomizu_r' : [(35.700785, 139.763734),  {'Tokyo' : 2.23, 'Shinjuku_r' : 7.77}]
            }

sobu_line = {
            'Shinjuku_a' : [(35.690142, 139.700905),    {'Yoyogi_a' : 0.762, 'Shinjuku_v': DIST_INTERCHANGE, 'Shinjuku_r': DIST_INTERCHANGE}],
            'Yoyogi_a' : [(35.683188, 139.701838),      {'Sendagaya' : 0.98635, 'Shinjuku_a': 0.762, 'Yoyogi_v' : DIST_INTERCHANGE}],
            'Sendagaya' : [(35.681405, 139.711334),     {'Shinanomachi' : 0.85902, 'Yoyogi_a' : 0.98635}],
            'Shinanomachi' : [(35.680281, 139.719445),  {'Yotsuya' : 1.19, 'Sendagaya' : 0.85902}],
            'Yotsuya' : [(35.686102, 139.729369),       {'Lichigaya' : 1.08, 'Shinanomachi' : 1.19}],
            'Lichigaya' : [(35.690851, 139.735270),     {'Lidabashi' : 1.12, 'Yotsuya' : 1.08}],
            'Lidabashi' : [(35.701918, 139.744240),     {'Suidobashi': 0.90481, 'Lichigaya' : 1.12}],
            'Suidobashi': [(35.701970, 139.752662),     {'Ochanomizu_a' : 1.09, 'Lidabashi' : 0.90481}],
            'Ochanomizu_a' : [(35.700785, 139.763734),  {'Akihabara' : 0.71711, 'Suidobashi': 1.09}]
            }

@eel.expose
def format(name):
    pos = name.find('-')
    
    if pos == -1 or pos == len(name) - 1:
        return name.capitalize()
    
    res = name[0].capitalize() + name[1 : pos + 1].lower() + name[pos + 1].capitalize()
    res += name[pos + 2 : ].lower()
    return res
    

@eel.expose
def is_station(station):
    return metro.is_node(station) and not station[-2] == '_'

def get_coords(station):

    if station in interchange_stations:
        coords = interchange_stations[station][0]

    elif station in yamanote_line:
        coords = yamanote_line[station][0]

    elif station in chuo_line:
        coords = chuo_line[station][0]

    else:
        coords = sobu_line[station][0]

    return coords

#draw[ station ] : [coordinates (picture), neighbors = {neighbor_1 : [color, path(station, neighbor_1)], ...}, size, name_coords]
#path(station, neighbor_i) = [path_coordinate_1, ...]
'''
name = station

if name[-2] == '_':
    name = name[:-2]

size = 9 || 6

'''
draw = {'Mejiro' : [(553,158),        {'Ikebukuro': [VERDE, [(592, 117)]], 'Takadanobaba' : [VERDE, []]}, 6, (504, 150), 0],
            'Ikebukuro' : [(617,117),     {'Otsuka' : [VERDE, []], 'Mejiro' : [VERDE, [(592, 117)]]}, 9, (622, 103), -1/4],
            'Otsuka' : [(687,117),        {'Sugamo' : [VERDE, []], 'Ikebukuro' : [VERDE, []]}, 6, (688, 103), -1/4],
            'Sugamo' : [(722, 117),       {'Komagome' : [VERDE, []], 'Otsuka' : [VERDE, []]}, 6, (725, 103), -1/4],
            'Komagome' : [(760,117),      {'Tabata' : [VERDE, [(785, 117)]], 'Sugamo' : [VERDE, []]}, 6, (765, 103), -1/4],
            'Tabata' : [(807,136),        {'Nishi-Nippori' : [VERDE, []], 'Komagome' : [VERDE, [(785, 117)]]}, 9, (814, 126), -1/4],
            'Nishi-Nippori' : [(825,153), {'Nippori' : [VERDE, [(830, 160)]],'Tabata' : [VERDE, []]}, 6, (838, 149), -1/4],
            'Nippori' : [(830,190),       {'Uguisudani' : [VERDE, []], 'Nishi-Nippori' : [VERDE, [(830, 160)]]}, 9, (842, 195), 0],
            'Uguisudani' : [(830,218),    {'Ueno' : [VERDE, []], 'Nippori' : [VERDE, []]}, 6, (842, 224), 0],
            'Ueno' : [(830,248),          {'Okachimachi' : [VERDE, []], 'Uguisudani' : [VERDE, []]}, 9, (842, 253), 0],
            'Okachimachi' : [(830,280),   {'Akihabara' : [VERDE, []], 'Ueno' : [VERDE, []]}, 6, (842, 282), 0],
            'Akihabara' : [(830,311),     {'Kanda' : [VERDE, []], 'Okachimachi' : [VERDE, []], 'Ochanomizu_a' : [AMARILLO, []]}, 9, (842, 330), 0],
            'Kanda' : [(830,357),         {'Tokyo' : [VERDE, []], 'Akihabara' : [VERDE, []]}, 9, (842, 360), 0],
            'Tokyo' : [(830,400),         {'Yurakucho' : [VERDE, [(830, 435)]], 'Kanda' : [VERDE, []], 'Ochanomizu_r' : [ROJO, [(798, 400), (798, 337), (753, 289)]]}, 9, (773, 421), 0],
            'Yurakucho' : [(827,440),     {'Shimbashi' : [VERDE, []], 'Tokyo' : [VERDE, [(830, 435)]]}, 6, (837, 450), 0],
            'Shimbashi' : [(801,467),     {'Hamamatsucho' : [VERDE, []], 'Yurakucho' : [VERDE, []]}, 6, (812, 476), 0],
            'Hamamatsucho' : [(770,494),  {'Tamachi' : [VERDE, []], 'Shimbashi' : [VERDE, []]}, 9, (786, 502), 0],
            'Tamachi' : [(737,530),       {'Shinagawa' : [VERDE, []], 'Hamamatsucho' : [VERDE, []]}, 6, (748, 538), 0],
            'Shinagawa' : [(704,565),     {'Osaki' : [VERDE, [(693, 575)]], 'Tamachi' : [VERDE, []]}, 9, (718, 577), 0],
            'Osaki' : [(641,575),         {'Gotanda' : [VERDE, []], 'Shinagawa' : [VERDE, [(693, 575)]]}, 9, (650, 563), -1/4],
            'Gotanda' : [(602,575),       {'Meguro' : [VERDE, []], 'Osaki' : [VERDE, []]}, 6, (608, 563), -1/4],
            'Meguro' : [(565,575),        {'Ebisu' : [VERDE, [(537, 575), (510, 545)]], 'Gotanda' : [VERDE, []]}, 6, (566, 563), -1/4],
            'Ebisu' : [(510,540),         {'Shibuya' : [VERDE, []], 'Meguro' : [VERDE, [(510, 545), (537, 575)]]}, 6, (460, 553), 0],
            'Shibuya' : [(510,488),       {'Harajuku' : [VERDE, []], 'Ebisu' : [VERDE, []]}, 6, (442, 493), 0],
            'Harajuku' : [(510,440),      {'Yoyogi_v' : [VERDE, []], 'Shibuya' : [VERDE, []]}, 6, (435, 444), 0],
            'Yoyogi_v' : [(510,362),      {'Shinjuku_v' : [VERDE, []], 'Harajuku' : [VERDE, []], 'Yoyogi_a' : [GRIS, []]}, 9, (523, 367), 0],
            'Shinjuku_v' : [(510, 322),    {'Shin-Okubo' : [VERDE, []], 'Yoyogi_v' : [VERDE, []], 'Shinjuku_a': [GRIS, []], 'Shinjuku_r': [GRIS, []]}, 9, (523, 328), 0],
            'Shin-Okubo' : [(510, 238),    {'Takadanobaba' : [VERDE, [(510, 200)]], 'Shinjuku_v' : [VERDE, []]}, 6, (523, 244), 0],
            'Takadanobaba' : [(516, 195),  {'Mejiro' : [VERDE, []], 'Shin-Okubo' : [VERDE, [(510, 200)]]}, 6, (404, 189), 0],
            'Shinjuku_a': [(465, 322),     {'Yoyogi_a' : [AMARILLO, []], 'Shinjuku_v': [GRIS, []], 'Shinjuku_r': [GRIS, []]}, 9, (523, 328), 0],
            'Yoyogi_a' : [(465,362),      {'Sendagaya' : [AMARILLO, [(465, 410)]], 'Shinjuku_a': [AMARILLO, []], 'Yoyogi_v' : [GRIS, []]}, 9, (523, 367), 0],
            'Sendagaya' : [(535, 410),     {'Shinanomachi' : [AMARILLO, []], 'Yoyogi_a' : [AMARILLO, [(465, 410)]]}, 6, (532, 424), 1/4],
            'Shinanomachi' : [(580, 410),  {'Yotsuya' : [AMARILLO, [(585, 410)]], 'Sendagaya' : [AMARILLO, []]}, 6, (584, 429), 0],
            'Yotsuya' : [(607, 388),       {'Lichigaya' : [AMARILLO, []], 'Shinanomachi' : [AMARILLO, [(585, 410)]]}, 6, (621, 395), 0],
            'Lichigaya' : [(624, 368),     {'Lidabashi' : [AMARILLO, []], 'Yotsuya' : [AMARILLO, []]}, 6, (638, 375), 0],
            'Lidabashi' : [(643, 349),     {'Suidobashi': [AMARILLO, []], 'Lichigaya' : [AMARILLO, []]}, 6, (656, 356), 0],
            'Suidobashi': [(662, 330),     {'Ochanomizu_a' : [AMARILLO, [(682, 310)]], 'Lidabashi' : [AMARILLO, []]}, 6, (676, 338), 0],
            'Ochanomizu_a' : [(690, 310),  {'Akihabara' : [AMARILLO, []], 'Suidobashi': [AMARILLO, [(682, 310)]], 'Ochanomizu_r': [GRIS, []]}, 9, (719, 277), -1/4],
            'Shinjuku_r' : [(485, 322),    {'Ochanomizu_r' : [ROJO, [(485, 385), (583, 385), (676, 289)]], 'Shinjuku_a': [GRIS, []], 'Shinjuku_v': [GRIS, []]}, 9, (523, 328), 0],
            'Ochanomizu_r' : [(710, 289),  {'Tokyo' : [ROJO, [(753, 289), (798, 337), (798, 400)]], 'Shinjuku_r' : [ROJO, [(676, 289), (583, 385), (485, 385)]], 'Ochanomizu_a': [GRIS, []]}, 9, (719, 277), -1/4] }

@eel.expose
def say_hello_py(f, t, n):
    print(f + ' ' + t + ' ' + n)
    return ['  ajdsgf ', 1, 2, 3]


#Draw metro map
@eel.expose
def draw_map():
    for station in draw.keys():
        for neighbor in draw[station][1]:
            draw_line(station, neighbor)

def put_name(station):
    name = station

    if name[-2] == '_':
        name = name[:-2]
    
    eel.add_name(name, draw[station][-1], draw[station][-2])


def draw_line(from_station, to_station, color = '#50504e'):

    eel.move_to(draw[from_station][0])

    for coordinate in draw[from_station][1][to_station][1]:
        eel.draw_line_to(coordinate)

    eel.draw_line_to(draw[to_station][0])

    eel.set_line_color(draw[from_station][1][to_station][0])

    eel.draw_point(draw[from_station][0], draw[from_station][-3], '#50504e')
    eel.draw_point(draw[to_station][0], draw[to_station][-3], color)
    
    eel.set_text_Style("15px Helvetica", "black")
    put_name(from_station)
    put_name(to_station)


def set_graph():
    
    for key in interchange_stations.keys():
        metro.set_neighbors(key, interchange_stations[key][1])

    for key in yamanote_line.keys():
        metro.set_neighbors(key, yamanote_line[key][1])
    
    for key in chuo_line.keys():
        metro.set_neighbors(key, chuo_line[key][1])

    for key in sobu_line.keys():
        metro.set_neighbors(key, sobu_line[key][1])


# The heuristic def. h(n) estimates the cost to reach goal from node n.
def heuristic(a, b):
    return geodesic(get_coords(a), get_coords(b)).kilometers

@eel.expose
def a_star_search(start, goal):

    print(start)
    print(goal)

    eel.clear_canvas()
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():

        current = frontier.get()[1]
        print('current = ', current)
        if current == goal or current[:-2] == goal:
            break
        
        for next in metro.get_neighbors(current).keys():

            new_cost = cost_so_far[current] + metro.get_cost(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                f_next = new_cost + heuristic(next, goal)
                print('\tnext = %s,  f_cost = %s'% (next, f_next))
                frontier.put((f_next, next))
                came_from[next] = current
                
                if current not in interchange_stations:
                    draw_line(current, next, '#00ffff')
                
                time.sleep(0.2)

    eel.delimage()
    time.sleep(1.5)
    last = current
    
    eel.clear_canvas()
    dist = 0

    while True:
        
        if current == start or current[:-2] == start:
            break
        
        current = came_from[last]
        
        draw_line(last, current)
        
        if not (last[:-2] == current[:-2]):
            dist += metro.get_cost(last, current)
        
        last = current
    
    print(dist)
    eel.set_text_Style("20px Helvetica", "#3f3e3e")
    eel.add_name('Total distance: %s km' % str(round(dist, 3)), 0, (140, 550))
    eel.set_text_Style("15px Helvetica", "black")
        
    return came_from, cost_so_far


if __name__ == "__main__":
    
    set_graph()

    eel.start('index.html', size=(1000, 600))