import sys
import json
import dijkstra


if __name__ == '__main__':

    with open(sys.argv[1], 'r') as data_file:
        datastore = json.load(data_file)
    
    distances = datastore['distances']
    requests = datastore['requests']
    vehicles = datastore['vehicles']
    
    for vehicle in vehicles:
        vehicle['available'] = True

    g = dijkstra.Graph()

    for distance in distances:
        if not distance['zipcode1'] in g.get_vertices():
            g.add_vertex(distance['zipcode1'])

        if not distance['zipcode2'] in g.get_vertices():
            g.add_vertex(distance['zipcode2'])

        g.add_edge(distance['zipcode1'], distance['zipcode2'], distance['distance'])

    """
    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    """


    def get_vehicle(vehicle_type, zipcode):
        available_vehicles = [v for v in vehicles if v['type'] == vehicle_type and v['available']]

        if len(available_vehicles) > 0:
            g.reset_vertices()
            place = g.get_vertex(zipcode)
            dijkstra.dijkstra(g, place)

            for av in available_vehicles:
                av['distance'] = g.get_vertex(av['zipcode']).get_distance()

            available_vehicles = sorted(available_vehicles, key=lambda k: k['distance'])
        
        return available_vehicles


    for request in requests:
        ev = get_vehicle(request['vehicle_type'], request['zipcode'])

        if len(ev) > 0:
            vehicles[vehicles.index(ev[0])]['available'] = False
            request['vehicle_id'] = ev[0]['id']
            request['distance'] = ev[0]['distance']
            print(request)


    # print(vehicles)
    # print(requests)
