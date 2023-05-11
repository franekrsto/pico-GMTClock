from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
import utime
from machine import Pin

# Setting up the display
display = PicoGraphics(display = DISPLAY_PICO_DISPLAY, pen_type = PEN_RGB332, rotate = 0)
display.set_font("bitmap8")

# Get the display size
width = 240
height = 135

# Set up the buttons
button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

# Setting up colours
WHITE  = display.create_pen(255, 255, 255)
BLACK  = display.create_pen(0, 0, 0)
RED    = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)

# Keep track of the hour offset
hour_offset = 0

last_press_time = utime.ticks_ms()

def display_text(text, x, y, color=(255, 255, 255)):
    display.set_pen(WHITE)
    display.text(text, x, y, width, 5)
    display.update()

def display_time():
    time = utime.localtime()
    hour = (time[3] + hour_offset) % 24
    minute = time[4]
    second = time[5]
    
    # Format the time as a string
    time_str = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    
    # Calculate the position for the text to be centered
    text_width = len(time_str) * 20
    text_height = 25
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Clear the screen
    display.set_pen(BLACK)
    display.clear()

    # Display the time
    display_text(time_str, x, y)

def increase_hour(p):
    global hour_offset, last_press_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) < 200:  # 200 ms debounce time
        return  # ignore this press
    last_press_time = current_time  # update the time of the last button press
    hour_offset += 1
    if hour_offset > 24:  # or 12 if you want to use a 12-hour clock
        hour_offset -= 24  # reset to negative to cycle correctly
    display_time()  # update the display immediately
        
def decrease_hour(p):
    global hour_offset, last_press_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) < 200:  # 200 ms debounce time
        return  # ignore this press
    last_press_time = current_time  # update the time of the last button press
    hour_offset -= 1
    if hour_offset > 24:  # or 12 if you want to use a 12-hour clock
        hour_offset -= 24  # reset to negative to cycle correctly
    display_time()  # update the display immediately

def display_date():
    current_date = utime.localtime()
    year = current_date[0]
    month = current_date[1]
    day = current_date[2]
    
    # You can adjust the position and format of the date text as needed
    date_str = "{}/{}/{}".format(day, month, year)
    display.set_pen(RED)  # Set pen color for date
    display.text(date_str, 150, 120)  # Display date
    
# Set up the buttons with interrupts
button_a.irq(increase_hour, Pin.IRQ_FALLING)
button_b.irq(decrease_hour, Pin.IRQ_FALLING)

# Main loop
while True:
    display_time()
    display_date()
    display.update()
    utime.sleep(1)  # pause for 1 second before updating the time again
