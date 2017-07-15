#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 10:25:35 2017

@author: sohdm
"""

"""
سلام
خسته نباشید

این مسئله یک مسئله csp هست که با روش backtracking حلش می کنیم
توی هر مرحله یکی از رقم های عدد ۱۳ رقمی مشخص میشه
برای اینکه تعیین کنیم کدوم رقم رو باید توی این مرحله پیدا کنیم از MRV استفاده می کنیم
اون رقمی رو انتخاب می کنیم که کمترین امکان برای انتخاب رو داشته باشه مثلا رقم ۱۲ ام می تونه ۲ و۳ باشه رقم ۱۳ ام ۴ و۶ و۰ 
ما رقم ۱۲ رو اول انتخاب می کنیم

بعد از انتخاب رقم باید انتخاب کنیم که جه مقداری بهش بدیم . این مقدار رو با استفاده از تکنیک مقدار محدود کننده یا LCV پیدا می کنیم
به این شکل که یکی از مقدار های ممکن رو انتخاب می کنیم میدیم به رقم ، بعد میایم می بینم از بین
رقم های دیگه ، چه رقم هایی از دامنشون حذف میشه
مثلا اگه رقم ۱۲ رو بدیم ۴
رقم ۱۳ رو دیگه نمیشه ۰ و ۶ داد (محدودیت ۱ ) فقط ۴ می مونه
به همین صورت تمام اعداد رو حساب می کنیم

