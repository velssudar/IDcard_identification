#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2

def frontPicture(path):

    img = cv2.imread(path, 0)
    img = cv2.resize(img, (2100, 1480))
    heigth = 480
    width = 630
    img = img[heigth:heigth + 540, width:width + 856]

    blur = cv2.GaussianBlur(img, (1, 1), 0)
    retval, binarized = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print "front retval:",retval

    tempPath="temp/temp.jpg"
    cv2.imwrite(tempPath,binarized)
    from run import frontPictureIdentify
    frontPictureIdentify(tempPath)


def backPicture(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (2100, 1480))
    heigth = 480
    width = 630
    img = img[heigth:heigth + 540, width:width + 856]

    blur = cv2.GaussianBlur(img, (3, 3), 0)
    retval, binarized = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # print "front retval:",retval

    tempPath="temp/temp2.jpg"
    cv2.imwrite(tempPath,binarized)
    from run import backPictureIdentify
    backPictureIdentify(tempPath)
