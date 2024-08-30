import sys
import random

import geopy.distance

import pandas as pd
import xml.etree.ElementTree as ET

def get_random_node_id():
    return ''.join(random.choices('123456789', k=10))

def interpolate_nodes(lat1, lon1, lat2, lon2, spacing=3):
    start = (lat1, lon1)
    end = (lat2, lon2)
    distance = geopy.distance.distance(start, end).meters
    
    # Number of intervals
    num_intervals = int(distance // spacing)
    
    if num_intervals == 0:
        return []
    
    node_ids = [get_random_node_id() for i in range(1, num_intervals)]
    latitudes = [lat1 + (lat2 - lat1) * i / num_intervals for i in range(1, num_intervals)]
    longitudes = [lon1 + (lon2 - lon1) * i / num_intervals for i in range(1, num_intervals)]
    
    return list(zip(node_ids, latitudes, longitudes))

def main(osm_file, nodes_file):
    tree = ET.parse(osm_file)
    root = tree.getroot()

    # Lists to store node information
    data = []

    # Parse nodes
    nodes = {}
    for node in root.findall('node'):
        node_id = node.get('id')
        lat = float(node.get('lat'))
        lon = float(node.get('lon'))
        nodes[node_id] = (lat, lon)

    # Parse ways and collect node references
    for way in root.findall('way'):
        way_id = way.get('id')
        for nd in way.findall('nd'):
            node_id = nd.get('ref')
            if node_id in nodes:
                lat, lon = nodes[node_id]
                data.append([node_id, way_id, lat, lon])

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=['node_id', 'way_id', 'lat', 'lon'])
    df = df.drop_duplicates()
    
    # List to store the new nodes
    new_rows = []

    # Group by way_id
    for way_id, group in df.groupby('way_id'):
        # Convert group DataFrame to a list of tuples
        nodes = group[['node_id', 'lat', 'lon']].values.tolist()
        
        # Iterate over each pair of consecutive rows in the group
        for i in range(len(nodes) - 1):
            node_id1, lat1, lon1 = nodes[i]
            node_id2, lat2, lon2 = nodes[i + 1]
            
            # Original row
            new_rows.append((node_id1, way_id, lat1, lon1))
            
            # Interpolated nodes
            interpolated_nodes = interpolate_nodes(lat1, lon1, lat2, lon2, spacing=3)
            new_rows.extend([(node_id, way_id, lat, lon) for node_id, lat, lon in interpolated_nodes])
            
            # Original row
            new_rows.append((node_id2, way_id, lat2, lon2))

    # Add the last original row
    new_rows.append((
        df.loc[len(df) - 1, 'node_id'], 
        df.loc[len(df) - 1, 'way_id'], 
        df.loc[len(df) - 1, 'lat'], 
        df.loc[len(df) - 1, 'lon'],
    ))

    # Create a new DataFrame with the new nodes
    new_df = pd.DataFrame(new_rows, columns=['node_id', 'way_id', 'lat', 'lon'])
    
    new_df.to_csv(nodes_file, index=False, header=True)

if __name__ == "__main__":
    main(*sys.argv[1:])