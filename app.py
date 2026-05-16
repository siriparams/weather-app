from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = "7c619b7010adfd8b3bc73a37d5541ad3"

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form["city"]

        return redirect(url_for("weather", city=city))

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )

@app.route("/weather/<city>")
def weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    if data["cod"] == 200:

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }

        return render_template(
            "index.html",
            weather=weather_data,
            error=None
        )

    return render_template(
        "index.html",
        weather=None,
        error="City not found"
    )
if __name__ == "__main__":
    app.run(debug=True)