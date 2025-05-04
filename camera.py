import cv2
import numpy as np
import time

# Camera index (0 or 1 depending on your setup)
camera_index = 0

# Open the camera once (don't reopen every time)
cap = cv2.VideoCapture(camera_index)
started = False
# Optional: Set camera exposure
#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
#cap.set(cv2.CAP_PROP_EXPOSURE, -6)

print("The binary is: ", end="")
if not cap.isOpened():
    print("Failed to open camera")
    exit()
binary = ""
print("Capturing and checking LED every second...\nPress Ctrl+C to stop.")


for _ in range(5):  # Grab a few dummy frames first
    cap.read()

while True:
    a = time.time()
    time.sleep(0.25)  # Wait 1 second before capturing again
    amount = 0
    for i in range(5):
        # Capture a frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture image")
            continue

        # Copy for drawing (we're not using this part to save or display)
        height, width, _ = frame.shape

        # Loop through each pixel
        frame = frame.astype(np.int16)
        b,g,r = cv2.split(frame)
        led_mask = ((g - b) > 50) & ((g - r) > 80) & (g > 90)
        led_found = np.any(led_mask)
        amount += 1 if led_found else 0
    # Print result every second
    c = "1" if (amount>=3) else "0"
    binary += c
    if c == "1" and not started:
        started = True
        binary = ""
    print(c, end="")
    # Check if last 16 characters are all '0'
    if binary[-16:] == '0' * 16:
        binary = binary[:-16]  # Remove the last 16 characters
        started = False
        # Pad with leading zeros until length is divisible by 8
        while len(binary) % 8 != 0:
            binary = binary + '0'

        ascii_text = ''.join(
            chr(int(binary[i:i + 8], 2))
            for i in range(0, len(binary), 8)
        )

        print("")
        print(ascii_text)
        binary = ""
        continue
    b = time.time()
    time.sleep(1-(b-a))



# Cleanup
cap.release()
