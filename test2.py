from pytesseract import pytesseract
import Image


img = "material/id.png"
result = pytesseract.image_to_string(Image.open(img), lang='chi_sim')
print result