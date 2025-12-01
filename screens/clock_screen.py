#!/usr/bin/env python3
import time
import datetime
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 480, 320

def render_clock():
    # Create blank image
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except IOError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Current time/date
    now = datetime.datetime.now()
    # time_str = now.strftime("%H:%M:%S")
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y.%m.%d")

    # Measure text sizes
    bbox_time = draw.textbbox((0, 0), time_str, font=font_big)
    w_time, h_time = bbox_time[2] - bbox_time[0], bbox_time[3] - bbox_time[1]

    bbox_date = draw.textbbox((0, 0), date_str, font=font_small)
    w_date, h_date = bbox_date[2] - bbox_date[0], bbox_date[3] - bbox_date[1]

    # Draw centered text
    draw.text(((WIDTH - w_time) / 2, (HEIGHT - h_time) / 2 - 40),
              time_str, font=font_big, fill="white")
    draw.text(((WIDTH - w_date) / 2, (HEIGHT - h_date) / 2 + 60),
              date_str, font=font_small, fill="#c379e8")

    return image

def update_framebuffer(image):
    # Convert to RGB565 (16-bit)
    arr = np.array(image.convert("RGB"), dtype=np.uint8)
    r = (arr[:,:,0] >> 3).astype(np.uint16)
    g = (arr[:,:,1] >> 2).astype(np.uint16)
    b = (arr[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b

    # Write to framebuffer
    with open(FB_DEVICE, "wb") as f:
        f.seek(0)
        f.write(rgb565.astype("uint16").tobytes())

