#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 10:25:35 2017

@author: sohdm
"""

def check_complete_asignment(asignment):
    #return len([asignment[x] for x in asignment if asignment[x]!=''])==len(asignment)
    return len([x for x in asignment if len(asignment[x])==1])==len(asignment)

def select_unasigned_variable(asignment,csp) :
    unasigned_var = [x for x in asignment if len(asignment[x])!=1]  
    
    """
    selecting varibale with MRV
    """
    selected_var = \
    [x for x in unasigned_var if \
     len(asignment[x])==min([len(asignment[y]) for y in unasigned_var])][0]
    
    return selected_var
  

#def unasigend_variable(asignment):


def check_constraint_1(asignment,var,value,csp,asigned_variable):
    
    check=list()
    
    if int(var) > 1 :
        if str(int(var)+1) in asigned_variable :
            if abs(asignment[str(int(var)+1)][0]-value)<2 :
                check.append(True)
            else :
                check.append(False)
        else : check.append(True)
    else : check.append(True)
    
    if int(var) < 13 :
        if str(int(var)-1) in asigned_variable :
            if abs(asignment[str(int(var)-1)][0]-value)<2 :
                check.append(True)
            else :
                check.append(False)
        else : check.append(True)
    else : check.append(True)
    
    if check == [True,True] : return True
    else : return False
    
    
def check_constraint_2(asignment,var,value,csp,asigned_variable):
    
    if len(asigned_variable) == 12 :
        
        used_digits = set([int(asignment[x][0]) for x in asigned_variable])
        used_digits.add(int(value))
        
        digits = set(list(range(10)))
        
        if len(digits.difference(used_digits)) > 0 and \
        len(digits.difference(used_digits)) < 7 :
            return True
        
        else: return False
    
    else : return True


def check_constraint_3(asignment,var,value,csp,asigned_variable):
    #print(var,value)
    if var == '1': 
        if value == 0 : return False
        else : return True
    else : return True
        

def check_constraint_4(asignment,var,value,csp,asigned_variable):
    
    list_number_sequences = [list(range(int(y),int(y)+5)) \
                          for y in \
                          [x for x in asignment if \
                           abs(int(x)-int(var))<5] if \
                           (int(y) < int(var)+1 and int(y)+5 > int(var))]
    
    
    for sequence in list_number_sequences :
        if len([x for x in sequence if \
            str(x) in asigned_variable]) == 5 :
                 if sum([asignment[str(x)][0] for x in\
                                        sequence]) < 41 :
                              next
                 else : return False
        else: next
        
    return True
                
    
def check_csp_constraints(asignment,var,value,csp):
    
    asigned_variable = [x for x in asignment if len(asignment[x])==1] 
    
    if check_constraint_1(asignment,var,value,csp,asigned_variable) and\
        check_constraint_2(asignment,var,value,csp,asigned_variable) and\
        check_constraint_3(asignment,var,value,csp,asigned_variable) and\
        check_constraint_4(asignment,var,value,csp,asigned_variable) :
            return True
    return False
        
        
def remove_inconsistent_values (asignment,var,csp):

    remove_value_list = list()
    for value in asignment[var]:
        if not check_csp_constraints(asignment,var,value,csp) :
            remove_value_list.append(value)
    
    for value in remove_value_list :
        asignment[var].remove(value)



def select_value(asignment,var,csp):
    """
    selecting value with LCV
    """
    dict_number_domain_values = dict()
     
    for value in asignment[var]:
        asignment_emulator = dict(asignment)
        asignment_emulator[var] = [value]
        unasigned_variable = [x for x in asignment_emulator if\
                            len(asignment_emulator[x])!=1]
        # for elseVar in unasigned_variable:
        #     remove_inconsistent_values(asignment_emulator,elseVar,csp)
        #
        number_domain_values = \
         sum([len(asignment_emulator[x]) for x in asignment_emulator])
         
        dict_number_domain_values[value] = number_domain_values
    
    list_selected_value = list()
    
    #print(dict_number_domain_values)
    while len(dict_number_domain_values) > 0 :
        selected_value = \
        [x for x in dict_number_domain_values if \
         dict_number_domain_values[x] == \
         min([dict_number_domain_values[y] for \
              y in dict_number_domain_values])][0]  
    
        list_selected_value.append(selected_value)
        dict_number_domain_values.pop(selected_value)
            
    return list_selected_value
                
     
            


    

def recursive_backtrack(asignment,csp):
    if check_complete_asignment(asignment) : return asignment

    print('')
    var = select_unasigned_variable(asignment,csp)
    
    print(var)
    remove_inconsistent_values(asignment,var,csp)

    if len(asignment[var]) == 0 : return False
    #print(asignment[var])
    #if len(asignment[var]) < 1 : return False
    
    list_value_sorted = select_value(asignment,var,csp)
    #print(list_value_sorted)
    for value in list_value_sorted :
        asignment_copy = dict(asignment)
        asignment[var] = [value]
        result=recursive_backtrack(asignment,csp)
        if result != False : return result
        asignment = dict(asignment_copy)

    print(asignment)
    return False
    


asignment = {'1':{'asigned':False},list(),
             '2':list(),
             '3':list(),
             '4':list(),
             '5':list(),
             '6':list(),
             '7':list(),
             '8':list(),
             '9':list(),
             '10':list(),
             '11':list(),
             '12':list(),
             '13':list()}

for var in asignment :
    asignment[var].extend(list(range(10)))


solution = recursive_backtrack(asignment,'')
print(solution)