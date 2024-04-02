from datetime import datetime
import csv

class Forecast:
    def __init__(self, location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning):
        self.location = location
        self.updated_date = updated_date
        self.forecast_date = forecast_date
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.condition = condition
        self.possible_rainfall = possible_rainfall
        self.chance_of_rain = chance_of_rain
        self.forecast = forecast
        self.warning = warning

    def __str__(self):
        return f"{self.location}: Updated Date - {self.updated_date}, Forecast Date - {self.forecast_date}, Min Temp - {self.min_temp}°C, Max Temp - {self.max_temp}°C, Condition - {self.condition}, Possible Rainfall - {self.possible_rainfall} mm, Chance of Rain - {self.chance_of_rain}%, Forecast - {self.forecast}, Warning - {self.warning}"

class ForecastCollection:
    def __init__(self):
        self.forecasts = []

    def add_forecast(self, forecast):
        self.forecasts.append(forecast)

class DataAnalyzer:
    @staticmethod
    def analyze_locations(forecast_collection):
        locations = set()
        for forecast in forecast_collection.forecasts:
            locations.add(forecast.location)
        return locations

class CSVReader:
    @staticmethod
    def read_forecast_data(filename):
        forecast_collection = ForecastCollection()
        with open(filename, 'r') as file:
            next(file)  # Skip the header row
            for line in file:
                data = line.strip().split(',')
                location = data[0]
                updated_date = datetime.strptime(data[1], "%A %d %B %Y")
                forecast_date = datetime.strptime(data[2], "%A %d %B")
                min_temp = int(data[3].rstrip('°C'))
                max_temp = int(data[4].rstrip('°C'))
                condition = data[5]
                possible_rainfall = data[6].rstrip(' mm')
                chance_of_rain = int(data[7].rstrip('%'))
                forecast = data[8]
                warning = data[9]
                forecast_obj = Forecast(location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning)
                forecast_collection.add_forecast(forecast_obj)
        return forecast_collection

class Main:
    @staticmethod
    def main():
        filename = 'forecast_data.csv'
        forecast_collection = CSVReader.read_forecast_data(filename)

        # Basic data analysis
        locations = DataAnalyzer.analyze_locations(forecast_collection)
        print("Locations:", locations)

if __name__ == "__main__":
    Main.main()
