import os
import requests
import datetime
import webbrowser
from dotenv import load_dotenv

class WeatherApp:
    def __init__(self):
        load_dotenv()
        self.city = None
        self._api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self._api_key:
            print("Please set OPENWEATHER_API_KEY environment variable")
            exit(1)

    def get_weather(self, test_city=None):
        city = test_city if test_city is not None else self.city
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self._api_key}&units=imperial"
        response = requests.get(url)
        weather_data = response.json()

        return weather_data
    
    def is_valid_city(self, city):
        weather_data = self.get_weather(city)
        return weather_data.get("cod") == 200

    def get_city(self):
        while True:
            user_input = input("Enter a city: ")

            if self.is_valid_city(user_input):
                self.city = user_input
                return user_input
            else:
                print("city not found")

    def extract_weather_info(self, weather_data):
        location = weather_data['name']
        temp = round(weather_data['main']['temp'])
        temp_min = round(weather_data['main']['temp_min'])
        temp_max = round(weather_data['main']['temp_max'])
        feels_like = round(weather_data['main']['feels_like'])
        description = weather_data['weather'][0]['description'].title()
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind']['deg']

        timezone_offset = weather_data['timezone']
    
        sunrise_utc = weather_data['sys']['sunrise']
        sunset_utc = weather_data['sys']['sunset']
        
        sunrise = datetime.datetime.utcfromtimestamp(sunrise_utc + timezone_offset).strftime('%I:%M %p')
        sunset = datetime.datetime.utcfromtimestamp(sunset_utc + timezone_offset).strftime('%I:%M %p')
    
        return location, temp, temp_min, temp_max, description, feels_like, humidity, wind_speed, wind_deg, sunrise, sunset
    
    def create_html(self, location, temp, temp_min, temp_max, description, feels_like, humidity, wind_speed, wind_deg, sunrise, sunset):
        html_template = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="styles.css">
        <title>Weather Dashboard</title>
    </head>
    <body>
        <header>
            <h1 class="location">{location}</h1>
            <h2 class="temperature">{temp}°</h2>
            <div class="high-and-low">
                <p>H: {temp_max}°</p>
                <p>L: {temp_min}°</p>
            </div>
        </header>

        <section class="cards">
            <div class="description card-long">
                <p class="card-header">DESCRIPTION</p>
                <p class="card-info">{description}</p>
            </div>

            <div class="feels-like card-small">
                <p class="card-header">FEELS LIKE</p>
                <p class="card-info">{feels_like}°</p>
            </div>

            <div class="humidity card-small">
                <p class="card-header">HUMIDITY</p>
                <p class="card-info">{humidity}%</p>
            </div>

            <div class="wind-speed card-long">
                <p class="card-header">WIND</p>
                <p class="card-info">Speed: {wind_speed}</p>
                <p class="card-info">Deg: {wind_deg}</p>
            </div>

            <div class="sunrise card-small">
                <p class="card-header">SUNRISE</p>
                <p class="card-info">{sunrise}</p>
            </div>

            <div class="sunset card-small">
                <p class="card-header">SUNSET</p>
                <p class="card-info">{sunset}</p>
            </div>
        </section>
    </body>
    </html>"""
        return html_template

    def generate_dashboard(self):
        weather_data = self.get_weather()
        location, temp, temp_min, temp_max, description, feels_like, humidity, wind_speed, wind_deg, sunrise, sunset = self.extract_weather_info(weather_data)
        html_content = self.create_html(location, temp, temp_min, temp_max, description, feels_like, humidity, wind_speed, wind_deg, sunrise, sunset)
        
        filename = "weather_dashboard.html"
        with open("weather_dashboard.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        
        file_path = os.path.abspath(filename)
        webbrowser.open(f"file://{file_path}")
        print(f"Dashboard generated for {location}! Check {filename}")



if __name__ == "__main__":
    weather_app = WeatherApp()
    city = weather_app.get_city()
    weather_app.generate_dashboard()
