from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = "7c619b7010adfd8b3bc73a37d5541ad3"
UNSPLASH_KEY = "hcro3sjEy0ucL9ULlHRE36xi4h8mqxkeXnhvzv2_s_I"

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
        image_url = f"https://api.unsplash.com/search/photos?page=1&query={city}&client_id={UNSPLASH_KEY}"

        image_response = requests.get(image_url)

        image_data = image_response.json()

        if image_data["results"]:

            city_image = image_data["results"][0]["urls"]["regular"]

        else:

            city_image = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "city_image": city_image,
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