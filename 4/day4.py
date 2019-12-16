def ok_double(num_equal, strict_double):
    if strict_double:
        return num_equal == 2
    else:
        return num_equal >= 2

def ok_password(password, strict_double):
    last_digit = -1
    double_found = False
    num_equal = 0
    for digit in str(password):
        int_digit = int(digit)
        if int_digit < last_digit:
            return False
        elif not double_found:
            if int_digit == last_digit:
                num_equal += 1
            else:
                if ok_double(num_equal, strict_double):
                    double_found = True
                num_equal = 1
        last_digit = int_digit
    return double_found or ok_double(num_equal, strict_double)

with open("day4.input") as file:
    pw_range = [int(val) for val in file.read().split('-')]

valid_passwords = 0
for password in range(pw_range[0], pw_range[1] + 1):
    if ok_password(password, True):
        valid_passwords += 1

print(valid_passwords)
