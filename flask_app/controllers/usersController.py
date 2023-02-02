from flask_app import app
from flask import render_template, request, redirect, session
import requests
from flask_app.models import user


@app.route("/user/home")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    else:
        weather_dict = {}
        zipcode = user.User.getZipcode({"id": session["user_id"]})
        zipcode = zipcode[0]["zip_code"]
        print(zipcode)

        api_key = "cf0c83b7515cbb1124c6ea2cb079ef6c"
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={api_key}&units=imperial"
        )
        print(weather_data.json())
        weather = weather_data.json()["weather"][0]["description"]
        temp = round(weather_data.json()["main"]["temp"])
        humidity = weather_data.json()["main"]["humidity"]
        city = weather_data.json()["name"]
        weather_dict = {
            "weather": weather,
            "temp": temp,
            "humidity": humidity,
            "city": city,
        }

        return render_template(
            "pages/dashboard.html",
            current_user=user.User.getById({"id": session["user_id"]}),
            weather=weather_dict,
        )


{
    "coord": {"lon": -81.5354, "lat": 39.2644},
    "weather": [
        {"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}
    ],
    "base": "stations",
    "main": {
        "temp": 24.87,
        "feels_like": 24.87,
        "temp_min": 23.59,
        "temp_max": 26.58,
        "pressure": 1027,
        "humidity": 76,
    },
    "visibility": 10000,
    "wind": {"speed": 1.12, "deg": 301, "gust": 1.16},
    "clouds": {"all": 100},
    "dt": 1675317670,
    "sys": {
        "type": 2,
        "id": 2007769,
        "country": "US",
        "sunrise": 1675341147,
        "sunset": 1675378027,
    },
    "timezone": -18000,
    "id": 0,
    "name": "Parkersburg",
    "cod": 200,
}
