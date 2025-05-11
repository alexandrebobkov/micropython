import machine
from machine import Pin
import time, math

ONBOARD_LED = 10	# GPIO10, PIN 7
ONBOARD_BTN = 3		# GPIO3, 13

# Configure on-board LED and push button
# Stated GPIOs correspond to the wiring schematic
#onboard_led = Pin(ONBOARD_LED, Pin.OUT)
onboard_button = Pin(ONBOARD_BTN, Pin.IN, Pin.PULL_UP)

led = machine.PWM(ONBOARD_LED, freq=1000)

def pulse(l, t):
    for i in range(20):
        l.duty(int(math.sin(i/10 * math.pi) * 500 + 500))
        time.sleep_ms(t)
    l.duty(0)
        
# Interrupt function to turn LED ON when on-board button is pressed
def button_interrupt(pin):
    pulse(led, 70)
        
#pulse(led, 50)
        
def main():
    
    # Assign interrupt to the on-board push button
    onboard_button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt)
    
if __name__ == '__main__':
    main()