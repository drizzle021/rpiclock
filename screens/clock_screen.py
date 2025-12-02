#!/usr/bin/env python3
import time
import datetime
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 480, 320

def render_clock():
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except IOError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    now = datetime.datetime.now()
    # time_str = now.strftime("%H:%M:%S")
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y.%m.%d")


    bbox_time = draw.textbbox((0, 0), time_str, font=font_big)
    w_time, h_time = bbox_time[2] - bbox_time[0], bbox_time[3] - bbox_time[1]

    bbox_date = draw.textbbox((0, 0), date_str, font=font_small)
    w_date, h_date = bbox_date[2] - bbox_date[0], bbox_date[3] - bbox_date[1]


    draw.text(((WIDTH - w_time) / 2, (HEIGHT - h_time) / 2 - 40),
              time_str, font=font_big, fill="white")
    draw.text(((WIDTH - w_date) / 2, (HEIGHT - h_date) / 2 + 60),
              date_str, font=font_small, fill="#c379e8")

    return image