import requests
import json

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key.
# You can get a free API key by signing up on the OpenWeatherMap website:
# https://openweathermap.org/api
API_KEY = 'YOUR_API_KEY'

# Base URL for the OpenWeatherMap API (current weather data)
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# --- Function to get weather data ---
def get_weather_data(city_name):
    """
    Fetches current weather data for a given city from OpenWeatherMap API.

    Args:
        city_name (str): The name of the city to get weather data for.

    Returns:
        dict or None: A dictionary containing weather data if successful,
                      otherwise None.
    """
    if not API_KEY or API_KEY == 'YOUR_API_KEY':
        print("Error: Please replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key.")
        return None

    # Construct the complete URL for the API request
    # 'q' for city name, 'appid' for API key, 'units=metric' for Celsius
    complete_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"

    try:
        # Send an HTTP GET request to the OpenWeatherMap API
        response = requests.get(complete_url)

        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if the 'cod' (code) indicates success (200)
        if data.get('cod') == 200:
            return data
        else:
            # Print error message from the API if available
            print(f"Error fetching data for {city_name}: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}") # Print response content for debugging
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response: {json_err}")
        print(f"Raw response: {response.text}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    city = input("Enter city name: ") # Prompt user for city name
    weather_data = get_weather_data(city)

    if weather_data:
        # Extract relevant information from the JSON response
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        city_name = weather_data['name']
        country = weather_data['sys']['country']

        # Print the extracted weather information
        print(f"\n--- Current Weather in {city_name}, {country} ---")
        print(f"Weather: {main_weather} ({description})")
        print(f"Temperature: {temperature}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print(f"Could not retrieve weather data for {city}.")


