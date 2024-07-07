import requests

def get_nearby_hospitals(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node["amenity"="hospital"](around:5000,{lat},{lon});
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    hospitals = []
    for element in data['elements']:
        name = element['tags'].get('name', 'No name available')
        lat = element['lat']
        lon = element['lon']
        hospitals.append({'name': name, 'lat': lat, 'lon': lon})
    return hospitals

# Example usage
latitude = 12.914142
longitude =  74.855957
nearby_hospitals = get_nearby_hospitals(latitude, longitude)
print(nearby_hospitals)
