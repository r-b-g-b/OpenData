import xml.dom.minidom as minidom
import matplotlib.pyplot as plt

doc = minidom.parse('map.osm')
osm = doc.getElementsByTagName('osm')[0]

ways = osm.getElementsByTagName('way')
ways_tert = [way for way in ways if way.getAttribute('')]
nodes = osm.getElementsByTagName('node')

fig, ax = plt.subplots()

highways = []
for way in ways:
	for tag in way.getElementsByTagName('tag'):
		if tag.getAttribute('k')=='highway':
			highways.append(way)
			continue


	if way.getElementsByTagName('tag')
highways = [way for way in ways if way.getElementsByTagName('tag').getAttribute('k')=='highway']
ukeys = []
for way in ways:
	tags = way.getElementsByTagName('tag')
	for tag in tags:
		key = tag.getAttribute('k')
		if key not in ukeys:
			ukeys.append(key)
ways.

def plotWays(ways, fig=None):
	if fig is None:
		fig, ax = plt.subplots()
	for way in ways:

		way_nds = way.getElementsByTagName('nd')
		way_nodes = []
		for way_nd in way_nds:
		    way_nodes.append([node for node in nodes if node.getAttribute('id')==way_nd.getAttribute('ref')][0])

		way_lats, way_lons = [], []
		for way_node in way_nodes:
		    way_lons.append(float(way_node.getAttribute('lat')))
		    way_lats.append(float(way_node.getAttribute('lon')))


		ax.plot(way_lons, way_lats, c='k', ls='-')

plt.show()