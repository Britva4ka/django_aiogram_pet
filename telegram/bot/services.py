import io
import csv
from pyowm import OWM
from pyowm.utils import config
from pyowm.commons.exceptions import NotFoundError
from table2ascii import table2ascii as t2a, PresetStyle, Alignment
from django.conf import settings
import datetime
from .utils import translate_to_emoji
from typing import List, Dict

owm = OWM(settings.OWM_API_TOKEN)

mgr = owm.weather_manager()
cfg = config.get_default_config()
cfg['language'] = 'en'


class ForecastManager:
    """
    Class for collecting weather data by OWM API and reformat it to some format

    !!! get_forecast method can return None, so u must remember it if u want to add new methods using this one. !!!
    (if not forecast_data:)

    """
    @staticmethod
    def get_forecast(lat: float, lon: float) -> List[Dict] or None:
        """

        :param lat: latitude
        :param lon: longitude
        :return: list of dicts or None
        """
        try:
            # forecast for every 3 hours, 8 times (24 hours)
            three_h_forecast = mgr.forecast_at_coords(lat, lon, '3h', 8)
        except NotFoundError:
            return None
        else:
            filtered_fc = three_h_forecast.forecast.weathers
            forecast_data = []
            for weather in filtered_fc:
                data = {
                    'time': datetime.datetime.fromtimestamp(weather.reference_time()).strftime("%H"),
                    'temperature': weather.temperature('celsius')['temp'],
                    'feels_like': weather.temperature('celsius')['feels_like'],
                    'humidity': weather.humidity,
                    'status': weather.detailed_status,
                    'wind_speed': weather.wind()['speed'],
                    'rain': weather.rain['3h'] if '3h' in weather.rain else '---'
                }
                forecast_data.append(data)

            return forecast_data

    def create_message(self, lat, lon) -> str:
        """
        Create string. (text message)
        :return: string
        """
        forecast_data = self.get_forecast(lat, lon)
        if not forecast_data:
            return "Not found forecast for your location"
        else:
            body = [["⏰", "🌡️", "💧", "☁️", "💨", "🌧️"]]
            body.extend([
                      [f"{weather['time']}h",
                       f"{round(float(weather['temperature']))}°C",
                       f"{weather['humidity']}%",
                       f"{translate_to_emoji(weather['status'])}",
                       f"{round(float(weather['wind_speed']), 1)}m/s",
                       f"{weather['rain']}"] for weather in forecast_data])
            tbl = t2a(
                body=body,
                column_widths=[4, 4, 4, 6, 6, 6],
                cell_padding=0,
                style=PresetStyle.ascii_minimalist,
                alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER,
                            Alignment.CENTER, Alignment.CENTER, Alignment.RIGHT],
            )
            return tbl

    def create_csv(self, lat, lon) -> io.BytesIO:
        """
        create csv file
        :return: csv in bytes
        """
        forecast_data = self.get_forecast(lat, lon)
        output = io.StringIO()
        if not forecast_data:
            fieldnames = ["ERROR"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({"ERROR": "Not found forecast for your location."})
            return io.BytesIO(output.getvalue().encode())

        fieldnames = ["⏰", "🌡️", "💧", "☁️", "💨", "🌧️"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for data in forecast_data:
            forecast = {
                "⏰": data["time"]+"h",
                "🌡️": str(data['temperature'])+"°C",
                "💧": str(data['humidity'])+"%",
                "☁️": translate_to_emoji(data['status']),
                "💨": str((data['wind_speed']))+"m/s",
                "🌧️": data['rain'],
            }
            writer.writerow(forecast)

        return io.BytesIO(output.getvalue().encode())
