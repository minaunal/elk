import requests
from elasticsearch import Elasticsearch
from datetime import datetime
import json
import time

# Elasticsearch ayarları
es = Elasticsearch([{'host': 'elasticsearch-mina', 'port': 9200}]) 

# OpenWeatherMap API anahtarınız
API_KEY = 'd98ab26d88c41bd5fdfa29cbbd4b3bfe'

# Şehirler
cities = [
    'Ankara', 'Istanbul', 'Izmir', 'London', 'Paris', 'Madrid', 
    'Barcelona', 'Berlin', 'Brazil', 'New York'
]

json_file_path = '/weather/weather_data.json'

def fetch_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    return response.json()

def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    while True:
        weather_data = []
        for city in cities:
            print(f'Fetching data for {city}...')
            data = fetch_weather(city)
            weather_data.append({
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'weather': data.get('weather', [{}])[0].get('description', ''),
                'temperature': data.get('main', {}).get('temp', ''),
                'humidity': data.get('main', {}).get('humidity', ''),
                'pressure': data.get('main', {}).get('pressure', '')
            })
            print(f'Data fetched for {city}.')

        save_to_json(weather_data, json_file_path)
        print(f'Weather data saved to {json_file_path}.')

        # 30 saniye bekle
        time.sleep(30)

if __name__ == '__main__':
    main()

