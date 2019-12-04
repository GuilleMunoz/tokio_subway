import eel
from structures import Graph
import queue
from geopy.distance import geodesic
import time

eel.init('web', allowed_extensions=['.js', '.html'])

DIST_INTERCHANGE = 1

VERDE = '#65a15e'
ROJO = '#eb3636'
AMARILLO = '#fffb00'
GRIS = '#8e8e8e'

metro = Graph()

interchange_stations = {
    'shinjuku' : [(35.690142, 139.700905),   {'shinjuku_a' : 0, 'shinjuku_r' : 0, 'shinjuku_v' : 0}],
    'yoyogi' : [(35.683188, 139.701838),     {'yoyogi_a' : 0, 'yoyogi_v' : 0}],
    'ochanomizu' : [(35.700785, 139.763734), {'ochanomizu_r' : 0, 'ochanomizu_a' : 0}]}

#line[ station ] = [coordinates (real), neighbors = {neighbor_1 : dist(station, neighbor_1), ...}] 
yamanote_line = {
                'mejiro' : [(35.720882, 139.706446),        {'ikebukuro': 10, 'takadanobaba' : 10}],
                'ikebukuro' : [(35.729694, 139.710717),     {'otsuka' : 10, 'mejiro' : 10}],
                'otsuka' : [(35.731622, 139.728111),        {'sugamo' : 10, 'ikebukuro' : 10}],
                'sugamo' : [(35.733341, 139.739617),        {'komagome' : 10, 'otsuka' : 10}],
                'komagome' : [(35.737177, 139.748937),      {'tabata' : 10, 'sugamo' : 10}],
                'tabata' : [(35.737906, 139.761062),        {'nishi-nippori' : 10, 'komagome' : 10}],
                'nishi-nippori' : [(35.732538, 139.766770), {'nippori' : 10,'tabata' : 10}],
                'nippori' : [(35.728453, 139.770268),       {'uguisudani' : 10, 'nishi-nippori' : 10}],
                'uguisudani' : [(35.721598, 139.778207),    {'ueno' : 10, 'nippori' : 10}],
                'ueno' : [(35.714290, 139.777488),          {'okachimachi' : 10, 'uguisudani' : 10}],
                'okachimachi' : [(35.707312, 139.774666),   {'akihabara' : 10, 'ueno' : 10}],
                'akihabara' : [(35.698078, 139.772977),     {'kanda' : 10, 'okachimachi' : 10, 'ochanomizu_a' : 10}],
                'kanda' : [(35.691891, 139.771065),         {'tokyo' : 10, 'akihabara' : 10}],
                'tokyo' : [(35.681689, 139.766721),         {'yurakucho' : 10, 'kanda' : 10, 'ochanomizu_r' : 10}],
                'yurakucho' : [(35.674464, 139.762311),     {'shimbashi' : 10, 'tokyo' : 10}],
                'shimbashi' : [(35.665617, 139.758320),     {'hamamatsucho' : 10, 'yurakucho' : 10}],
                'hamamatsucho' : [(35.655671, 139.757065),  {'tamachi' : 10, 'shimbashi' : 10}],
                'tamachi' : [(35.645989, 139.747875),       {'shinagawa' : 10, 'hamamatsucho' : 10}],
                'shinagawa' : [(35.628123, 139.739378),     {'osaki' : 10, 'tamachi' : 10}],
                'osaki' : [(35.620183, 139.727706),         {'gotanda' : 10, 'shinagawa' : 10}],
                'gotanda' : [(35.626366, 139.723339),       {'meguro' : 10, 'osaki' : 10}],
                'meguro' : [(35.634345, 139.715775),        {'ebisu' : 10, 'gotanda' : 10}],
                'ebisu' : [(35.646901, 139.710325),         {'shibuya' : 10, 'meguro' : 10}],
                'shibuya' : [(35.658356, 139.701763),       {'harajuku' : 10, 'ebisu' : 10}],
                'harajuku' : [(35.670028, 139.702321),      {'yoyogi_v' : 10, 'shibuya' : 10}],
                'yoyogi_v' : [(35.683188, 139.701838),      {'shinjuku_v' : 10, 'harajuku' : 10, 'yoyogi_a' : DIST_INTERCHANGE}],
                'shinjuku_v' : [(35.690142, 139.700905),    {'shin-okubo' : 10, 'yoyogi_v' : 10, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
                'shin-okubo' : [(35.701242, 139.700322),    {'takadanobaba' : 10, 'shinjuku_v' : 10}],
                'takadanobaba' : [(35.712696, 139.703658),  {'mejiro' : 10, 'shin-okubo' : 10}]
                }

chuo_line = {
            'shinjuku_r' : [(35.690142, 139.700905),    {'ochanomizu_r' : 10, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_v': DIST_INTERCHANGE}],
            'ochanomizu_r' : [(35.700785, 139.763734),  {'tokyo' : 10, 'shinjuku_r' : 10}]
            }

sobu_line = {
            'shinjuku_a' : [(35.690142, 139.700905),    {'yoyogi_a' : 10, 'shinjuku_v': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
            'yoyogi_a' : [(35.683188, 139.701838),      {'sendagaya' : 10, 'shinjuku_a': 10, 'yoyogi_v' : DIST_INTERCHANGE}],
            'sendagaya' : [(35.681405, 139.711334),     {'shinanomachi' : 10, 'yoyogi_a' : 10}],
            'shinanomachi' : [(35.680281, 139.719445),  {'yotsuya' : 10, 'sendagaya' : 10}],
            'yotsuya' : [(35.686102, 139.729369),       {'lichigaya' : 10, 'shinanomachi' : 10}],
            'lichigaya' : [(35.690851, 139.735270),     {'lidabashi' : 10, 'yotsuya' : 10}],
            'lidabashi' : [(35.701918, 139.744240),     {'suidobashi': 10, 'lichigaya' : 10}],
            'suidobashi': [(35.701970, 139.752662),     {'ochanomizu_a' : 10, 'lidabashi' : 10}],
            'ochanomizu_a' : [(35.700785, 139.763734),  {'akihabara' : 10, 'suidobashi': 10}]
            }


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

#draw[ station ] : [coordinates (picture), neighbors = {neighbor_1 : [color, path(station, neighbor_1)], ...}]
#path(station, neighbor_i) = [path_coordinate_1, ...]
draw = {'mejiro' : [(553,158),        {'ikebukuro': [VERDE, [()]], 'takadanobaba' : [VERDE, []]}],
            'ikebukuro' : [(617,117),     {'otsuka' : [VERDE, []], 'mejiro' : [VERDE, [()]]}],
            'otsuka' : [(687,117),        {'sugamo' : [VERDE, []], 'ikebukuro' : [VERDE, []]}],
            'sugamo' : [(),        {'komagome' : [VERDE, []], 'otsuka' : [VERDE, []]}],
            'komagome' : [(760,117),      {'tabata' : [VERDE, [()]], 'sugamo' : [VERDE, []]}],
            'tabata' : [(802,136),        {'nishi-nippori' : [VERDE, []], 'komagome' : [VERDE, [()]]}],
            'nishi-nippori' : [(825,153), {'nippori' : [VERDE, [()]],'tabata' : [VERDE, []]}],
            'nippori' : [(830,190),       {'uguisudani' : [VERDE, []], 'nishi-nippori' : [VERDE, [()]]}],
            'uguisudani' : [(830,218),    {'ueno' : [VERDE, []], 'nippori' : [VERDE, []]}],
            'ueno' : [(830,248),          {'okachimachi' : [VERDE, []], 'uguisudani' : [VERDE, []]}],
            'okachimachi' : [(830,280),   {'akihabara' : [VERDE, []], 'ueno' : [VERDE, []]}],
            'akihabara' : [(830,311),     {'kanda' : [VERDE, []], 'okachimachi' : [VERDE, []], 'ochanomizu_a' : [AMARILLO, []]}],
            'kanda' : [(830,357),         {'tokyo' : [VERDE, []], 'akihabara' : [VERDE, []]}],
            'tokyo' : [(830,400),         {'yurakucho' : [VERDE, [()]], 'kanda' : [VERDE, []], 'ochanomizu_r' : [ROJO, [(), (), ()]]}],
            'yurakucho' : [(827,440),     {'shimbashi' : [VERDE, []], 'tokyo' : [VERDE, [()]]}],
            'shimbashi' : [(801,467),     {'hamamatsucho' : [VERDE, []], 'yurakucho' : [VERDE, []]}],
            'hamamatsucho' : [(770,494),  {'tamachi' : [VERDE, []], 'shimbashi' : [VERDE, []]}],
            'tamachi' : [(737,530),       {'shinagawa' : [VERDE, []], 'hamamatsucho' : [VERDE, []]}],
            'shinagawa' : [(704,565),     {'osaki' : [VERDE, [()]], 'tamachi' : [VERDE, []]}],
            'osaki' : [(641,575),         {'gotanda' : [VERDE, []], 'shinagawa' : [VERDE, [()]]}],
            'gotanda' : [(602,575),       {'meguro' : [VERDE, []], 'osaki' : [VERDE, []]}],
            'meguro' : [(565,575),        {'ebisu' : [VERDE, [(), ()]], 'gotanda' : [VERDE, []]}],
            'ebisu' : [(512,545),         {'shibuya' : [VERDE, []], 'meguro' : [VERDE, [(), ()]]}],
            'shibuya' : [(512,488),       {'harajuku' : [VERDE, []], 'ebisu' : [VERDE, []]}],
            'harajuku' : [(512,440),      {'yoyogi_v' : [VERDE, []], 'shibuya' : [VERDE, []]}],
            'yoyogi_v' : [(512,461),      {'shinjuku_v' : [VERDE, []], 'harajuku' : [VERDE, []], 'yoyogi_a' : [GRIS, []]}],
            'shinjuku_v' : [(),    {'shin-okubo' : [VERDE, []], 'yoyogi_v' : [VERDE, []], 'shinjuku_a': [GRIS, []], 'shinjuku_r': [GRIS, []]}],
            'shin-okubo' : [(),    {'takadanobaba' : [VERDE, [()]], 'shinjuku_v' : [VERDE, []]}],
            'takadanobaba' : [(),  {'mejiro' : [VERDE, []], 'shin-okubo' : [VERDE, [()]]}],
            'shinjuku_a': [(),     {'yoyogi_a' : [AMARILLO, []], 'shinjuku_v': [GRIS, []], 'shinjuku_r': [GRIS, []]}],
            'yoyogi_a' : [(465,362),      {'sendagaya' : [AMARILLO, [()]], 'shinjuku_a': [AMARILLO, []], 'yoyogi_v' : [GRIS, []]}],
            'sendagaya' : [(),     {'shinanomachi' : [AMARILLO, []], 'yoyogi_a' : [AMARILLO, [()]]}],
            'shinanomachi' : [(),  {'yotsuya' : [AMARILLO, [()]], 'sendagaya' : [AMARILLO, []]}],
            'yotsuya' : [(),       {'lichigaya' : [AMARILLO, []], 'shinanomachi' : [AMARILLO, [()]]}],
            'lichigaya' : [(),     {'lidabashi' : [AMARILLO, []], 'yotsuya' : [AMARILLO, []]}],
            'lidabashi' : [(),     {'suidobashi': [AMARILLO, []], 'lichigaya' : [AMARILLO, []]}],
            'suidobashi': [(),     {'ochanomizu_a' : [AMARILLO, [()]], 'lidabashi' : [AMARILLO, []]}],
            'ochanomizu_a' : [(),  {'akihabara' : [AMARILLO, []], 'suidobashi': [AMARILLO, [()]]}],
            'shinjuku_r' : [(),    {'ochanomizu_r' : [ROJO, [(), (), ()]], 'shinjuku_a': [GRIS, []], 'shinjuku_v': [GRIS, []]}],
            'ochanomizu_r' : [(),  {'tokyo' : [ROJO, [(), (), ()]], 'shinjuku_r' : [ROJO, [(), (), ()]]}]
            }

@eel.expose
def say_hello_py(f, t, n):
    print(f + ' ' + t + ' ' + n)
    return ['  ajdsgf ', 1, 2, 3]


def draw_line(from_station, to_station):

    eel.move_to(draw[from_station][0])

    for coordinate in draw[from_station][1][to_station][1]:
        eel.draw_line_to(coordinate)

    eel.draw_line_to(draw[to_station][0])

    eel.set_line_color(draw[from_station][1][to_station][0])
    eel.draw_point(draw[from_station][0], 10)
    eel.draw_point(draw[to_station][0], 10)

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

            new_cost = cost_so_far[current] + metro.cost(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                f_next = new_cost + heuristic(next, goal)
                print('\tnext = %s,  cost = %s'% (next, f_next))
                frontier.put((f_next, next))
                came_from[next] = current
                
                draw_line(current, next)
                time.sleep(0.2)

    last = current

    while True:
        print(last)
        if last == start:
            break
        last = came_from[last]
        
    return came_from, cost_so_far


if __name__ == "__main__":
    
    set_graph()

    eel.start('index.html', size=(1000, 600))