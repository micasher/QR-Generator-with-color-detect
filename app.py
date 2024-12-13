import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from PIL import Image, ImageDraw
import colorgram

# נתיב הלוגו
logo_path = r"example"  # עדכן לנתיב הקובץ שהעלית
output_path = r"generated_qr.png"

# ה-URL או הנתונים שייכנסו ל-QR Code
data = "https://google.com"

# חילוץ צבעים דומיננטיים מהלוגו
colors = colorgram.extract(logo_path, 5)

# סינון צבעים לבנים או קרובים ללבן
filtered_colors = [
    color.rgb for color in colors if not (color.rgb.r > 240 and color.rgb.g > 240 and color.rgb.b > 240)
]

# בחירת הצבעים הדומיננטיים
dominant_color = filtered_colors[0] if filtered_colors else (0, 0, 0)  # צבע ראשי
secondary_color = filtered_colors[1] if len(filtered_colors) > 1 else (255, 255, 255)  # צבע משני

# הדפסת הצבעים שנמצאו
for i, color in enumerate(colors):
    print(f"Color {i+1}: {color.rgb}")

print(f"Dominant Color (Filtered): {dominant_color}")
print(f"Secondary Color (Filtered): {secondary_color}")

# יצירת QR Code עם צביעה מותאמת
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(data)
qr.make(fit=True)

# יצירת תמונת QR Code עם גרדיאנט צבעים
qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=VerticalGradiantColorMask(
        top_color=dominant_color,   # הצבע הראשי
        bottom_color=secondary_color,  # הצבע המשני
    ),
).convert("RGBA")

# פתיחת הלוגו
logo = Image.open(logo_path).convert("RGBA")

# הוספת מסגרת ללוגו
logo_width, logo_height = logo.size
border_size = int(logo_width * 0.1)  # גודל המסגרת כ-10% מגודל הלוגו
logo_with_border = Image.new(
    "RGBA",
    (logo_width + 2 * border_size, logo_height + 2 * border_size),
    (255, 255, 255, 255),  # מסגרת לבנה
)
logo_with_border.paste(logo, (border_size, border_size), logo)

# שינוי גודל הלוגו בהתאם לגודל ה-QR Code
qr_width, qr_height = qr_img.size
scale_factor = 0.25  # הלוגו יהיה 25% מגודל ה-QR Code
new_logo_size = (int(qr_width * scale_factor), int(qr_height * scale_factor))
logo_resized = logo_with_border.resize(new_logo_size, Image.LANCZOS)

# מיקום הלוגו במרכז ה-QR Code
logo_x = (qr_width - logo_resized.size[0]) // 2
logo_y = (qr_height - logo_resized.size[1]) // 2

# שילוב הלוגו עם ה-QR Code
qr_img.paste(logo_resized, (logo_x, logo_y), logo_resized)

# שמירת התוצאה
qr_img.save(output_path)

print(f"QR Code with custom logo and colors saved to: {output_path}")
