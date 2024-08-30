import sys

import pandas as pd
import xml.etree.ElementTree as ET

def main(osm_file, nodes_file):
    tree = ET.parse(osm_file)
    root = tree.getroot()

    nodes = []
    for node in root.findall('node'):
        node_id = node.get('id')
        lat = node.get('lat')
        lon = node.get('lon')
        nodes.append({
            'node_id': node_id, 
            'lat': lat, 
            'lon': lon,
        })

    df = pd.DataFrame(nodes)
    df = df.drop_duplicates()
    df.to_csv(nodes_file, index=False, header=True)

if __name__ == "__main__":
    main(*sys.argv[1:])