import schedule
import time
import requests
from twilio.rest import Client


def get_weather(latitude, longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(base_url)
    data = response.json()
    return data


def cel_to_fahr(celsius):
    return (celsius * 9 / 5) + 32


def SMS_text(body):
    # Your Account SID from twilio.com/console
    account_sid = "twilo_sid"
    # Your Auth Token from twilio.com/console
    auth_token = "twilio_token"
    # Twilio phone number
    from_phone_number = "twilio_number"
    # Personal phone number
    to_phone_number = "personal_number"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_phone_number,
        to=to_phone_number
    )
    print("Text message sent!")


def weather_location():
    lat = 36.9741  # Latitude of Santa Cruz
    long = -122.0308  # Longitude of Santa Cruz

    weather_data = get_weather(lat, long)
    temperature_celsius = weather_data["hourly"]["temperature_2m"][0]
    relative_humidity = weather_data["hourly"]["relativehumidity_2m"][0]
    wind_speed = weather_data["hourly"]["windspeed_10m"][0]
    temperature_fahrenheit = cel_to_fahr(temperature_celsius)

    weather_print = (
        f"Good morning Anish!\n"
        f"\n"
        f"It's 8:00 a.m. and the weather in Santa Cruz is:\n"
        f"\n"
        f"Temperature: {temperature_fahrenheit:.2f}°F\n"
        f"Relative Humidity: {relative_humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    SMS_text(weather_print)


def weather_schedule():
    schedule.every().day.at("09:00").do(weather_location)
    while True:
        schedule.run_pending()
        time.sleep(1)


weather_schedule()
