#!/usr/bin/env python
# coding=utf-8

# 引入依赖
from PIL import Image
import pytesseract
import cv2
import os
import heapq


def main():
    tesseractID("material/111.jpg")

def tesseractID(path):
    img = cv2.imread(path, 0)
    heigth = 1300
    width = 1700
    img = img[heigth:heigth + 920, width:width + 1440]
    img = cv2.resize(img, (900, 600))

    cv2.imshow("Picture", img)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    retval, binarized = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY);

    # 闭运算 先膨胀后腐蚀称为闭
    closed = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow("Close Picture",closed)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # 开运算 先腐蚀后膨胀
    opened = cv2.morphologyEx(binarized, cv2.MORPH_OPEN, kernel)

    # cv2.imshow("Open Picture", opened)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 膨胀图像 (白色)
    dilated = cv2.dilate(binarized, kernel)

    # cv2.imshow("Dilated Picture", dilated)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 腐蚀图像，使身份证号连成一整块，方便裁剪
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 20))
    eroded = cv2.erode(binarized, kernel)

    # cv2.imshow("Eroded picture", eroded)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 黑白反色，将字转为白色，为下一步框选做准备
    inverted = cv2.bitwise_not(eroded)

    # cv2.imshow("Inverted Picture", inverted)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 框选出前景中，识别出的文本块
    _, contours, hierarchy = cv2.findContours(inverted, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    """
    第一个参数是寻找轮廓的图像；
    第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
        cv2.RETR_EXTERNAL表示只检测外轮廓
        cv2.RETR_LIST检测的轮廓不建立等级关系
        cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。
            如果内孔内还有一个连通物体，这个物体的边界也在顶层。
        cv2.RETR_TREE建立一个等级树结构的轮廓。
    第三个参数method为轮廓的近似办法
    cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），
        abs（y2-y1））==1
    cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，
        例如一个矩形轮廓只需4个点来保存轮廓信息
    cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
    """

    # 在所有文本框中挑出最长的三个框，身份证号应该在其中
    IDcnts = findIDcnt(contours)

    # 画框
    # cv2.drawContours(img, IDcnts, -1, (255,0,0), 3)
    #
    # cv2.imshow("drawContours", img)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    IDimgs = []
    for index, IDcnt in enumerate(IDcnts):
        x, y, w, h = cv2.boundingRect(IDcnt)
        # 裁剪图片，并储存在IDimgs中
        IDimg = img[y: y + h, x: x + w]
        IDimgs.insert(index, IDimg)

        cv2.imshow("Cut Picture", IDimg)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 将这三张可能的框出的图片传给tesseract识别，得到身份证
    IDstring = tesseractImg(IDimgs)
    print(path + ": " + IDstring)
    return IDstring

# 在所有的框中挑出三个最宽的矩形框
def findIDcnt(countours):
    # 保存所有框的宽度
    widths = []
    for index, cnt in enumerate(countours):
        x, y, width, height = cv2.boundingRect(cnt)
        widths.insert(index, width)

    # 挑出宽度前三的三个宽度
    IDList = heapq.nlargest(10, widths)
    # 根据这三个宽度，找出对应的那三个矩形框
    IDcnts = []
    for index, item in enumerate(IDList):
        index2 = widths.index(item)
        IDcnts.insert(index, countours[index2])
        # print "countours["+str(index)+"]\r\n",countours[index2],"\r\n"
    return IDcnts


# tesseract识别号码
def tesseractImg(imgs):
    for img in imgs:
        result = pytesseract.image_to_string(Image.fromarray(img), lang='eng',
                                             config="-c tessedit_char_whitelist=0123456789X")
        if (len(result) == 18):
            return result

    return "ID not found!"


if __name__ == "__main__":
    main()