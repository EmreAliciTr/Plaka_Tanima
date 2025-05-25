import cv2
import imutils
import easyocr
import re
import math
import numpy as np
import os
from datetime import datetime

# OCR motoru (EasyOCR)
reader = easyocr.Reader(['tr', 'en'])

# Klasör ayarları
save_dir = "captured_plates"
image_folder = "plates_to_read"
os.makedirs(save_dir, exist_ok=True)

# Tespit edilen plakalar { "plate_text": {"count": int, "image": np.array} }
detected_plates = {}

# Kamera başlat
cap = cv2.VideoCapture(0)

# Küçük görsel ayarları
thumb_w, thumb_h = 200, 60
spacing = 10
thumbs_per_row = 4

def is_valid_plate(text):
    text = text.upper()
    if len(text) < 5 or len(text) > 12:
        return False
    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    return letters >= 2 and digits >= 2

def create_plate_thumbnail_with_texts(plate_img, text, count):
    plate_img_resized = cv2.resize(plate_img, (thumb_w, thumb_h))
    total_h = thumb_h + 40
    thumb_with_texts = np.ones((total_h, thumb_w), dtype=np.uint8) * 255
    thumb_with_texts[20:20 + thumb_h, 0:thumb_w] = plate_img_resized
    thumb_with_texts[0:20, :] = 0
    thumb_with_texts[thumb_h + 20:total_h, :] = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 1

    count_text = f"Okundu: {count}"
    text_size_count = cv2.getTextSize(count_text, font, font_scale, thickness)[0]
    text_x_count = (thumb_w - text_size_count[0]) // 2
    text_y_count = 15
    cv2.putText(thumb_with_texts, count_text, (text_x_count, text_y_count), font, font_scale, (255,), thickness, cv2.LINE_AA)

    text_size_plate = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x_plate = (thumb_w - text_size_plate[0]) // 2
    text_y_plate = total_h - 5
    cv2.putText(thumb_with_texts, text, (text_x_plate, text_y_plate), font, font_scale, (255,), thickness, cv2.LINE_AA)

    return thumb_with_texts

def update_result_window():
    if not detected_plates:
        return

    plates = list(detected_plates.items())
    rows = math.ceil(len(plates) / thumbs_per_row)
    total_width = thumbs_per_row * (thumb_w + spacing) - spacing
    total_height = rows * (thumb_h + 40 + spacing) - spacing + 20
    result_img = np.ones((total_height, total_width), dtype=np.uint8) * 255

    for idx, (text, data) in enumerate(plates):
        row = idx // thumbs_per_row
        col = idx % thumbs_per_row
        x = col * (thumb_w + spacing)
        y = row * (thumb_h + 40 + spacing)
        thumb_with_texts = create_plate_thumbnail_with_texts(data["image"], text, data["count"])
        result_img[y:y + thumb_h + 40, x:x + thumb_w] = thumb_with_texts

    cv2.imshow("Tespit Edilen Plaka Görselleri", result_img)

def process_plate_image(plate_img):
    result = reader.readtext(plate_img)
    for (bbox, text, prob) in result:
        text_clean = re.sub(r'\W+', '', text.upper())
        if is_valid_plate(text_clean):
            if text_clean in detected_plates:
                detected_plates[text_clean]["count"] += 1
            else:
                detected_plates[text_clean] = {"count": 1, "image": plate_img}

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{text_clean}_{timestamp}.png"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, plate_img)

            print(f"✅ Plaka: {text_clean} (Toplam: {detected_plates[text_clean]['count']})")
            update_result_window()
            return
    print("❌ Geçersiz ya da okunamayan plaka.")

def read_plate_images_from_folder(folder_path):
    print(f"\n📂 '{folder_path}' klasöründeki plakalar taranıyor...")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder_path, filename)
            image = cv2.imread(path)
            if image is not None:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                process_plate_image(gray)

# Önce klasördeki plakaları tara
read_plate_images_from_folder(image_folder)

print("📡 Kamera taraması başlatıldı. Çıkmak için 'q' tuşuna bas.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=1000)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 250)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]

    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if 4 <= len(approx) <= 6:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 2 < aspect_ratio < 6 and w > 100:
                plate_img = gray[y:y + h, x:x + w]
                process_plate_image(plate_img)

    cv2.imshow("Kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
