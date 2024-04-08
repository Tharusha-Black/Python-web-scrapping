# Importing necessary modules
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import logging

# Class representing a forecast object
class Forecast:
    def __init__(self, *args):
        self.location, self.updated_date, self.forecast_date, self.min_temp, self.max_temp, self.condition, self.possible_rainfall, self.chance_of_rain, self.forecast, self.warning = args

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

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Scraper:
    @staticmethod
    def scrape_forecast_from_url(url):
        location = url.split('/')[-1].split('.')[0].capitalize()
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')  # Use 'html.parser' instead of 'lxml'
            
            forecast_data = []  # Initialize list to store forecast data
            
            day_elements = soup.find_all('div', class_='day')
            
            for day_element in day_elements:
                updated_date = soup.find('p', class_='date').text.strip().split('on')[-1].strip().replace('.', '')
                forecast_date = day_element.find('h2').text.strip()
                min_temp_element = day_element.find('ul').find('li', string=re.compile(r'^Min:'))
                max_temp_element = day_element.find('ul').find('li', string=re.compile(r'^Max:'))
                min_temp = min_temp_element.text.split(':')[1].strip() if min_temp_element else "N/A"
                max_temp = max_temp_element.text.split(':')[1].strip() if max_temp_element else "N/A"
                condition_element = day_element.find('ul').find('li', string=re.compile(r'(Light|Morning|Afternoon|Cloudy|Clear|Mostly|Chance of a thunderstorm|Possible shower|Slight chance of rain|Cloudy with rain expected|Chance of Showers|Possible Showers).*', re.IGNORECASE))
                condition = condition_element.text.strip() if condition_element else "N/A"
                possible_rainfall_element = day_element.find('ul').find('li', string=re.compile(r'^Possible rainfall:'))
                possible_rainfall = possible_rainfall_element.text.split(':')[1].strip() if possible_rainfall_element else "N/A"
                chance_of_rain_element = day_element.find('ul').find('li', string=re.compile(r'^Chance of any rain:'))
                chance_of_rain = chance_of_rain_element.text.split(':')[1].strip() if chance_of_rain_element else "N/A"
                forecast_element = day_element.find('div', class_='forecast').find('p')
                forecast = forecast_element.text.strip() if forecast_element else "N/A"
                warning_element = day_element.find('p', class_='alert')
                warning = warning_element.text.strip() if warning_element else "N/A"
                
                # Append forecast data to the list
                forecast_data.append((location, updated_date, forecast_date, min_temp, max_temp, condition, possible_rainfall, chance_of_rain, forecast, warning))
            
            return forecast_data
        except requests.exceptions.RequestException as e:
            logging.error("Failed to fetch HTML content from the URL: %s", url)
            logging.error("Error details: %s", e)
            return None

        
# Class for writing forecast data to a CSV file
class CSVWriter:
    @staticmethod
    def write_forecast_data(filename, forecast_collection):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, 'a', newline='') as file:  # Open the file in append mode
            writer = csv.writer(file)

            # Write the header row if file is empty
            if file.tell() == 0:
                writer.writerow(["Location", "Updated_Date", "Forecast_Date", "Min_Temp", "Max_Temp", "Condition", "Possible_Rainfall", "Chance_of_Rain", "Forecast", "Warning", "Current_Time"])

            # Write forecast data
            for forecast in forecast_collection.forecasts:
                writer.writerow([forecast.location, forecast.updated_date, forecast.forecast_date, forecast.min_temp, forecast.max_temp, forecast.condition, forecast.possible_rainfall, forecast.chance_of_rain, forecast.forecast, forecast.warning, current_time])


class Main:
    @staticmethod
    def main():
        urls = [
            "https://prog2007.it.scu.edu.au/weather/sydney.html",
            "https://prog2007.it.scu.edu.au/weather/brisbane.html",
            "https://prog2007.it.scu.edu.au/weather/melbourne.html"
        ]
        forecast_data = []  # Initialize list to store all forecast data
        for url in urls:
            forecasts = Scraper.scrape_forecast_from_url(url)
            if forecasts:
                forecast_data.extend(forecasts)

        # Convert forecast data to DataFrame
        df = pd.DataFrame(forecast_data)

        # Basic data analysis
        locations = df[0].unique() # change here to check if 'Location' column exists
        logging.info("Locations: %s", locations)
        
        # Save forecast data to CSV
        forecast_collection = ForecastCollection()
        for forecast_tuple in forecast_data:
            forecast = Forecast(*forecast_tuple)
            forecast_collection.add_forecast(forecast)
        
        CSVWriter.write_forecast_data("forecast_scraped_data.csv", forecast_collection)
        logging.info("Forecast data saved to forecast_scraped_data.csv")

if __name__ == "__main__":
    Main.main()
