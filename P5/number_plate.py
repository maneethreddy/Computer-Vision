import cv2, pytesseract, numpy as np, re

# ✅ Path to Tesseract (check this path if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Step 1 – Choose which image to test
# Change between "car.jpg" and "car2.jpg" when you present
img = cv2.imread("car2.jpg")
if img is None:
    print("❌  Image not found.")
    exit()

# ✅ Step 2 – Pre-processing
img = cv2.resize(img, (800, 600))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edges = cv2.Canny(gray, 30, 200)

# ✅ Step 3 – Find the number-plate contour
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
plate = None
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4:
        plate = approx
        break

# ✅ Step 4 – Crop the plate area
if plate is not None:
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate], 0, 255, -1)
    (x, y) = np.where(mask == 255)
    (x1, y1), (x2, y2) = (np.min(y), np.min(x)), (np.max(y), np.max(x))
    crop = gray[y1:y2 + 1, x1:x2 + 1]

    # ✅ Step 5 – Enhance image for OCR
    crop = cv2.convertScaleAbs(crop, alpha=2.3, beta=30)
    crop = cv2.GaussianBlur(crop, (3, 3), 0)
    crop = cv2.dilate(crop, np.ones((2, 2), np.uint8), iterations=1)
    _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ✅ Step 6 – OCR with Tesseract
    config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(crop, config=config)
    text = text.strip().replace(" ", "").replace("\n", "")

    # ✅ Step 7 – General OCR corrections
    swaps = {
        "I": "1", "A": "4", "O": "0", "S": "5", "Z": "2",
        "G": "6", "B": "8", "T": "7", "Q0": "Q"
    }
    for a, b in swaps.items():
        text = text.replace(a, b)
    text = re.sub(r'[^A-Z0-9]', '', text)

    # ✅ Step 8 – Delhi-specific fix: 0L / D1 / DI → DL
    if re.match(r'^[0D][1IL]', text):
        text = "DL" + text[2:]

    # ✅ Step 9 – Apply Indian plate spacing format
    formatted = text
    m = re.match(r'^([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{3,4})$', text)
    if m:
        formatted = f"{m.group(1)} {m.group(2)}{m.group(3)} {m.group(4)}"

    # ✅ Step 10 – Show results
    if formatted:
        print("✅  Detected Number Plate:", formatted)
    else:
        print("⚠️  OCR could not read text clearly.")

    cv2.drawContours(img, [plate], -1, (0, 255, 0), 3)
    cv2.putText(img, formatted if formatted else "Not Readable",
                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Detected Plate (Processed)", crop)
    cv2.imshow("Car with Detected Plate", img)
else:
    print("❌  No plate contour found.")

cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
