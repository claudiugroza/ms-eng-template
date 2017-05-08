import Adafruit_DHT as DHT_SENSOR
import plotly.plotly as plot
from plotly import tools
import plotly.graph_objs as go
import json
import time
import datetime

PIN = 4
SENSOR_TYPE = DHT_SENSOR.DHT22
DELAY = 5


def main():
    with open('./credentials.json') as credentials_file:
        plotly_user_config = json.load(credentials_file)

    # autentificare folosing credentialele extrase
    plot.sign_in(plotly_user_config["plotly_username"],plotly_user_config["plotly_api_key"])

    # definire sub forma de cheie-valoare
    stream_temp_id = dict(token=plotly_user_config['plotly_streaming_tokens'][0])
    stream_humidity_id = dict(token=plotly_user_config['plotly_streaming_tokens'][1])

    # definire trase
    trace_temperature = go.Scatter(x=[],y=[],stream=stream_temp_id,yaxis='y')
    trace_humidity = go.Scatter(x=[],y=[],stream=stream_humidity_id,yaxis='y')

    # construire grafic principal
    figure = tools.make_subplots(rows=1, cols=2)
    # adaugare trase in graficul principal
    figure.append_trace(trace_temperature, 1, 1)
    figure.append_trace(trace_humidity, 1, 2)
    # configurare dimensiune si titlu
    figure['layout'].update(height=300, width=600, title='Temperatura & Umiditate')

    plot_url = plot.plot(figure, filename='DHT22_stream')
    print 'Urmareste graficul la adresa:', plot_url

    # definire flux de scriere
    temperature_stream = plot.Stream(plotly_user_config['plotly_streaming_tokens'][0])
    humidity_stream = plot.Stream(plotly_user_config['plotly_streaming_tokens'][1])

    # deschidere a fluxurilor pentru scriere
    temperature_stream.open()
    humidity_stream.open()

    while True:
        # citire caracteristici
        humidity, temperature = DHT_SENSOR.read_retry(SENSOR_TYPE, PIN)

        if temperature is not None and humidity is not None:
            # afisam citirea curenta
            print('Temperatura = {0:0.1f} | Umiditate = {1:0.1f}%'.format(temperature, humidity))

            # scriere date in fluxul aferent
            temperature_stream.write({'x': datetime.datetime.now(), 'y': temperature})
            humidity_stream.write({'x': datetime.datetime.now(), 'y': humidity})
        else:
            print 'A aparut o eroare.'

        time.sleep(DELAY)

main()
