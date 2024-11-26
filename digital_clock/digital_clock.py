import tkinter as tk
import time
import requests
import urllib.parse  # For encoding city names

# Function to get the user's current location (city)
def get_location():
    try:
        # Fetch location data using ipinfo.io
        location_url = 'https://ipinfo.io/json'
        response = requests.get(location_url, timeout=5)
        location_data = response.json()
        
        # Extract city from location data
        city = location_data.get('city', 'Unknown')
        return city
    except Exception:
        return "Unknown"

# Function to get weather information based on the city without an API key
def get_weather(city):
    try:
        # Encode the city name to handle spaces and special characters
        encoded_city = urllib.parse.quote(city)
        
        # Fetch weather data from wttr.in
        weather_url = f"https://wttr.in/{encoded_city}?format=%C+%t"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(weather_url, headers=headers, timeout=5)
        
        # Return the weather data as a string
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
        else:
            return "Weather data unavailable"
    except Exception as e:
        return f"Error fetching weather: {e}"

# Function to update the time
def time_update():
    # Get the current time in the format HH:MM:SS
    current_time = time.strftime('%H:%M:%S')
    
    # Update the time on the label
    time_label.config(text=current_time)
    
    # Call the time_update function again after 1000 ms (1 second)
    time_label.after(1000, time_update)

# Create the root window
root = tk.Tk()
root.title("Digital Clock with Location and Weather")

# Set the size of the window
root.geometry("400x350")

# Set the background color of the window
root.config(bg="black")

# Create a label widget to display the time
time_label = tk.Label(root, font=("calibri", 40, 'bold'), background="black", foreground="white")
time_label.pack(anchor='center')

# Create a label widget to display the location
location_label = tk.Label(root, font=("calibri", 14, 'bold'), background="black", foreground="white")
location_label.pack(anchor='center', pady=10)

# Create a label widget to display the weather
weather_label = tk.Label(root, font=("calibri", 14, 'bold'), background="black", foreground="white")
weather_label.pack(anchor='center', pady=10)

# Display the user's location and weather
city = get_location()
if city and city != "Unknown":
    location_label.config(text=f"Location: {city}")
    # Get and display the weather information
    weather_info = get_weather(city)
    weather_label.config(text=f"Weather: {weather_info}")
else:
    location_label.config(text="Location: Unable to detect location")
    weather_label.config(text="Weather: Unable to fetch weather")

# Call the time_update function to initialize the clock
time_update()

# Run the application
root.mainloop()
