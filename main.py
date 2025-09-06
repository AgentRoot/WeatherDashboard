import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "cafbfe3eef7a43aaaae64442250609"
URL = "https://api.weatherapi.com/v1/current.json"

def get_weather():
    city = city_entry.get()
    main_url = f"{URL}?key={API_KEY}&q={city}"
    response = requests.get(main_url)
    data = response.json()
    
    if "error" in data:
        result_label.config(text="❌ City not found!", fg="red")
        icon_label.config(image="")
        feels_like_label.config(text="")
        humidity_label.config(text="")
        wind_label.config(text="")
    else:
        location = data['location']
        current = data['current']

        # Main info
        temp = f"{current['temp_c']}°C"
        condition = current['condition']['text']
        icon_url = "https:" + current['condition']['icon']

        # Update main weather text
        result_label.config(
            text=f"{location['name']}, {location['country']}\n{temp} | {condition}",
            fg="white"
        )

        # Update detailed weather info
        feels_like_label.config(text=f"Feels Like: {current['feelslike_c']}°C")
        humidity_label.config(text=f"Humidity: {current['humidity']}%")
        wind_label.config(text=f"Wind: {current['wind_kph']} kph ({current['wind_dir']})")

        # Fetch and update weather icon
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo  # Keep reference

# Tkinter window setup
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("400x400")
root.configure(bg="#1e1e1e")

# City entry
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

# Search button
search_btn = tk.Button(root, text="Search", font=("Segoe UI", 12), command=get_weather)
search_btn.pack(pady=5)

# Weather icon
icon_label = tk.Label(root, bg="#1e1e1e")
icon_label.pack(pady=10)

# Main weather result
result_label = tk.Label(root, font=("Segoe UI", 14), bg="#1e1e1e", fg="white")
result_label.pack(pady=5)

# Detailed weather info labels
feels_like_label = tk.Label(root, font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
feels_like_label.pack(pady=2)

humidity_label = tk.Label(root, font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
humidity_label.pack(pady=2)

wind_label = tk.Label(root, font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
wind_label.pack(pady=2)

root.mainloop()
