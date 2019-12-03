import eel
from structures import Graph
import queue
from geopy.distance import geodesic

eel.init('web', allowed_extensions=['.js', '.html'])

DIST_INTERCHANGE = 1

#stations[ station ] = [coordinates (real), neighbors = {neighbor_1 : dist(station, neighbor_1), ...}] 
yamanote_line = {'mejiro' : [(35.720882, 139.706446),        {'ikebukuro': 0, 'tokadanobaba' : 0}],
                'ikebukuro' : [(35.729694, 139.710717),     {'otsuka' : 0, 'mejiro' : 0}],
                'otsuka' : [(35.731622, 139.728111),        {'sugamo' : 0, 'ikebukuro' : 0}],
                'sugamo' : [(35.733341, 139.739617),        {'komagome' : 0, 'otsuka' : 0}],
                'komagome' : [(35.737177, 139.748937),      {'tabata' : 0, 'sugamo' : 0}],
                'tabata' : [(35.737906, 139.761062),        {'nishi-nippori' : 0, 'komagome' : 0}],
                'nishi-nippori' : [(35.732538, 139.766770), {'nippori' : 0,'tabata' : 0}],
                'nippori' : [(35.728453, 139.770268),       {'uguisudani' : 0, 'nishi-nippori' : 0}],
                'uguisudani' : [(35.721598, 139.778207),    {'ueno' : 0, 'nippori' : 0}],
                'ueno' : [(35.714290, 139.777488),          {'okachimachi' : 0, 'uguisudani' : 0}],
                'okachimachi' : [(35.707312, 139.774666),   {'akihabara' : 0, 'ueno' : 0}],
                'akihabara' : [(35.698078, 139.772977),     {'kanda' : 0, 'okachimachi' : 0}],
                'kanda' : [(35.691891, 139.771065),         {'tokyo' : 0, 'akihabara' : 0}],
                'tokyo' : [(35.681689, 139.766721),         {'yurakucho' : 0, 'kanda' : 0}],
                'yurakucho' : [(35.674464, 139.762311),     {'shimbashi' : 0, 'tokyo' : 0}],
                'shimbashi' : [(35.665617, 139.758320),     {'hamamatsucho' : 0, 'yurakucho' : 0}],
                'hamamatsucho' : [(35.655671, 139.757065),  {'tamachi' : 0, 'shimbashi' : 0}],
                'tamachi' : [(35.645989, 139.747875),       {'shinagawa' : 0, 'hamamatsucho' : 0}],
                'shinagawa' : [(35.628123, 139.739378),     {'osaki' : 0, 'tamachi' : 0}],
                'osaki' : [(35.620183, 139.727706),         {'gotanda' : 0, 'shinagawa' : 0}],
                'gotanda' : [(35.626366, 139.723339),       {'meguro' : 0, 'osaki' : 0}],
                'meguro' : [(35.634345, 139.715775),        {'ebisu' : 0, 'gotanda' : 0}],
                'ebisu' : [(35.646901, 139.710325),         {'shibuya' : 0, 'meguro' : 0}],
                'shibuya' : [(35.658356, 139.701763),       {'harajuku' : 0, 'ebisu' : 0}],
                'harajuku' : [(35.670028, 139.702321),      {'yoyogi_v' : 0, 'shibuya' : 0}],
                'yoyogi_v' : [(35.683188, 139.701838),      {'shinjuku_v' : 0, 'harajuku' : 0, 'yoyogi_a' : DIST_INTERCHANGE}],
                'shinjuku_v' : [(35.690142, 139.700905),    {'shin-okubo' : 0, 'yoyogi_v' : 0, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
                'shin-okubo' : [(35.701242, 139.700322),    {'takadonobaba' : 0, 'shinjuku_v' : 0}],
                'takadonobaba' : [(35.712696, 139.703658),  {'mejiro' : 0, 'shin-okubo' : 0}]
                }

chuo_line = {'shinjuku_r' : [(35.690142, 139.700905),    {'ochanomizu_r' : 0, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_v': DIST_INTERCHANGE}],
            'ochanomizu_r' : [(35.700785, 139.763734),  {'tokyo' : 0, 'shinjuku_r' : 0}]
            }

sobu_line = {'shinjuku_a': [(35.690142, 139.700905),     {'yoyogi_a' : 0, 'shinjuku_v': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
            'yoyogi_a' : [(35.683188, 139.701838),      {'sendagaya' : 0, 'shinjuku_a': 0, 'yoyogi_v' : DIST_INTERCHANGE}],
            'sendagaya' : [(35.681405, 139.711334),     {'shinanomachi' : 0, 'yoyogi_a' : 0}],
            'shinanomachi' : [(35.680281, 139.719445),  {'yotsuya' : 0, 'sendagaya' : 0}],
            'yotsuya' : [(35.686102, 139.729369),       {'lichigaya' : 0, 'shinanomachi' : 0}],
            'lichigaya' : [(35.690851, 139.735270),     {'lidabashi' : 0, 'yotsuya' : 0}],
            'lidabashi' : [(35.701918, 139.744240),     {'suidobashi': 0, 'lichigaya' : 0}],
            'suidobashi': [(35.701970, 139.752662),     {'ochanomizu_a' : 0, 'lidabashi' : 0}],
            'ochanomizu_a' : [(35.700785, 139.763734),  {'akihabara' : 0, 'suidobashi': 0}]
            }


@eel.expose
def is_station(station):
    return station in yamanote_line or station in chuo_line or station in sobu_line

def get_coords(station):

    if station in yamanote_line:
        coords = yamanote_line[station][0]

    elif station in chuo_line:
        coords = chuo_line[station][0]

    else:
        coords = sobu_line[station][0]

    return coords

#draw[ station ] : [coordinates (picture), neighbors = {neighbor_1 : [color, path(station, neighbor_1)], ...}]
#path(station, neighbor_i) = [path_coordinate_1, ...]
draw = {'mejiro' : [(),        {'ikebukuro': 0, 'tokadanobaba' : 0}],
            'ikebukuro' : [(),     {'otsuka' : 0, 'mejiro' : 0}],
            'otsuka' : [(),        {'sugamo' : 0, 'ikebukuro' : 0}],
            'sugamo' : [(),        {'komagome' : 0, 'otsuka' : 0}],
            'komagome' : [(),      {'tabata' : 0, 'sugamo' : 0}],
            'tabata' : [(),        {'nishi-nippori' : 0, 'komagome' : 0}],
            'nishi-nippori' : [(), {'nippori' : 0,'tabata' : 0}],
            'nippori' : [(),       {'uguisudani' : 0, 'nishi-nippori' : 0}],
            'uguisudani' : [(),    {'ueno' : 0, 'nippori' : 0}],
            'ueno' : [(),          {'okachimachi' : 0, 'uguisudani' : 0}],
            'okachimachi' : [(),   {'akihabara' : 0, 'ueno' : 0}],
            'akihabara' : [(35.698078, 139.772977),     {'kanda' : 0, 'okachimachi' : 0}],
            'kanda' : [(35.691891, 139.771065),         {'tokyo' : 0, 'akihabara' : 0}],
            'tokyo' : [(35.681689, 139.766721),         {'yurakucho' : 0, 'kanda' : 0}],
            'yurakucho' : [(35.674464, 139.762311),     {'shimbashi' : 0, 'tokyo' : 0}],
            'shimbashi' : [(35.665617, 139.758320),     {'hamamatsucho' : 0, 'yurakucho' : 0}],
            'hamamatsucho' : [(35.655671, 139.757065),  {'tamachi' : 0, 'shimbashi' : 0}],
            'tamachi' : [(35.645989, 139.747875),       {'shinagawa' : 0, 'hamamatsucho' : 0}],
            'shinagawa' : [(35.628123, 139.739378),     {'osaki' : 0, 'tamachi' : 0}],
            'osaki' : [(35.620183, 139.727706),         {'gotanda' : 0, 'shinagawa' : 0}],
            'gotanda' : [(35.626366, 139.723339),       {'meguro' : 0, 'osaki' : 0}],
            'meguro' : [(35.634345, 139.715775),        {'ebisu' : 0, 'gotanda' : 0}],
            'ebisu' : [(35.646901, 139.710325),         {'shibuya' : 0, 'meguro' : 0}],
            'shibuya' : [(35.658356, 139.701763),       {'harajuku' : 0, 'ebisu' : 0}],
            'harajuku' : [(35.670028, 139.702321),      {'yoyogi_v' : 0, 'shibuya' : 0}],
            'yoyogi_v' : [(35.683188, 139.701838),      {'shinjuku_v' : 0, 'harajuku' : 0, 'yoyogi_a' : DIST_INTERCHANGE}],
            'shinjuku_v' : [(35.690142, 139.700905),    {'shin-okubo' : 0, 'yoyogi_v' : 0, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
            'shin-okubo' : [(35.701242, 139.700322),    {'takadonobaba' : 0, 'shinjuku_v' : 0}],
            'takadonobaba' : [(35.712696, 139.703658),  {'mejiro' : 0, 'shin-okubo' : 0}],
            'shinjuku_a': [(35.690142, 139.700905),     {'yoyogi_a' : 0, 'shinjuku_v': DIST_INTERCHANGE, 'shinjuku_r': DIST_INTERCHANGE}],
            'yoyogi_a' : [(35.683188, 139.701838),      {'sendagaya' : 0, 'shinjuku_a': 0, 'yoyogi_v' : DIST_INTERCHANGE}],
            'sendagaya' : [(35.681405, 139.711334),     {'shinanomachi' : 0, 'yoyogi_a' : 0}],
            'shinanomachi' : [(35.680281, 139.719445),  {'yotsuya' : 0, 'sendagaya' : 0}],
            'yotsuya' : [(35.686102, 139.729369),       {'lichigaya' : 0, 'shinanomachi' : 0}],
            'lichigaya' : [(35.690851, 139.735270),     {'lidabashi' : 0, 'yotsuya' : 0}],
            'lidabashi' : [(35.701918, 139.744240),     {'suidobashi': 0, 'lichigaya' : 0}],
            'suidobashi': [(35.701970, 139.752662),     {'ochanomizu_a' : 0, 'lidabashi' : 0}],
            'ochanomizu_a' : [(35.700785, 139.763734),  {'akihabara' : 0, 'suidobashi': 0}],
            'shinjuku_r' : [(35.690142, 139.700905),    {'ochanomizu_r' : 0, 'shinjuku_a': DIST_INTERCHANGE, 'shinjuku_v': DIST_INTERCHANGE}],
            'ochanomizu_r' : [(35.700785, 139.763734),  {'tokyo' : 0, 'shinjuku_r' : 0}]
            }

@eel.expose
def say_hello_py(f, t, n):
    print(f + ' ' + t + ' ' + n)
    return ['  ajdsgf ', 1, 2, 3]


metro = Graph()

def set_graph():
    
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

    frontier = queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():

        current = frontier.get()
        
        if current == goal:
            break
        
        for next in metro.get_neighbors(current).keys():

            new_cost = cost_so_far[current] + metro.cost(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                f_next = new_cost + heuristic(next, goal)
                frontier.put(next, f_next)
                came_from[next] = current
                
                draw_line(current, next)
                
    return came_from, cost_so_far


def draw_line(from_station, to_station):

    for coordinate in draw[from_station][1][to_station][1]:
        eel.draw_line_to(coordinate)

    eel.set_line_color(draw[from_station][1][to_station][0])

if __name__ == "__main__":
    
    set_graph()

    eel.start('index.html', size=(1000, 600))