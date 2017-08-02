#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
import cv2
import pytesseract
from flask import json

from imageProcessing import backPicture,frontPicture

# 主程序
def main():

    path = "material/zhao_1.jpg"
    # 加载正面照片
    frontPicture(path)

    path2 = "material/zhao_2.jpg"
    # 加载反面图片
    backPicture(path2)

# 正面身份证信息识别
def frontPictureIdentify(path):
    # 加载预处理照片
    img = cv2.imread(path)
    # 设置尺寸信息 身份证尺寸 85.6 mm * 54.0 mm * 1.0 mm
    img = cv2.resize(img, (856, 540))

    # 姓名
    Name=[]
    name_heigth = 50
    name_width = 150
    name = img[name_heigth:name_heigth+80,name_width:name_width+370]
    Name.append(name)
    print "Name:",tesseractChinese(Name)

    # 性别
    Sex=[]
    sex_heigth = 120
    sex_width = 150
    sex = img[sex_heigth:sex_heigth + 70, sex_width:sex_width + 70]
    Sex.append(sex)
    print "Sex:",tesseractSex(Sex)

    # 民族
    Nationality=[]
    nationality_heigth = 120
    nationality_width = 330
    nationality = img[nationality_heigth:nationality_heigth + 70, nationality_width:nationality_width + 200]
    Nationality.append(nationality)
    print "Nationality:",tesseractNationality(Nationality)

    # 生日
    Birth_year=[]
    birth_year_heigth = 190
    birth_year_width = 150
    birth_year = img[birth_year_heigth:birth_year_heigth + 70, birth_year_width:birth_year_width + 100]
    Birth_year.append(birth_year)

    Birth_month=[]
    birth_month_heigth = 190
    birth_month_width = 290
    birth_month = img[birth_month_heigth:birth_month_heigth + 70, birth_month_width:birth_month_width + 40]
    Birth_month.append(birth_month)

    Birth_day=[]
    birth_day_heigth = 190
    birth_day_width = 365
    birth_day = img[birth_day_heigth:birth_day_heigth + 70, birth_day_width:birth_day_width + 50]
    Birth_day.append(birth_day)

    print "Birth:", tesseractDate(Birth_year)+"/" \
                    ""+tesseractDate(Birth_month)+"/" \
                    ""+tesseractDate(Birth_day)

    # 地址
    Address=[]
    address_heigth = 260
    address_width = 150
    address = img[address_heigth:address_heigth + 170, address_width:address_width + 370]
    Address.append(address)
    print "Address:",tesseractChinese(Address)

    # 身份证号
    ID_number =[]
    ID_heigth = 425
    ID_width = 280
    ID = img[ID_heigth:ID_heigth + 80, ID_width:ID_width + 550]
    ID_number.append(ID)
    print "ID_number:",tesseractID(ID_number)

    data =[{"Name:":tesseractChinese(Name),
                 "Sex:":tesseractSex(Sex),
                 "Nationality:":tesseractNationality(Nationality),
                 "Birth:":tesseractDate(Birth_year)+"/" \
                    ""+tesseractDate(Birth_month)+"/" \
                    ""+tesseractDate(Birth_day),
                 "Address:":tesseractChinese(Address),
                 "ID_number:":tesseractID(ID_number)}]
    frontData = json.dumps(data)
    print "json:",frontData
    # cv2.imshow("font", img)
    # cv2.waitKey(0)
    #
    # cv2.imshow("name", name)
    # cv2.waitKey(0)
    #
    # cv2.imshow("sex", sex)
    # cv2.waitKey(0)
    #
    # cv2.imshow("nationality", nationality)
    # cv2.waitKey(0)
    #
    # cv2.imshow("birth_year", birth_year)
    # cv2.waitKey(0)
    #
    # cv2.imshow("birth_month", birth_month)
    # cv2.waitKey(0)
    #
    # cv2.imshow("birth_day", birth_day)
    # cv2.waitKey(0)
    #
    # cv2.imshow("address", address)
    # cv2.waitKey(0)
    #
    # cv2.imshow("ID", ID)
    # cv2.waitKey(0)
    #
    # cv2.destroyAllWindows()

# 身份证背面信息读取
def backPictureIdentify(path):
    # 加载图片
    img = cv2.imread(path)
    # 设置尺寸
    img = cv2.resize(img, (856, 540))

    # 签发机关
    IssuingAuthority = []
    issuingAuthority_heigth = 360
    issuingAuthority_width = 340
    issuingAuthority = img[issuingAuthority_heigth:issuingAuthority_heigth + 80,
                       issuingAuthority_width:issuingAuthority_width + 500]
    IssuingAuthority.append(issuingAuthority)
    print "IssuingAuthority:", tesseractChinese(IssuingAuthority)

    # 有效期
    ValidPerriod = []
    validPerriod_heigth = 430
    validPerriod_width = 340
    validPerriod = img[validPerriod_heigth:validPerriod_heigth + 80,
                   validPerriod_width:validPerriod_width + 500]
    ValidPerriod.append(validPerriod)
    print "ValidPerriod:", tesseractValidperriod(ValidPerriod)

    data =[{"IssuingAuthority:":tesseractChinese(IssuingAuthority).encode("utf-8"),
                "ValidPerriodStar": tesseractValidperriod(ValidPerriod)[:8],
                "ValidPerriodEnd:":tesseractValidperriod(ValidPerriod)[9:]
                }]
    backData = json.dumps(data)
    print "json",backData

    # cv2.imshow("back", img)
    # cv2.waitKey(0)
    #
    # cv2.imshow("IssuingAuthority", issuingAuthority)
    # cv2.waitKey(0)
    #
    # cv2.imshow("ValidPerriod", validPerriod)
    # cv2.waitKey(0)
    #
    # cv2.destroyAllWindows()

# 中文识别
def tesseractChinese(imgs):
    """
       psm
       0 =仅定向和脚本检测（OSD）。
       1 =自动页面分割与OSD。
       2 =自动页面分割，但没有OSD或OCR。
       3 =全自动页面分割，但没有OSD。（默认）
       4 =假设可变大小的单列文本。
       5 =假设垂直排列文本的单个统一块。
       6 =假设单个统一的文本块。
       7 =将图像视为单个文本行。
       8 =将图像视为单个字。
       9 =将图像视为一个单一的单词。
       10 =将图像视为单个字符。
    """
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='chi_sim',
                                             config='-psm 3')
    return result.replace(" ","").replace("\n","")

# 性别中文识别
def tesseractSex(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='chi_sim',
                                             config="-c tessedit_char_whitelist=男女 -psm 8")
    return result.replace(" ","")

# 民族中文识别
def tesseractNationality(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='chi_sim',
                                             config="-psm 7")
    return result.replace(" ","")

# 日期英文识别
def tesseractDate(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='eng',
                                             config="-c tessedit_char_whitelist=0123456789 -psm 7")
    return result.replace(" ","")

# 身份英文识别
def tesseractID(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='eng',
                                             config="-c tessedit_char_whitelist=0123456789X -psm 7")
    return result.replace(" ","")

# 有效期中文识别
def tesseractValidperriod(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img),
                                             lang='chi_sim',
                                             config="-c tessedit_char_whitelist=0123456789-长期 -psm 7")
        # result.replace(" ", "")
        # result = result[:8]+"-"+result[9:]
    return result.replace(" ","")

# 主程序
if __name__ == "__main__":
    main();