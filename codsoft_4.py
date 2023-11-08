from flask import Flask, render_template, request
import requests
import re
from datetime import datetime
import configparser


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('API_KEY', 'key')


@app.route('/')
def index():
    return render_template('weather.html')


@app.route('/weather/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        place = request.form['place']
        zip_pattern = r"\d{5}"
        if re.match(zip_pattern, place):
            url = f"https://api.openweathermap.org/data/2.5/weather?zip={place}&units=metric&appid={api_key}"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&units=metric&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                name = data["name"]
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"]
                speed_ms = data["wind"]["speed"]
                speed = speed_ms * 3.6
                now = datetime.now()
                current_date = now.strftime("%d-%m-%y %H:%M:%S")
                return render_template('result.html', date=current_date, name=name, temperature=temperature,
                                       humidity=humidity, wind_speed=speed, weather_description=description)
            except KeyError as ke:
                error = "Error Occured:" + str(ke)
                return render_template('result.html', error=error)
        else:
            error = "Error occurred while fetching data from the OpenWeatherMap API"
            return render_template('result.html', error=error)

    else:
        render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
