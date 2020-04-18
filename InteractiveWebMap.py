import folium
import pandas

volcano_markers = pandas.read_csv("Volcanoes.txt")
lat = list(volcano_markers["LAT"])
lon = list(volcano_markers["LON"])
popup_msg = list(volcano_markers["ELEV"])


def color_prod(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 < elevation < 2000:
        return 'purple'
    elif 2000 < elevation < 3000:
        return 'orange'
    else:
        return 'red'


html = """<h4>Volcano information:</h4> Height: %s m"""

map = folium.Map(location=[38.8, -110.1], zoom_start=4, tiles="CartoDB positron")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, p_m in zip(lat, lon, popup_msg):
    iframe = folium.IFrame(html=html % str(p_m), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe),
                                      radius=6, fill_color=color_prod(p_m), color='black',
                                      fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("InteractiveWebMap.html")
