import os, json, requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OWM_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CACHE_DIR = "weather_cache"
ICON_DIR = "assets/1x"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_location():
    try:
        r = requests.get("http://ip-api.com/json/", timeout=8)
        data = r.json()
        return data["lat"], data["lon"]
    except Exception:
        return None, None

def kelvin_to_celsius(k): return round(k - 273.15)

def get_today_weather(lat, lon):
    today = datetime.now().strftime("%d.%m.%Y")
    cache_path = os.path.join(CACHE_DIR, f"weather_{today}.json")
    data = None

    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            data = json.load(f)
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
        r = requests.get(url, timeout=8)
        data = r.json()
        if r.status_code == 200:
            with open(cache_path, "w") as f:
                json.dump(data, f)

    if data:
        temp = kelvin_to_celsius(data["main"]["temp"])
        temp_min = kelvin_to_celsius(data["main"]["temp_min"])
        temp_max = kelvin_to_celsius(data["main"]["temp_max"])
        condition = data["weather"][0]["description"].title()
        return condition, temp, temp_min, temp_max

ICON_MAP = {
    "Clear": "clear.png",
    "Clouds": "cloudy.png",
    "Fog": "fog.png",
    "Mist": "fog.png",
    "Smoke": "fog.png",
    "Haze": "fog.png",
    "Dust": "fog.png",
    "Sand": "fog.png",
    "Ash": "fog.png",
    "Squall": "fog.png",
    "Tornado": "fog.png",
    "Rain": "rain.png",
    "Drizzle": "rain.png",
    "Snow": "snow.png",
    "Thunderstorm": "thunder.png",
    "Thunder": "thunder.png",
    "Wind": "wind.png"
}

def get_icon_for_condition(condition):
    key = condition.split()[0]
    filename = ICON_MAP.get(key)
    if filename:
        return os.path.join(ICON_DIR, filename)
    return None

def draw_text_center(draw, text, center_xy, font, fill):
    w, h = draw.textbbox((0,0), text, font=font)[2:]
    draw.text((center_xy[0]-w//2, center_xy[1]-h//2), text, font=font, fill=fill)

def render_weather():
    W, H = 480, 320
    bg = Image.new("RGBA", (W, H), (15, 18, 25, 255))
    draw = ImageDraw.Draw(bg)

    try:
        font_path = r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_medium = ImageFont.truetype(font_path, 24)
        font_large  = ImageFont.truetype(font_path, 48)
    except IOError:
        font_medium = ImageFont.load_default()
        font_large  = ImageFont.load_default()

    lat, lon = get_location()
    condition, temp, temp_min, temp_max = get_today_weather(lat, lon)
    date_str = datetime.now().strftime("%Y.%m.%d")

    draw_text_center(draw, date_str, (W//2, 40), font_medium, (240,240,240))

    icon_path = get_icon_for_condition(condition)
    if icon_path and os.path.exists(icon_path):
        icon_img = Image.open(icon_path).convert("RGBA")
        icon_img.thumbnail((120, 120), Image.LANCZOS)
        bg.alpha_composite(icon_img, (W//2 - icon_img.width//2, 70))
    else:
        draw.rectangle([W//2 - 60, 70, W//2 + 60, 190], fill=(255,0,0))

    draw_text_center(draw, f"{temp}°C", (W//2, 190), font_large, (255,255,255))
    draw_text_center(draw, f"{temp_min}°C | {temp_max}°C", (W//2, 230), font_medium, (180,180,180))
    draw_text_center(draw, condition, (W//2, 270), font_medium, "#c379e8")

    return bg