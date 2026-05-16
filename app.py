from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# -----------------------------
# API KEYS
# -----------------------------

API_KEY = "7c619b7010adfd8b3bc73a37d5541ad3"

UNSPLASH_KEY = "hcro3sjEy0ucL9ULlHRE36xi4h8mqxkeXnhvzv2_s_I"


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        city = request.form["city"]

        return redirect(url_for("weather", city=city))

    return render_template(
        "index.html",
        weather=None,
        error=None
    )


# -----------------------------
# WEATHER PAGE
# -----------------------------

@app.route("/weather/<city>")
def weather(city):

    # -----------------------------
    # GET CITY COORDINATES
    # -----------------------------

    geo_url = (
        f"http://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=1&appid={API_KEY}"
    )

    geo_response = requests.get(geo_url)

    geo_data = geo_response.json()

    # -----------------------------
    # CITY NOT FOUND
    # -----------------------------

    if not geo_data:

        return render_template(
            "index.html",
            weather=None,
            error="City not found"
        )

    # -----------------------------
    # LATITUDE & LONGITUDE
    # -----------------------------

    lat = geo_data[0]["lat"]

    lon = geo_data[0]["lon"]

    official_city = geo_data[0].get("name", city)

    # -----------------------------
    # WEATHER API
    # -----------------------------

    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    weather_response = requests.get(weather_url)

    data = weather_response.json()

    # -----------------------------
    # WEATHER NOT FOUND
    # -----------------------------

    if data["cod"] != 200:

        return render_template(
            "index.html",
            weather=None,
            error="Weather data not found"
        )

    # -----------------------------
    # UNSPLASH IMAGE
    # -----------------------------

    image_url = (
        f"https://api.unsplash.com/search/photos?"
        f"page=1&query={official_city}&client_id={UNSPLASH_KEY}"
    )

    image_response = requests.get(image_url)

    image_data = image_response.json()

    # -----------------------------
    # IMAGE FALLBACK
    # -----------------------------

    if image_data["results"]:

        city_image = (
            image_data["results"][0]["urls"]["regular"]
        )

    else:

        city_image = (
            "https://images.unsplash.com/"
            "photo-1506744038136-46273834b3fb"
        )

    # -----------------------------
    # WEATHER DATA
    # -----------------------------

    weather_data = {

        "city": official_city,

        "temperature": round(data["main"]["temp"]),

        "description": data["weather"][0]["description"],

        "humidity": data["main"]["humidity"],

        "wind": data["wind"]["speed"],

        "city_image": city_image
    }

    # -----------------------------
    # RETURN PAGE
    # -----------------------------

    return render_template(
        "index.html",
        weather=weather_data,
        error=None
    )


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)