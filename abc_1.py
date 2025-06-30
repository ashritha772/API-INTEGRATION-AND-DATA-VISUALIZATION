import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # type: ignore
from datetime import datetime

# Configuration
API_KEY = '593bc283fddd25b42f574abfcc22b486'  # Replace with your actual API key
CITY = 'London'
UNITS = 'metric'  # For Celsius temperatures
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# Fetch data from OpenWeatherMap API
def fetch_weather_data(city, api_key, units='metric'):
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Process the weather data into a DataFrame
def process_weather_data(weather_data):
    if not weather_data:
        return None
    
    records = []
    for forecast in weather_data['list']:
        record = {
            'datetime': datetime.fromtimestamp(forecast['dt']),
            'temp': forecast['main']['temp'],
            'feels_like': forecast['main']['feels_like'],
            'temp_min': forecast['main']['temp_min'],
            'temp_max': forecast['main']['temp_max'],
            'pressure': forecast['main']['pressure'],
            'humidity': forecast['main']['humidity'],
            'wind_speed': forecast['wind']['speed'],
            'wind_deg': forecast['wind']['deg'],
            'weather_main': forecast['weather'][0]['main'],
            'weather_desc': forecast['weather'][0]['description'],
            'clouds': forecast['clouds']['all'],
            'pop': forecast.get('pop', 0)  # Probability of precipitation
        }
        records.append(record)
    
    return pd.DataFrame(records)

# Create visualizations
def create_visualizations(df, city):
    if df is None or df.empty:
        print("No data to visualize")
        return
    
    # Set style
    sns.set_style('whitegrid')
    plt.figure(figsize=(15, 10))
    
    # Create subplots
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    
    # Plot 1: Temperature over time
    plt.subplot(2, 2, 1)
    sns.lineplot(x='datetime', y='temp', data=df, label='Temperature')
    sns.lineplot(x='datetime', y='feels_like', data=df, label='Feels Like')
    plt.title(f'Temperature Forecast for {city}')
    plt.xlabel('Date & Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    
    # Plot 2: Humidity and Pressure
    plt.subplot(2, 2, 2)
    ax1 = sns.lineplot(x='datetime', y='humidity', data=df, color='blue', label='Humidity')
    ax2 = plt.twinx()
    sns.lineplot(x='datetime', y='pressure', data=df, color='red', ax=ax2, label='Pressure')
    plt.title(f'Humidity and Pressure Forecast for {city}')
    ax1.set_xlabel('Date & Time')
    ax1.set_ylabel('Humidity (%)', color='blue')
    ax2.set_ylabel('Pressure (hPa)', color='red')
    plt.xticks(rotation=45)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    # Plot 3: Wind Speed
    plt.subplot(2, 2, 3)
    sns.barplot(x='datetime', y='wind_speed', data=df, palette='coolwarm')
    plt.title(f'Wind Speed Forecast for {city}')
    plt.xlabel('Date & Time')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45)
    
    # Plot 4: Weather Conditions
    plt.subplot(2, 2, 4)
    weather_counts = df['weather_main'].value_counts()
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('pastel'))
    plt.title(f'Weather Conditions Distribution for {city}')
    
    plt.suptitle(f'Weather Forecast Dashboard for {city}', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == '__main__':
    print("Fetching weather data...")
    weather_data = fetch_weather_data(CITY, API_KEY, UNITS)
    
    if weather_data:
        print("Processing data...")
        weather_df = process_weather_data(weather_data)
        
        if weather_df is not None:
            print("Creating visualizations...")
            create_visualizations(weather_df, CITY)
            
            # Save the data to CSV for reference
            weather_df.to_csv(f'{CITY.lower()}_weather_forecast.csv', index=False)
            print(f"Data saved to {CITY.lower()}_weather_forecast.csv")
    else:
        print("Failed to fetch weather data. Please check your API key and internet connection.")