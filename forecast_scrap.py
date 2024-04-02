# Importing necessary modules
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv

# Class representing a forecast object
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

# Class representing a collection of forecasts
class ForecastCollection:
    def __init__(self):
        self.forecasts = []

    def add_forecast(self, forecast):
        self.forecasts.append(forecast)

# Class for analyzing forecast data
class DataAnalyzer:
    @staticmethod
    def analyze_locations(forecast_collection):
        locations = set()
        for forecast in forecast_collection.forecasts:
            locations.add(forecast.location)
        return locations

# Class for scraping forecast data from URLs
class Scraper:
    @staticmethod
    def scrape_forecast_from_url(url):
        # Extracting location name from the URL
        location = url.split('/')[-1].capitalize()  
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content.decode('utf-8')
            soup = BeautifulSoup(html_content, 'html.parser')
            updated_date = soup.find('p', class_='date').text.strip().split('on')[-1].strip().replace('.', '')
            forecast_date = soup.find('div', class_='day').find('h2').text.strip()
            min_temp_element = soup.find('div', class_='day').find('ul').find('li', string=re.compile(r'^Min:'))
            max_temp_element = soup.find('div', class_='day').find('ul').find('li', string=re.compile(r'^Max:'))
            min_temp = min_temp_element.text.split(':')[1].strip() if min_temp_element else "N/A"
            max_temp = max_temp_element.text.split(':')[1].strip() if max_temp_element else "N/A"
            condition_element = soup.find('div', class_='day').find('ul').find('li', string=re.compile(r'(Light|Morning|Afternoon|Cloudy|Clear|Mostly|Chance of a thunderstorm|Possible shower|Slight chance of rain|Cloudy with rain expected|Chance of Showers|Possible Showers).*', re.IGNORECASE))
            condition = condition_element.text.strip() if condition_element else "N/A"
            possible_rainfall_element = soup.find('div', class_='day').find('ul').find('li', string=re.compile(r'^Possible rainfall:'))
            possible_rainfall = possible_rainfall_element.text.split(':')[1].strip() if possible_rainfall_element else "N/A"
            chance_of_rain_element = soup.find('div', class_='day').find('ul').find('li', string=re.compile(r'^Chance of any rain:'))
            chance_of_rain = chance_of_rain_element.text.split(':')[1].strip() if chance_of_rain_element else "N/A"
            forecast_element = soup.find('div', class_='day').find('div', class_='forecast').find('p')
            forecast = forecast_element.text.strip() if forecast_element else "N/A"
            warning_element = soup.find('div', class_='day').find('p', class_='alert')
            warning = warning_element.text.strip() if warning_element else "N/A"
            return Forecast(location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning)
        else:
            print("Failed to fetch HTML content from the URL:", url)
            return None

# Class for writing forecast data to a CSV file
class CSVWriter:
    @staticmethod
    def write_forecast_data(filename, forecast_collection):
        with open(filename, 'a', newline='') as file:  # Open the file in append mode
            writer = csv.writer(file)
            for forecast in forecast_collection.forecasts:
                writer.writerow([forecast.location, forecast.updated_date, forecast.forecast_date, forecast.min_temp, forecast.max_temp, forecast.condition, forecast.possible_rainfall, forecast.chance_of_rain, forecast.forecast, forecast.warning])

# Main class for orchestrating the scraping and saving process
class Main:
    @staticmethod
    def main():
        urls = [
            "https://prog2007.it.scu.edu.au/weather/sydney.html",
            "https://prog2007.it.scu.edu.au/weather/brisbane.html",
            "https://prog2007.it.scu.edu.au/weather/melbourne.html"
        ]
        forecast_collection = ForecastCollection()
        for url in urls:
            forecast = Scraper.scrape_forecast_from_url(url)
            if forecast:
                forecast_collection.add_forecast(forecast)

        # Basic data analysis
        locations = DataAnalyzer.analyze_locations(forecast_collection)
        print("Locations:", locations)
        
        # Save forecast data to CSV
        CSVWriter.write_forecast_data("forecast_scraped_data.csv", forecast_collection)

if __name__ == "__main__":
    Main.main()
