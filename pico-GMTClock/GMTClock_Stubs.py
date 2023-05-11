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
    # Get the current time in GMT using the utime.localtime() function
    # Adjust the hour based on the hour_offset variable    
    # Format the time as a string
    # You can also use the string's format method to add leading zeros to single-digit numbers
    
    # Calculate the position for the text to be centered on the display
    
    # Clear the screen to the background color and use the display's set_pen method to set the color    
    # Display the time on the screen using the display_text function

def increase_hour(p):
    # You need to increase the hour_offset and avoid bouncing
    
    # Check if the time since the last button press is less than the debounce time
    # If it is, this button press should be ignored
    # If the button press is valid, increase the hour_offset by 1
    # If the hour_offset is greater than 24, reset it to 0
    
    # Finally, call the display_time function to update the display immediately
        
def decrease_hour(p):
    # This function is very similar to the increase_hour function
    # The only difference is that you should decrease the hour_offset instead of increasing it

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

