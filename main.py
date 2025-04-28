import cv2
import numpy as np
import time

# Camera index (0 or 1 depending on your setup)
camera_index = 1

# Open the camera once (don't reopen every time)
cap = cv2.VideoCapture(camera_index)

# Optional: Set camera exposure
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

print("The binary is: ", end="")
if not cap.isOpened():
    print("Failed to open camera")
    exit()
binary = ""
print("Capturing and checking LED every second...\nPress Ctrl+C to stop.")


while True:
    time.sleep(0.25)  # Wait 1 second before capturing again
    amount = 0
    for i in range(3):
        # Capture a frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture image")
            continue

        # Copy for drawing (we're not using this part to save or display)
        dotted_frame = frame.copy()
        height, width, _ = frame.shape

        led_found = False

        # Loop through each pixel
        for y in range(height):
            for x in range(width):
                b, g, r = frame[y, x]

                # Cast to int16 before subtracting to prevent overflow
                g, b, r = map(np.int16, [g, b, r])

                # Apply LED green detection condition
                if (g - b > 50) and (g - r > 100) and (g > 110):
                    led_found = True
                    break  # Exit loop once LED is detected

            if led_found:
                break  # Exit outer loop once LED is detected

        amount += 1 if led_found else 0
    # Print result every second
    c = "1" if (amount>=2) else "0"
    binary += c
    print(c, end="")
    # Check if last 16 characters are all '0'
    if binary[-8:] == '0' * 8:
        binary = binary[:-8]  # Remove the last 16 characters
        break
    time.sleep(0.75)

# Pad with leading zeros until length is divisible by 8
while len(binary) % 8 != 0:
    binary = binary + '0'


ascii_text = ''.join(
    chr(int(binary[i:i+8], 2))
    for i in range(0, len(binary), 8)
)

print("")
print(ascii_text)

# Cleanup
cap.release()
