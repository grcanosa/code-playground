import folium

map = folium.Map(location=[40,-3],zoom_start=6,tiles="Mapbox Bright")

fg = folium.FeatureGroup(name="My Map")
fg.add_child(folium.Marker(location=[40,-3],popup="lalala",icon=folium.Icon(color="green")))
map.add_child(fg)

map.save("map1.html")