"""
import copy

# برای نمایش عدد
def formatSolution(solution):
    number = ''
    for i in solution :
        number += str(solution[i]['domain'][0])
    return number

# متغیر هایی که مقدار ندادیم بهشون
def unasigned_variables_list(asignment):
    return [x for x in asignment if asignment[x]['asigned']==False]

# متغیر هایی که مقدار دادیم بهشون
def asigned_variables_list(asignment):
    return [x for x in asignment if asignment[x]['asigned']==True]

# ببینیم آیا به جواب رسیدیم یا نه
def check_complete_asignment(asignment):
    return len(asigned_variables_list(asignment))==len(asignment)


# اینجا با MRV میایم متغیر مناسب رو شناسایی می کنیم
def select_unasigned_variable(asignment,csp) :
    unasigned_var = unasigned_variables_list(asignment)
    
    """
    selecting varibale with MRV
    """
    selected_var = \
    [x for x in unasigned_var if \
     len(asignment[x]['domain'])==min([len(asignment[y]['domain']) for y in unasigned_var])][0]
    
    return selected_var


# محدودیت اول
def check_constraint_1(asignment,var,value,csp):

    asigned_variable = asigned_variables_list(asignment)
    
    check=list()
    
    if var > 1 :
        if var - 1 in asigned_variable :
            if abs(asignment[var-1]['domain'][0]-value)<2 :
                check.append(True)
            else :
                check.append(False)
        else : check.append(True)
    else : check.append(True)
    
    if var < 13 :
        if var+1 in asigned_variable :
            if abs(asignment[var+1]['domain'][0]-value)<2 :
                check.append(True)
            else :
                check.append(False)
        else : check.append(True)
    else : check.append(True)
    
    if check == [True,True] : return True
    else : return False
    

#   محدودیت دوم
def check_constraint_2(asignment,var,value,csp):

    asigned_variable = asigned_variables_list(asignment)
    
    if len(asigned_variable) == 12 :
        
        used_digits = set([int(asignment[x]['domain'][0]) for x in asigned_variable])
        used_digits.add(int(value))
        
        digits = set(list(range(10)))
        
        if len(digits.difference(used_digits)) > 0 and \
        len(digits.difference(used_digits)) < 7 :
            return True
        
        else: return False
    
    else : return True


# محدودیت سوم
def check_constraint_3(asignment,var,value,csp):

    if var == 1:
        if value == 0 : return False
        else : return True
    else : return True
        

# محدودیت چهارم
def check_constraint_4(asignment,var,value,csp):

    asigned_variable = asigned_variables_list(asignment)

    if (len(asigned_variable)) > 0 :
        list_number_sequences = [list(range(y, y + 5)) \
                                 for y in \
                                 [x for x in asignment if \
                                  x - var < 5] if \
                                 (y < var + 1 and y + 5 > var)]

        # //list_number_sequences_edited = [x.remove(var) for x in list_number_sequences]

        for sequence in list_number_sequences :

            sequence.remove(var)
            if len([x for x in sequence if \
                    x in asigned_variable]) == 4 :

                     if sum([asignment[x]['domain'][0] for x in sequence])+value > 40 :
                         return False

    return True

                

#  این تابع چک می کنه آیا همه محدودیت ها ارضا میشه یا نه
def check_csp_constraints(asignment,var,value,csp):

    if asignment[var]['asigned'] : return True
    if check_constraint_1(asignment,var,value,csp) and\
        check_constraint_2(asignment,var,value,csp) and\
        check_constraint_3(asignment,var,value,csp) and\
        check_constraint_4(asignment,var,value,csp) :
            return True

    return False
        

# این تایع مقادیری که با محدودیت ها نمی خونن میاد حذف می کنه از دامنه متغیر
def remove_inconsistent_values (asignment,var,csp):

    remove_value_list = list()
    for value in asignment[var]['domain']:
        if not check_csp_constraints(asignment,var,value,csp) :
            remove_value_list.append(value)
    
    for value in remove_value_list :
        asignment[var]['domain'].remove(value)



# اینجا با همون LCV میام مقدار های مناسب رو به ترتیب می چینیم و امتحان می کنیم
def select_value(asignment,var,csp):
    """
    selecting value with LCV
    """
    dict_number_domain_values = dict()
     
    for value in asignment[var]['domain']:
        asignment_emulator = copy.deepcopy(asignment)
        asignment_emulator[var]['domain'] = [value]
        asignment_emulator[var]['asigned'] = True

        for var in asignment_emulator:
            remove_inconsistent_values(asignment_emulator, var, csp)

        number_domain_values = \
         sum([len(asignment_emulator[x]['domain']) for x in asignment_emulator])
         
        dict_number_domain_values[value] = number_domain_values

        del asignment_emulator
    
    list_selected_value = list()

    while len(dict_number_domain_values) > 0 :
        selected_value = \
        [x for x in dict_number_domain_values if \
         dict_number_domain_values[x] == \
         min([dict_number_domain_values[y] for \
              y in dict_number_domain_values])][0]  
    
        list_selected_value.append(selected_value)
        dict_number_domain_values.pop(selected_value)
            
    return list_selected_value


# بدنه اصلی کار و تابع اصلی
def recursive_backtrack(asignment,solutionList,maximum_numbers,csp):
    if check_complete_asignment(asignment) :
        solutionList.append(formatSolution(asignment))
        print(formatSolution(asignment))
        if len(solutionList) > maximum_numbers : return asignment
        return False

    var = select_unasigned_variable(asignment,csp)
    
    # print(var)

    if len(asignment[var]['domain']) == 0 : return False

    remove_inconsistent_values(asignment,var,csp)

    list_value_sorted = select_value(asignment,var,csp)

    for value in list_value_sorted :
        asignment_copy = copy.deepcopy(asignment)
        asignment[var]['domain'] = [value]
        asignment[var]['asigned'] = True
        result=recursive_backtrack(asignment,solutionList,maximum_numbers,csp)
        if result != False : return result
        asignment = copy.deepcopy(asignment_copy)
        del asignment_copy

    return False
    

# این شکل جواب هامونه و مقدار دهی اولیه است
asignment = {1:{'domain':list(),'asigned':False},
            2:{'domain':list(),'asigned':False},
            3:{'domain':list(),'asigned':False},
            4:{'domain':list(),'asigned':False},
            5:{'domain':list(),'asigned':False},
            6:{'domain':list(),'asigned':False},
            7:{'domain':list(),'asigned':False},
            8:{'domain':list(),'asigned':False},
            9:{'domain':list(),'asigned':False},
            10:{'domain':list(),'asigned':False},
            11:{'domain':list(),'asigned':False},
            12:{'domain':list(),'asigned':False},
            13:{'domain':list(),'asigned':False}}

for var in asignment :
    asignment[var]['domain'].extend(list(range(10)))

# اینجا جواب ها رو به ترتیب چاپ می کنیم . الان فقط ۲۰۰۰۰ تا جواب چاپ می کنه ولی خیلی خیلی زیاد تر از ایناست
# با تغییر اون ۲۰۰۰۰ میشه بیشترش کرد
solutionList = list()
solution = recursive_backtrack(asignment,solutionList,20000,'')
