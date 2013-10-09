from imposm.parser import OSMParser
import pandas as pd
# simple class that handles the parsed OSM data.

styles = dict(primary=dict(lw=1, c='b'), primary_link=dict(lw=1, c='b'),
    secondary=dict(lw=0.5, c='g'), secondary_link=dict(lw=0.5, c='g'),
    tertiary=dict(lw=0.25, c='m'), tertiary_link=dict(lw=0.25, c='m'),
    motorway=dict(lw=1, c='k'), motorway_link=dict(lw=1, c='k'), 
    residential=dict(lw=0.25, c='k'))

class Parser(object):
    def __init__(self):
    	self.ways = []
    	self.coords = []
    	self.nodes = []
    	self.relations = []

    def ways_callback(self, ways):
        # callback method for ways
        for osm_id, tags, refs in ways:
            if 'highway' in tags.keys():
                self.ways.append([osm_id, tags, refs])
    def coords_callback(self, coords):
        # callback method for ways
        for coord in coords:
            self.coords.append(coord)
    def nodes_callback(self, nodes):
        # callback method for ways
        for node in nodes:
            self.nodes.append(node)
    def relations_callback(self, relations):
        # callback method for ways
        for relation in relations:
            self.relations.append(relation)

# instantiate counter and parser and start parsing
osm = Parser()
p = OSMParser(concurrency=2,
	ways_callback=osm.ways_callback,
	coords_callback=osm.coords_callback,
	nodes_callback=osm.nodes_callback)

p.parse('map.osm')

# put coordinate lat/longs in a referencable DataFrame
ref, lat, lon = zip(*osm.coords)
df = pd.DataFrame(dict(lat=lat, lon=lon), index=ref)

# plot berkeley
fig, ax = plt.subplots()
ax.set_aspect('equal')
for osm_id, tags, refs in osm.ways:
    coords = df.ix[refs]
    if tags['highway'] in styles.keys():
        style = styles[tags['highway']]
        ax.plot(coords.lat, coords.lon, lw=0.2, c='k')

def whatKeys():
    ref_keys = set()
    for osm_id, tags, refs in osm.ways:
        ref_keys.add(tags['highway'])



