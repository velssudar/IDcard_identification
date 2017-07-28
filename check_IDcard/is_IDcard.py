#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime
import pickle


def is_IDcard_number(IDcard_number):

    #读取地区映射
    area_file = open('area_data.pkl','rb')
    area_dict = pickle.load(area_file)
    area_id = IDcard_number[0:6]
    # print area_id

    #性别字典
    sex_dict = {
        0:"woman",1:"man"
    }

    #判断长度，必须为十八位
    if len(IDcard_number) != 18:
        return False, "Length error"

    #正则匹配 前十七只能时数字 最后一位只能是x，X，或者数字
    if not re.match(r"^\d{17}(\d|X|x)$", IDcard_number):
        return False, "Format error"

    #判断前6位是否在地区表中
    try :
        area_name = area_dict[area_id]
        print area_name
    except :
        return False, "Area error"

    #判断出生日期是否合法
    try:
        datetime.date(int(IDcard_number[6:10]), int(IDcard_number[10:12]), int(IDcard_number[12:14]))
        # 生日
        birth = IDcard_number[6:14]
        # print birth
    except ValueError as ve:
        return False, "Datetime error: {0}".format(ve)

    #判断性别
    if (int(IDcard_number[16])%2) not in sex_dict:
        return False,"Sex error"

    #匹配最后一位校验码是否正确
        # 所在位数值*对应值再相加，运算后的值%11 取余数对应的字母或数字
    check_sum = int(IDcard_number[0]) * 7 + \
                int(IDcard_number[1]) * 9 + \
                int(IDcard_number[2]) * 10 + \
                int(IDcard_number[3]) * 5 + \
                int(IDcard_number[4]) * 8 + \
                int(IDcard_number[5]) * 4 + \
                int(IDcard_number[6]) * 2 + \
                int(IDcard_number[7]) * 1 + \
                int(IDcard_number[8]) * 6 + \
                int(IDcard_number[9]) * 3 + \
                int(IDcard_number[10]) * 7 + \
                int(IDcard_number[11]) * 9 + \
                int(IDcard_number[12]) * 10 + \
                int(IDcard_number[13]) * 5 + \
                int(IDcard_number[14]) * 8 + \
                int(IDcard_number[15]) * 4 + \
                int(IDcard_number[16]) * 2;
    check_remainder = check_sum % 11
    # print check_remainder
    check_code_dict = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
    if check_code_dict[check_remainder] != IDcard_number.upper()[17]:
        return False, "Check code error"

    return True, "area:",area_name.decode("utf-8"),"birth",birth,"sex:",sex_dict[(int(IDcard_number[16])%2)]

#测试
if __name__ == "__main__":
    idcard_number = str(input('请输入身份证号码：'))
    print is_IDcard_number(idcard_number)
    # print is_IDcard_number("330702196302260412X")
    # print is_IDcard_number("3307021963X226041x")
    # print is_IDcard_number("330702196呵呵41X")
    # print is_IDcard_number("39070219630226041X")
    # print is_IDcard_number("33070219630229041X")
    # print is_IDcard_number("330702196302260410")
    # print is_IDcard_number("33070219630226041x")
    # print is_IDcard_number("33070219630226041X")
