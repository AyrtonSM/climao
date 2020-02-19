import json
import requests as rq
from flask import Flask, request, render_template

app = Flask(__name__)
app.run(debug=True)
api_key = 'eb7daf8b6d9a3607541965d82a76ad80'

@app.route('/')
def weather_page():
    return render_template('weather.html')

@app.route('/data/weather', methods=['GET', 'POST'])
def weather():
    print('youu')
    if request.method == 'GET': 
        city = request.args.get('cidade')
        weather_response = rq.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}') 
        weather_json_data = json.loads(weather_response.text)

        

        weather_json_data['main']['temp'] = kelvinToCelcius(weather_json_data['main']['temp'])
        weather_json_data['main']['temp_min'] = kelvinToCelcius(weather_json_data['main']['temp_min'])
        weather_json_data['main']['temp_max'] = kelvinToCelcius(weather_json_data['main']['temp_max'])
        weather_json_data['main']['feels_like'] = kelvinToCelcius(weather_json_data['main']['feels_like'])


        # print(weather_json_data['main']) 


        return render_template('weather_info.html', data=weather_json_data)



def kelvinToCelcius(temp):
    celcius = (temp - 273.15)
    return round(celcius,2)