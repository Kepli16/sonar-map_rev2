import folium
import xml.etree.ElementTree as ET

# Create base map
m = folium.Map(location=[36.5, -122], zoom_start=10)

# Parse KML file
tree = ET.parse('cleaned_doc.kml')
root = tree.getroot()
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Loop through all GroundOverlay elements
for overlay in root.findall(".//kml:GroundOverlay", ns):
    href = overlay.find(".//kml:Icon/kml:href", ns)
    latlonbox = overlay.find("kml:LatLonBox", ns)

    if href is not None and latlonbox is not None:
        image_path = href.text
        north = float(latlonbox.find("kml:north", ns).text)
        south = float(latlonbox.find("kml:south", ns).text)
        east = float(latlonbox.find("kml:east", ns).text)
        west = float(latlonbox.find("kml:west", ns).text)

        # Add image overlay
        folium.raster_layers.ImageOverlay(
            image=image_path,
            bounds=[[south, west], [north, east]],
            opacity=0.6
        ).add_to(m)

# Save the map
m.save("output_map.html")
print("Map with sonar overlays saved to output_map.html")
