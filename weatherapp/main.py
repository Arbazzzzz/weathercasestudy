from flask import Flask, render_template, request
from urllib.parse import quote as url_quote

import requests

app = Flask(__name__)

API_KEY = "bd5e378503939ddaee76f12ad7a97608"  # Replace with your valid API key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    if not city:
        return render_template('home.html', error="Please enter a city name.")
    
    # Construct the URL for the weather API request
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if the 'name' key exists in the response
        if 'name' in data:
            weather_data = {
                'city': data['name'],  # The city name from the response
                'temperature': data['main']['temp'],  # Temperature from the 'main' key
                'description': data['weather'][0]['description'],  # Weather description
                'icon': data['weather'][0]['icon']  # Weather icon
            }
            return render_template('weather.html', weather=weather_data)
        else:
            return render_template('home.html', error="Unexpected data format from API.")
    else:
        # If the API response status code isn't 200, show error
        if response.status_code == 404:
            return render_template('home.html', error="City not found. Please try again.")
        else:
            return render_template('home.html', error="An error occurred. Please try again later.")

if __name__ == '__main__':
    app.run(debug=True)
