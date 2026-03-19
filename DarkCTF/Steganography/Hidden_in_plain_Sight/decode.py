s = "a9Cb2rX7aQ5cL1kP8Oe3nM4{R6Tt2Hk9iW1sJ0_Z8Iu5sF3_V7Ih6tK2!d4}"

# Pattern: CrackOn{...}
# C is at index 2
# r is at index 5
# a is at index 8
# Interval = 3

flag = ""
for i in range(2, len(s), 3):
    flag += s[i]

print(f"Decoded flag: {flag}")
