from datetime import datetime
import chardet
import csv

class Forecast:
    def __init__(self, location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning):
        """
        Initialize Forecast object with provided attributes.

        Args:
        - location (str): The location for which forecast is made.
        - updated_date (datetime): The date when the forecast was updated.
        - forecast_date (datetime): The date of the forecast.
        - min_temp (int): The minimum temperature forecasted.
        - max_temp (int): The maximum temperature forecasted.
        - condition (str): The weather condition.
        - possible_rainfall (float): The possible rainfall in millimeters.
        - chance_of_rain (int): The chance of rain in percentage.
        - forecast (str): The forecast details.
        - warning (str): Any warning associated with the forecast.
        """
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
        """
        Return a string representation of the Forecast object.
        """
        return f"{self.location}: Updated Date - {self.updated_date}, Forecast Date - {self.forecast_date}, Min Temp - {self.min_temp}°C, Max Temp - {self.max_temp}°C, Condition - {self.condition}, Possible Rainfall - {self.possible_rainfall} mm, Chance of Rain - {self.chance_of_rain}%, Forecast - {self.forecast}, Warning - {self.warning}"

class ForecastCollection:
    def __init__(self):
        """
        Initialize ForecastCollection object to hold multiple forecasts.
        """
        self.forecasts = []

    def add_forecast(self, forecast):
        """
        Add a forecast to the collection.

        Args:
        - forecast (Forecast): The Forecast object to add.
        """
        self.forecasts.append(forecast)

class DataAnalyzer:
    @staticmethod
    def analyze_locations(forecast_collection):
        """
        Analyze the unique locations present in the forecast collection.

        Args:
        - forecast_collection (ForecastCollection): The collection of forecasts.

        Returns:
        - set: A set containing unique locations.
        """
        locations = set()
        for forecast in forecast_collection.forecasts:
            locations.add(forecast.location)
        return locations

class CSVReader:
    @staticmethod
    def read_forecast_data(filename):
        """
        Read forecast data from a CSV file.

        Args:
        - filename (str): The name of the CSV file containing forecast data.

        Returns:
        - ForecastCollection: A collection of forecasts read from the file.
        """
        forecast_collection = ForecastCollection()
        try:
            with open(filename, 'rb') as file:  # Open the file in binary mode
                # Use chardet to detect the encoding
                rawdata = file.read()
                encoding = chardet.detect(rawdata)['encoding']
            with open(filename, 'r', encoding=encoding) as file:  # Use detected encoding
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    try:
                        location = row[0]
                        updated_date = datetime.strptime(row[1], "%A %d %B %Y")
                        forecast_date = datetime.strptime(row[2], "%A %d %B")
                        min_temp = int(row[3].rstrip('°C'))
                        max_temp = int(row[4].rstrip('°C'))
                        condition = row[5]
                        possible_rainfall = row[6].rstrip(' mm')
                        chance_of_rain = int(row[7].rstrip('%'))
                        forecast = row[8]
                        warning = row[9]
                        forecast_obj = Forecast(location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning)
                        forecast_collection.add_forecast(forecast_obj)
                    except (ValueError, IndexError, TypeError) as e:
                        print(f"Error processing row: {row}. Reason: {e}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return forecast_collection

class Main:
    @staticmethod
    def main():
        """
        Main function to run the program.
        """
        filename = 'forecast_data.csv'
        forecast_collection = CSVReader.read_forecast_data(filename)

        # Basic data analysis
        locations = DataAnalyzer.analyze_locations(forecast_collection)
        print("Locations:", locations)

if __name__ == "__main__":
    Main.main()
