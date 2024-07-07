import requests

# Your IPGeolocation API key
api_key = '16b2e9db5578445bab14eb4f8e996abb'

# Make a request to the IPGeolocation API
response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}')

if response.status_code == 200:
    data = response.json()
    latitude = data['latitude']
    longitude = data['longitude']

    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Failed to get location data")
