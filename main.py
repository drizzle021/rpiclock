import time
import numpy as np
from screens.clock_screen import render_clock
from screens.weather_screen import render_weather
#from screens.nba_screen import render_nba

FB_PATH = "/dev/fb1"

SCREENS = [
    {"render": render_clock, "duration": 10, "refresh": 1},
    {"render": render_weather, "duration": 10, "refresh": 10},
    # {"render": render_nba, "duration": 10, "refresh": 10}
]


def image_to_rgb565(img):
    arr = np.array(img.convert("RGB"), dtype=np.uint8)
    r = (arr[:,:,0] >> 3).astype(np.uint16)
    g = (arr[:,:,1] >> 2).astype(np.uint16)
    b = (arr[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b

    return rgb565.astype("uint16").tobytes()

def show_on_fb(img):
    with open(FB_PATH, "wb") as f:
        f.seek(0)
        f.write(image_to_rgb565(img))

def main():
    while True:
        for screen in SCREENS:
            elapsed = 0
            while elapsed < screen["duration"]:
                img = screen["render"]()
                show_on_fb(img)
                time.sleep(screen["refresh"])
                elapsed += screen["refresh"]

if __name__ == "__main__":
    main()
