import cv2
import pytesseract
import numpy as np
import re

# ✅ Path to Tesseract (update if installed elsewhere)
pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Step 1 – Load Image
# 👉 Change between "car.jpg" and "car2.jpg" for each car
img = cv2.imread("car2.jpg")
if img is None:
    print("❌ Image not found.")
    exit()

# ✅ Step 2 – Resize and Preprocess
img = cv2.resize(img, (800, 600))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edges = cv2.Canny(gray, 30, 200)

# ✅ Step 3 – Detect Number Plate Contour
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
plate = None

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4:
        plate = approx
        break

# ✅ Step 4 – Mask and Crop the Plate
if plate is not None:
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate], 0, 255, -1)
    (x, y) = np.where(mask == 255)
    (x1, y1), (x2, y2) = (np.min(y), np.min(x)), (np.max(y), np.max(x))
    crop = gray[y1:y2 + 1, x1:x2 + 1]

    # ✅ Step 5 – Enhance Cropped Plate for OCR
    crop = cv2.convertScaleAbs(crop, alpha=2.4, beta=25)
    crop = cv2.GaussianBlur(crop, (3, 3), 0)
    crop = cv2.dilate(crop, np.ones((2, 2), np.uint8), iterations=1)
    _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ✅ Step 6 – Run OCR
    config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(crop, config=config)
    text = text.strip().replace(" ", "").replace("\n", "")

    # ✅ Step 7 – General OCR Fixes
    fixes = {
        "I": "1", "A": "4", "O": "0", "S": "5", "Z": "2",
        "G": "6", "B": "8", "T": "7", "Q0": "Q", "VV": "W"
    }
    for wrong, right in fixes.items():
        text = text.replace(wrong, right)

    # ✅ Step 8 – State-Specific Corrections
    # Delhi plate: fix 0L / D1 / DI → DL
    if re.match(r'^[0D][1IL]', text):
        text = "DL" + text[2:]
    # Rajasthan plate: fix C4 → CV (common misread)
    if "RJ" in text and "C4" in text:
        text = text.replace("C4", "CV")

    # Remove non-alphanumeric leftovers
    text = re.sub(r'[^A-Z0-9]', '', text)

    # ✅ Step 9 – Apply Proper Formatting (XX 00XX 0000)
    formatted = text
    match = re.match(r'^([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{3,4})$', text)
    if match:
        formatted = f"{match.group(1)} {match.group(2)}{match.group(3)} {match.group(4)}"

    # ✅ Step 10 – Display Result
    if formatted:
        print("✅ Detected Number Plate:", formatted)
    else:
        print("⚠️ OCR could not read text clearly.")

    # Draw result on image
    cv2.drawContours(img, [plate], -1, (0, 255, 0), 3)
    cv2.putText(img, formatted if formatted else "Not Readable",
                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show outputs
    cv2.imshow("Detected Plate (Processed)", crop)
    cv2.imshow("Car with Detected Plate", img)

else:
    print("❌ No plate contour found.")

cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
