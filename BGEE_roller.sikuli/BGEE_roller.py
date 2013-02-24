total_roll_pattern = "Total_Roll.png"
reroll_button_pattern = "REROLL.png"
store_button_pattern = "STORE.png"
recall_button_pattern = "REQALL.png"

number_patterns = [
    (0, "number0.png"),
    (1, "number1.png"),
    (2, "number2.png"),
    (3, Pattern("number3.png").similar(0.87)),
    (4, "number4.png"),
    (5, Pattern("number5.png").similar(0.85)),
    (6, "number6.png"),
    (7, "number7.png"),
    (8, "number8.png"),
    (9, "number9.png"),
]

# Numbers are roughly 12 x 15
digit_offset_width = 14
digit_width = 14
digit_height = 15
expand_pixels = 4  # margin of error

# Thresholds
max_iterations = 10
target_value = 89


def get_digits_in_region(region):
    found_numbers = []
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
        print 'ERROR: Mutiple matches. tens:', tens_digits, ', ones: ', ones_digits
        if len(tens_digits) != 1:
            tens_digit_region.highlight(3)
        if len(ones_digits) != 1:
            ones_digit_region.highlight(3)
        return 0

# Main runtime loop.
current_top = 0
click(store_button_pattern)

for i in xrange(0, max_iterations):
    current_value = get_roll_value()

    if current_value > current_top:
        click(store_button_pattern)
        current_top = current_value
        print i, ": Stored new top value: ", current_top

        if current_top >= target_value:
            break;
    else:
        print i, ": Rolled a max value of: ", current_value 
        
    click(reroll_button_pattern)

click(recall_button_pattern)
print "Done, recalled top roll of ", current_top
