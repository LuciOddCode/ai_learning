from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import geocoder
from geopy.geocoders import Nominatim
import requests

load_dotenv()


def getCityCoordinates(city):
    geolocator = Nominatim(user_agent="b0e4d4263c3b455c94050950acc0b645")
    if city:
        location = geolocator.geocode(city)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find coordinates for {city}.")
            return None
    else:
        g = geocoder.ip('me')
        return g.latlng if g.latlng else (0, 0)


def getWeather(city):
    coordinates = getCityCoordinates(city)
    if not coordinates:
        return "Invalid city. Please enter a valid city name."

    lat, lon = coordinates

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch weather data. API returned status code {response.status_code}."


agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools],
    name="Simple Groq Agent",
    description="A fun weather forecaster.",
    instructions="""You are a witty weather forecaster. Use the provided weather data to generate engaging and humorous forecasts.""",
    show_tool_calls=True,
    markdown=True
)

print("Simple Groq Agent")
city = input("Enter the city name: ").strip()

weather = getWeather(city)

if isinstance(weather, dict):
    agent.print_response(str(weather))
else:
    print(weather)
