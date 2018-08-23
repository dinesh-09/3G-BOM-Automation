# -*- coding: utf-8 -*-
"""
Created on Tue May  8 12:03:07 2018

@author: Demon King
"""
def conv_tim_hr(input_time,str_op=0):
    if str_op==0:
        return(input_time//3600,input_time%3600//60,input_time%60)
    else:
        return(str(input_time//3600)+' hrs ',str(input_time%3600//60)+' mins ',\
               str(input_time%60)+' secs ')
        
from class_product import *
from Read_File import Read_File  
import os.path
import time
import traceback
#import datetime
tot_st_time,tot_rt_time,tot_cmp_time = 0,0,0
list_exc=[]
start_time=time.time()
with open(r'P:\Test\out.txt', 'w') as f:
    file_paths = Read_File(r'P:\Test\paths-file.txt')
    i,s,r,c=-1,0,0,0
    file_paths = [path for path in file_paths if not path.startswith('#')]
    for path in file_paths:
        i+=1
    #attrib_file = r'P:\Sample_Product_Excel\Attributes_input.csv'
        try:
            attrib_file = path
            stock_items = component()
            stock_items.read_attribs(attrib_file)
            stock_items.create_comb()
            print('\n\n*********Processing files at path ',path,'*********', file=f)
            st_time = time.time()
            tot_st_time += st_time-start_time
            # **************************************************************** #
            #stock_file = r'P:\Sample_Product_Excel\1ST_StockItems-RC1-Test.csv'
            stock_file = path+r'\Stock_Items.csv'
            if os.path.isfile(stock_file) == True:
                s+=1
                print('\nStock Items file found, processing.....', file=f)
                stock_items.read_out_file(stock_file)
                stock_items.populate_items(print_type=1)
                stock_items.write_file(stock_file.replace(".csv","_out.csv"))
                
            else:
                if i == len(file_paths)-1:
                    print('\nStock Items file not found!', file=f)
                    continue
                else:
                    print('Stock Items file not found ! Checking the next folder in the list.....', file=f)
                    continue
            
            # **************************************************************** #
            #routing_file = r'P:\Sample_Product_Excel\2ND_Routing-RC1-Test.csv'
            routing_file = path+r'\Routing.csv'
            routing_list = path+r'\ROUTING_LIST.csv'
            if os.path.isfile(routing_file) == True:
                r+=1
                print('\nRouting file found, processing.....', file=f)
                stock_items.read_out_file(routing_file)
                stock_items.read_routing_infile(routing_list)
                stock_items.create_routing_content()
                stock_items.write_file(routing_file.replace(".csv","_out.csv"))
                
            else:
                print('\nRouting file not found ! Checking the next folder in the list.....', file=f)
                continue
            rt_time = time.time()
            tot_rt_time += rt_time-st_time
            # **************************************************************** #
            #components_file = r'P:\Test\Components-Test.csv'
            #comp_list = r'P:\Test\COMPONENTS.csv'
            components_file = path+r'\Components.csv'
            comp_list = path+r'\COMPONENTS_LIST.csv'
            if os.path.isfile(components_file) == True:
                c+=1
                print('\nComponents file found, processing.....', file=f)
                stock_items.read_out_file(components_file)
                aa=time.time()
                stock_items.read_comp_infile(comp_list)
#                ab=time.time()
#                print("Comp infile time: ",conv_tim_hr(ab-aa))
                stock_items.create_components_content()
#                ac=time.time()
#                print("Comp select time: ",conv_tim_hr(ac-ab))
                stock_items.write_file(components_file.replace(".csv","_out.csv"))
            else:
                print('\nComponents file not found ! Checking the next folder in the list.....', file=f)
                continue
            cmp_time = time.time()
            tot_cmp_time += cmp_time-rt_time
        except Exception as e:
            print(e)
            list_exc.append(i)
            print('\nError in entry number',c,'in the list:', e, file=f)
            traceback.print_exc()
#            c+=1
#            r+=1
#            s+=1
            #i+=1
            continue
        

    elapsed_time=time.time()-start_time
    hrs,mins,secs =conv_tim_hr(elapsed_time)
    tot_st_time = conv_tim_hr(tot_st_time,str_op=1)
    tot_rt_time = conv_tim_hr(tot_rt_time,str_op=1)
    tot_cmp_time = conv_tim_hr(tot_cmp_time,str_op=1)
    
    print('\nFolder list complete!')
    #print("\nTotal time for creating all Stock_Items :", tot_st_time, file=f)
    #print("\nTotal time for creating all Routings :", tot_rt_time, file=f)
    #print("\nTotal time for creating all Components :", tot_cmp_time, file=f)
    #print('\nTotal run time for ',c,'destination folders, in hrs:mins:secs format, is:',str(datetime.timedelta(seconds=(time.time()-start_time))), file=f)
    print('\nTotal run time for ',s, 'destination folders is:',hrs,' hrs',mins,' mins',secs,' secs', file=f)
    if len(list_exc)!=0:
        print('\n Exceptions occured in the following entries in the list : ',end="", file=f)
        print(*list_exc, sep = ", ", file=f)
# add %"r%" before string variables

#if not (a==1 and b==2 and c==3):
#    print('It Works !!')   
#    
#
#if not (a==1 and b==2 and c==3):
#    print('It Works !!')
#else:
#    print('The non does too')