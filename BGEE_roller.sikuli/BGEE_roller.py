'''
BGEE Sikuli Auto Roller

Copyright (c) 2013 Michael Rabbitt (github.com/mrabbitt)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
'''
import logging
import sys
from os import path

reload(logging)  # Workaround from: https://answers.launchpad.net/sikuli/+question/180346#comment-17

total_roll_pattern = "Total_Roll.png"
reroll_button_pattern = "REROLL.png"
store_button_pattern = "STORE.png"
recall_button_pattern = "RECALL.png"

number_patterns = [
    (0, "number0.png"),
    (1, "number1.png"),
    (2, "number2.png"),
    (3, "number3.png"),
    (4, "number4.png"),
    (5, "number5.png"),
    (6, "number6.png"),
    (7, "number7.png"),
    (8, "number8.png"),
    (9, "number9.png"),
]

# Sizes for game running windowed at 800x600.
digit_offset_width = 12
digit_width = 12
digit_height = 12
expand_pixels = 4  # margin of error

# Thresholds
max_iterations = 999
target_value = 89

# Logging configuration
LOG_FORMAT = '%(asctime)s [%(process)d] %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO, stream=sys.stdout)
if getBundlePath() is not None and getBundlePath().endswith('.sikuli'):
    # Place log file next to .sikuli file.
    log_path = path.join(path.dirname(path.abspath(getBundlePath())), 'BGEE_roller.log')
    handler = logging.FileHandler(filename=log_path, encoding='UTF-8', mode='a')
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.root.addHandler(handler)
    logging.debug('Logging to: %s', log_path)
                        
def get_digits_in_region(region):
    found_numbers = []
    # TODO Can this be parallelized?
    for number_pattern in number_patterns:
        if region.exists(number_pattern[1], 0.001):
            found_numbers.append(number_pattern[0])
    return found_numbers

# Find total roll region
def get_roll_value():
    wait(total_roll_pattern)
    total_roll = find(total_roll_pattern)

    tens_digit_region = Region(
        int(total_roll.getTopRight().getX() - expand_pixels),
        int(total_roll.getTopRight().getY() - expand_pixels) - 1,
        digit_width + (2 * expand_pixels), 
        digit_height+ (2 * expand_pixels)
    )
    ones_digit_region = Region(
        int(total_roll.getTopRight().getX() - expand_pixels) + digit_offset_width,
        int(total_roll.getTopRight().getY() - expand_pixels) - 1,
        digit_width + (2 * expand_pixels), 
        digit_height + (2 * expand_pixels)
    )
    
    tens_digits = get_digits_in_region(tens_digit_region)
    ones_digits = get_digits_in_region(ones_digit_region)
    if len(tens_digits) == len(ones_digits) == 1:
        roll_value = tens_digits[0] * 10 + ones_digits[0]
        return roll_value
    else:
        logging.error('Mutiple matches. tens: %s, ones: %s', tens_digits, ones_digits)
        if len(tens_digits) != 1:
            tens_digit_region.highlight(3)
        if len(ones_digits) != 1:
            ones_digit_region.highlight(3)
        return 0


# Main runtime loop.
logging.info("Starting with max_iterations=%d, target_value=%d", max_iterations, target_value)

try:
    click(store_button_pattern)
    current_top = get_roll_value()
    logging.info("Stored initial top value:  %d", current_top)

    for i in xrange(1, max_iterations+1):
        click(reroll_button_pattern)
        current_value = get_roll_value()
    
        if current_value > current_top:
            click(store_button_pattern)
            current_top = current_value
            logging.info("Roll #%d: Stored new top value:  %d", i, current_top)
    
            if current_top >= target_value:
                break;
        else:
            logging.info("Roll #%d: Rolled total value of: %d (stored top value: %d)", 
                         i, current_value, current_top)
            
    
    click(recall_button_pattern)
    logging.info("Done, recalled top roll of %s!", current_top)

except:
    logging.exception('Unexpected exception occurred.')
    raise