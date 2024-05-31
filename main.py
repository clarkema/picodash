import time

from macfont import test
import writer
import waveshare.lcd as LCD

def read_co2_level():
    return 795

def exponential_moving_average(alpha, new_value, previous_average):
    return alpha * new_value + (1 - alpha) * previous_average
    
def co2_status_colour(co2_level):
    if co2_level < 800:
        return lcd.green
    elif co2_level < 1200:
        return lcd.orange
    else:
        return lcd.red

if __name__=='__main__':  
    lcd = LCD.LCD_1inch28()
    lcd.set_bl_pwm(20000)

    wtr = writer.CWriter(lcd, test, lcd.white, lcd.red, verbose=True)

    alpha = 0.5
    co2_average = read_co2_level()
      
    while(True):
        # This `round` could prove to be an issue. Investigate if there is flicking between 2 values.
        #co2_average = round(exponential_moving_average(alpha, read_co2_level(), co2_average))
        co2_average = co2_average + 1

        status_background = co2_status_colour(co2_average)
        lcd.fill(status_background)

        lcd.ellipse(120,120,100,100,lcd.black, True)
      
        co2_str = str(co2_average)
        co2_str_pixel_width = wtr.stringlen(co2_str)
        wtr.set_textpos(lcd, 90, 120 - (co2_str_pixel_width // 2))
        wtr.printstring(str(co2_average))
        lcd.show()
        time.sleep(0.2)
