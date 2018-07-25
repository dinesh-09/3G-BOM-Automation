# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Demon King
"""
class component:
    import sys
    
    # ********************* Initialise ******************** #
    def __init__(self):
        self.comp_list = []
        self.iid=[]
        self.content=[]
        self.attribs=[]
        self.idesc=[]
        self.attrib_comb = []
        self.attr_value=[]
        self.r_attr_value=[]
        self.non_combs=[]
        self.var = ''
        self.attr_code=[]
        self.attrib_stype = []
    # ******************* Read and Write CSV_File ******************* #
    
    def transfer_csv(self,csv_file,content=None,rwflag=0,mute=0):
        import csv
        import sys
        if rwflag == 0: # Reading
            csv_out = []
            try:
                with open(csv_file) as cf:
                    csv_dump = csv.reader(cf,delimiter=',')
                    for row in csv_dump:
                        csv_out.append(row)
            except Exception as e:
                raise 
            if csv_out != [[]]:       
                csv_out = [d for d in csv_out if not d[0]=='#']   # Discards lines starting with # comment
            else:
                csv_out=[]
                
            return(csv_out)
        if rwflag == 1: # Writing
            with open(csv_file,'w',newline='') as cf:
                    writer = csv.writer(cf)
                    writer.writerows(content)
            if mute!=1:
                print('\tWriting Complete')
        else:
            print('\tIncorrect Read-Write Flag')
            sys.exit()
    
    # ******************* Read Component List File ******************* #
    
    def read_comp_infile(self,cf_name,file_flag=0):
        
        from sort_by_another import sort_by_another
        from copy import deepcopy
        from itertools import chain
        
        self.attr_value=[]
        if file_flag==0:
            comp_file = self.transfer_csv(cf_name)
        else: 
            comp_file=cf_name
        var_flag=comp_file[0][1]
        flag_list = comp_file[2]
        del comp_file[2],comp_file[1],comp_file[0]
        
        # Transposing the list
        comp_file = [list(i) for i in zip(*comp_file)]
        
        # Filtering ATTR_VALUEs
        attr_count=0
        for col in range(len(flag_list)-1,-1,-1):
            if flag_list[col]=='AV':
                self.attr_value.append(comp_file[col])
                attr_count += 1
                del comp_file[col], flag_list[col]

        if attr_count==0:
            raise Exception('Atrribute Error! No attributes have been provided')
        
        self.attr_value = self.attr_value[::-1]
        
        del_ind=[]
        if var_flag==1:
            del_ind.append(flag_list.index('D'))
            del_ind.append(flag_list.index('Q-D'))
        else:
            del_ind.append(flag_list.index('V'))
            del_ind.append(flag_list.index('Q-V'))
        
        for index in del_ind[::-1]:
            del comp_file[index], flag_list[index]
        
        comp_file = [list(i) for i in zip(*comp_file)]
                
        for row in range(len(self.attr_value)): # Splitting multiple attributes on a single line
            for entry in range(len(self.attr_value[row])-1,-1,-1):
                if ',' in self.attr_value[row][entry]:
                    all_attribs=[x.strip() for x in self.attr_value[row][entry].split(',')]
                    for attrib in all_attribs:
                        comp_file.insert(entry+1,comp_file[entry])
                        for ind in range(len(self.attr_value)):
                            if ind != row:
                                self.attr_value[ind].insert(entry+1,self.attr_value[ind][entry])
                            else:
                                self.attr_value[ind].insert(entry+1,attrib)
                    for ind in range(len(self.attr_value)):
                        del self.attr_value[ind][entry]
                    del comp_file[entry] 
        # Creating attribute codes
        #a=deepcopy(self.attr_value)
        #a = [list(i) for i in zip(*a)]
        self.attr_code = []
        attribs = deepcopy(self.attribs)
        if self.attribs[0]!=['']:
            self.attribs.insert(0,[''])
        # Need to create index list to later arrange the components before printing
        index_list = list(range(len(comp_file)))
        comp_file = [comp_file[i]+[index_list[i]] for i in range(len(comp_file))]
        # Creating the atrribute codes
        
        self.convert_attr_to_code(sub_conv_flag=1)
        # Sorting based on attribute code
        ind_list = sort_by_another(self.attr_code,ret_type=1)
        self.attr_value = [[self.attr_value[row][ind] for ind in ind_list]\
                       for row in range(len(self.attr_value))]
        self.attrib_stype = [[self.attrib_stype[row][ind] for ind in ind_list]\
                       for row in range(len(self.attrib_stype))]
        self.attr_code = [[self.attr_code[line][ind] for ind in ind_list]\
                          for line in range(len(self.attr_code))]
        comp_file = [comp_file[ind] for ind in ind_list]
        attrib_stype=[]
        attr_code=[]
        true_ind_list=[]
        if any(-1 in x for x in self.attr_code):
            for comp_no in range(len(comp_file)):
                ans = [self.attr_code[j][comp_no]>=0 for j in range(len(self.attr_code))]
                if all(ans):
                    true_ind_list.append(comp_no) 
            comp_file = [comp_file[ind] for ind in true_ind_list]
            self.attr_value = [[self.attr_value[row][ind] for ind in true_ind_list]\
                               for row in range(len(self.attr_value))]
            self.attrib_stype = [[self.attrib_stype[row][ind] for ind in true_ind_list]\
                               for row in range(len(self.attrib_stype))]
            self.attr_code = [[self.attr_code[line][ind] for ind in true_ind_list]\
                               for line in range(len(self.attr_code))]
        
        attr_code = self.attr_code.copy()
        attrib_stype = self.attrib_stype.copy()
        self.comp_attr_mtrx = [[[] for j in range(len(attribs[i]))] for i in range(len(attribs))] # -1 since 0 is automatically added in every list 
        temp = self.comp_attr_mtrx
        for j in range(len(comp_file)-1,-1,-1): # j is the index of each component in the list
            attr_type_list = [attr_list[j] for attr_list in attr_code]
            attr_stype_list = [attr_list[j] for attr_list in attrib_stype]
            s_ind = sort_by_another(attr_type_list,rev=True,ret_type=1)
            s_ind = [s_ind[i] for i in range(len(s_ind)) if attr_type_list[i] != 0]
            attr_stype_list = [attr_stype_list[m] for m in s_ind]
            attr_type_list = [attr_type_list[m] for m in s_ind]
            for i in range(1,len(attribs)): # number of attribute types
                if i in attr_type_list:
                    temp[i][attr_stype_list[attr_type_list.index(i)]].append(j)
                else:
                    for b in temp[i]:
                        b.append(j)
        self.comp_attr_mtrx = temp
        for i in self.comp_attr_mtrx[1:]:
            for j in i:
                j.extend(self.comp_attr_mtrx[0][0])
                j.sort()
        temp = self.comp_attr_mtrx
        del self.comp_attr_mtrx[0]
        self.comp_list = comp_file

    # ******************* Read Routing List File ******************* #
    
    def read_routing_infile(self,cf_name):
        from sort_by_another import sort_by_another
        
        comp_file = self.transfer_csv(cf_name)
        flag_list = comp_file[1]
        del comp_file[1],comp_file[0]
        # Transposing the list
        comp_file = [list(i) for i in zip(*comp_file)]
        
        # Filtering ATTR_VALUEs
        attr_count=0
        self.attr_value=[]
        for col in range(len(flag_list)-1,-1,-1):
            if flag_list[col]=='AV':
                self.attr_value.append(comp_file[col])
                attr_count += 1
                del comp_file[col], flag_list[col]

#        if attr_count==0:
#            raise Exception('Atrribute Error! No attributes have been provided')
        
        self.attr_value = self.attr_value[::-1]
        comp_file = [list(i) for i in zip(*comp_file)]
                
        for row in range(len(self.attr_value)): # Splitting multiple attributes on a single line
            for entry in range(len(self.attr_value[row])-1,-1,-1):
                if ',' in self.attr_value[row][entry]:
                    all_attribs=[x.strip() for x in self.attr_value[row][entry].split(',')]
                    for attrib in all_attribs:
                        comp_file.insert(entry+1,comp_file[entry])
                        for ind in range(len(self.attr_value)):
                            if ind != row:
                                self.attr_value[ind].insert(entry+1,self.attr_value[ind][entry])
                            else:
                                self.attr_value[ind].insert(entry+1,attrib)
                    for ind in range(len(self.attr_value)):
                        del self.attr_value[ind][entry]
                    del comp_file[entry] 
        # Creating attribute codes
        self.attr_code = []
        attribs = self.attribs
#        attr_value = deepcopy(self.attr_value)
        attribs.insert(0,[''])
        # Need to create index list to later arrange the components before printing
        index_list = list(range(len(comp_file)))
        comp_file = [comp_file[i]+[index_list[i]] for i in range(len(comp_file))]
        # Creating the atrribute codes
        
        self.convert_attr_to_code(sub_conv_flag=1)
 
        # Sorting based on attribute code
        ind_list = sort_by_another(self.attr_code,ret_type=1)
        self.attr_value = [[self.attr_value[row][ind] for ind in ind_list]\
                           for row in range(len(self.attr_value))]
        comp_file = [comp_file[ind] for ind in ind_list]
            
        self.attr_code = sort_by_another(self.attr_code,ret_type=0)
        stype = self.attrib_stype
        self.attrib_stype = [[self.attrib_stype[row][ind] for ind in ind_list]\
                           for row in range(len(self.attrib_stype))]
        attr_code = self.attr_code.copy()
        attrib_stype = self.attrib_stype.copy()
        self.comp_attr_mtrx = [[[] for j in range(len(attribs[i]))] for i in range(len(attribs))] # -1 since 0 is automatically added in every list 
        temp = self.comp_attr_mtrx
        for j in range(len(comp_file)-1,-1,-1): # j is the index of each component in the list
            attr_type_list = [attr_list[j] for attr_list in attr_code]
            attr_stype_list = [attr_list[j] for attr_list in attrib_stype]
            s_ind = sort_by_another(attr_type_list,rev=True,ret_type=1)
            s_ind = [s_ind[i] for i in range(len(s_ind)) if attr_type_list[i] != 0]
            attr_stype_list = [attr_stype_list[m] for m in s_ind]
            attr_type_list = [attr_type_list[m] for m in s_ind]
            for i in range(1,len(attribs)): # number of attribute types
                if i in attr_type_list:
                    temp[i][attr_stype_list[attr_type_list.index(i)]].append(j)
                else:
                    for b in temp[i]:
                        b.append(j)
        self.comp_attr_mtrx = temp
        for i in self.comp_attr_mtrx[1:]:
            for j in i:
                j.extend(self.comp_attr_mtrx[0][0])
                j.sort()
        #temp = self.comp_attr_mtrx
        del self.comp_attr_mtrx[0]
        self.comp_list = comp_file

    # ***************** Combinations code ***************** #
    
    # attr is a list of all the standard attributes available for a user to customize
    
    def create_comb(self):   # Creates all the possible combinations of the attributes excluding non-combs. 
        import itertools

        # ******** Creating all possible combinations ******** #
        comb = itertools.product(*self.attribs)
        for element in comb:
            self.attrib_comb.append(list(element))   # Ensuring its a list of lists and not a list of tuples

        # ******** Converting non_combs to codes ******** #
        if self.non_combs != []:
            non_combs_code = self.convert_attr_to_code(self.non_combs)
            non_combs_code = [sorted(m) for m in non_combs_code]
    
            for l in range(len(self.non_combs)):
                self.attrib_comb = \
                list(itertools.filterfalse(lambda x: x if [x[y] for y in non_combs_code[l]]== self.non_combs[l] else 0,self.attrib_comb))
        self.gen_ids()

        
    # ***************** Creation of item-id list of numbers from length of code ***************** #
    def gen_ids(self):
        n_list=len(self.attrib_comb)
        num = len(str(n_list))
        code='{0:0'+str(num)+'}'
        iid = [code.format(n) for n in range(1,n_list+1)]
        
        
        if self.var != '':
            iid = [self.var + '-' + i for i in iid]
#            for a in self.attrib_comb:
#                a.insert(0,self.var)
        self.iid=iid
        
    # ***************** Select the components ***************** #     
   
    def select_component2(self,attr,r_flag=0):
        from operator import itemgetter
        from copy import deepcopy
        from search_val import search_val
        attr = [i for i in attr if i!='']
        code,stype = self.convert_attr_to_code(attr,sub_conv_flag=1)
        code,stype = code[0],stype[0]
        set_list = []
        comp_attr_mtrx = self.comp_attr_mtrx
        ind_list = search_val(code,-1,mult_flag=1)
        if ind_list is not None:
            attr=[attr[ind] for ind in range(len(code)) if ind not in ind_list]
            stype=[stype[ind] for ind in range(len(code)) if ind not in ind_list]
            code=[code[ind] for ind in range(len(code)) if ind not in ind_list]
                #del comp_attr_mtrx[ind]
        # If only one attribute and all elements of comp_list selected, means non-factor
        for i in range(len(attr)):
            if i!=0:
                og_set = set_list
                check_set = set(comp_attr_mtrx[code[i]-1][stype[i]])
                set_list = og_set.intersection(check_set)
            else:
                set_list= set(comp_attr_mtrx[code[i]-1][stype[i]].copy()) #-1 since code is from 1
                #set_list = [m for m in ans]
#        set_list.sort()
        #final_comp_list = deepcopy(self.comp_list)                
        if len(set_list)!=len(self.comp_list):        
            final_comp_list = [self.comp_list[m] for m in set_list]
        else:
            final_comp_list = deepcopy(self.comp_list)                
        if r_flag==0:
            seq_col_no=1
        else:
            seq_col_no=2
        # Converting the Sequence to int for sorting    
        for ind in range(len(final_comp_list)):
            final_comp_list[ind][seq_col_no] = int(final_comp_list[ind][seq_col_no])
            
        if r_flag==0:
            final_comp_list = sorted(final_comp_list, key=itemgetter(seq_col_no,-1))   
        else:
            final_comp_list = sorted(final_comp_list, key=itemgetter(seq_col_no))   
        
        
        # Converting sequence back to a string
        for ind in range(len(final_comp_list)):  
            final_comp_list[ind] = final_comp_list[ind][:-1]
            final_comp_list[ind][seq_col_no] = str(final_comp_list[ind][seq_col_no])
            
        return(final_comp_list)
        
        # ***************** Select the components ***************** #     
   
    def select_component(self,attr,r_flag=0):
        from operator import itemgetter
        from find_ind_range import find_ind_range
        from sort_by_another import sort_by_another
        
        attr.insert(0,'')  # To Select all null components
        final_comp_list = self.comp_list.copy()
        final_attr_value = self.attr_value.copy()
        final_attr_code = self.attr_code.copy()
        for seq in range(len(self.attr_value)):
            ind_list = []
            #final_attr_value = [[]*len(self.attr_value)]
            attr_ind = 0
            if seq != 0:
                inds = sort_by_another(final_attr_code[seq],ret_type=1)
                final_attr_code = [[final_attr_code[row][ind] for ind in inds] \
                                   for row in range(len(final_attr_code))]
                final_comp_list = [final_comp_list[ind] for ind in inds]
                final_attr_value = [[final_attr_value[row][ind] for ind in inds] \
                                   for row in range(len(final_attr_value))]
            for attrib in attr:
                ind_st,ind_end=find_ind_range(final_attr_code[seq],attr_ind)
                for i in range(ind_st,ind_end+1):
                    if final_attr_value[seq][i] == attrib:
                        ind_list.append(i)
                attr_ind += 1
            ind_list = sorted(ind_list)
            
            for row in range(len(final_attr_value)):
                final_attr_value[row] = list(final_attr_value[row][i] for i in ind_list) 
                final_attr_code[row] = list(final_attr_code[row][i] for i in ind_list)
            final_comp_list = list(final_comp_list[i] for i in ind_list) 
        if r_flag==0:
            seq_col_no=1
        else:
            seq_col_no=2
            
        # Converting the Sequence to int for sorting
        for ind in range(len(final_comp_list)):
            final_comp_list[ind][seq_col_no] = int(final_comp_list[ind][seq_col_no])
        if r_flag==0:
            final_comp_list = sorted(final_comp_list, key=itemgetter(seq_col_no,-1))   
        else:
            final_comp_list = sorted(final_comp_list, key=itemgetter(seq_col_no))   
        final_comp_list = [i[:-1] for i in final_comp_list]
#        # Converting sequence back to a string
        for ind in range(len(final_comp_list)):    
            final_comp_list[ind][seq_col_no] = str(final_comp_list[ind][seq_col_no])
        return(final_comp_list)
        
   # ****************** Read the attributes ****************** #     
    
    def read_attribs(self,path='',Gflag=0):
        import os
        if path!='':
            path=path+'\\'
        if Gflag==0:
            name=r'Attributes_input.csv'
        else:
            name=r'Attributes_input_'+self.order_list[1]+'.csv'
        try:
            attribs= self.transfer_csv(path+name,0)
        except Exception as e:
            if Gflag!=0:
                self.read_attribs(path=path,Gflag=0)
            else:
                raise 
                
        if os.path.isfile(path+r'var.txt'):
            self.var = self.transfer_csv(path+r'var.txt',0)[0][0]
        del attribs[0] # deleting the header
        # Transposing the list for creating combinations
        attribs = list(zip(*attribs))
        # Filtering the empty elements # 
        attribs=list(filter(None,[list(filter(None,l)) for l in attribs]))
        self.attribs = list(filter(None,[list(filter(None,l)) for l in attribs]))
        
        # **************** Reading non_combs ******************* # 
        if path!='':
            self.non_combs= self.transfer_csv(path+r'Non-Combs.csv',0)        
    
    # ****************** Convert attributes to code ****************** #     

    def convert_attr_to_code(self,attr_value=None,sub_conv_flag=0):
        attr_code=[]
        attr_flag = [0 if attr_value == None else 1][0]
        if attr_value is None:
            attr_value = self.attr_value 
        if type(attr_value[0])==str:
                attr_value = [attr_value]
        if sub_conv_flag == 1:
            c = [[] for i in range(len(attr_value))]
        if type(attr_value)==str:
            attr_value=[[attr_value]]
        for j in range(len(attr_value)):
            boolean_list = [[any(x in [m] for x in n) for n in self.attribs] for m in attr_value[j]]
            True_flag = [int(True in m) for m in boolean_list]
            g = [boolean_list[m].index(True) \
                                   if True_flag[m] != 0 else -1 for m in range(len(boolean_list))]

            if sub_conv_flag == 1:
#                if type(g[0]==int):
#                    g = [g]
                for b in range(len(g)):
                    try:
                        alph = self.attribs[g[b]].index(attr_value[j][b])
                    except:
                        alph=0
                    c[j].append(alph)
            attr_code.append(g)
        if sub_conv_flag==1:
            self.attrib_stype=[]
        if attr_flag==0:
            self.attr_code=[]
        for i in range(len(attr_code)):
            self.attrib_stype.append([])
            self.attr_code.append([])
            for j in range(len(attr_code[i])):
                #if attr_code[i][j]!=-1:
                if sub_conv_flag == 1:
                    self.attrib_stype[i].append(c[i][j])
                if attr_flag==0:
                    self.attr_code[i].append(attr_code[i][j])
        else:
            if sub_conv_flag == 1:
                return(attr_code,c)
            else:
                return(attr_code)
            
#    def read_idesc(self,ifile):
#        attribs= self.transfer_csv(ifile,0)
#        del attribs[0] # deleting the header
#        # Transposing the list for creating combinations
#        attribs = list(zip(*attribs))
#        # Filtering the empty elements # 
#        self.idesc = list(filter(None,[list(filter(None,l)) for l in attribs]))
        
    def read_out_file(self,outfile):
        self.content=self.transfer_csv(outfile)
        #print("Length",len(self.content))
        self.header=self.content[0]
        del self.content[0]

        
        
# ************************************************************************************** #
    
#class product(component):
    
#    def __init__(self):
#        self.flag_colm=0 # Column number coressponding to cflag
#        self.cnum = []   # List of column number where c flags exist
#        self.iid = []    # List of item ids
#        print('Product initialized successfully')
        #self.idesc = []    # List of item descriptions
        
    
    # afile is the file containing the attributes # 
    # sfile is the file containing the skeleton of the stockitems file to be populated #
    
    def populate_items(self,s_items=None,id_no=-1,print_type=0,print_flag=1,header_edit_flag=0,\
                       attrib=None,mute=0):  # Creates the list of all the stockitems to be populated 
        from copy import deepcopy
        if attrib is None:
            attribs = deepcopy(self.attrib_comb)
                
        else:
            attribs=[attrib]
            
        if s_items is None:  # Stock_Items or Routing
            s_items = deepcopy(self.content)
            
            
        # ******** Creating the stock items ********* #
        prefix_flag = [a for a in s_items[0]]   # the flag list of choosing prefix and suffix
        del s_items[0]
                        
        prefix_list = s_items
        del s_items
        
        if prefix_flag.count('1') != prefix_flag.count('2'):
            raise Exception('Error in input file, mismatch in number of prefixes and suffixes')
            return()
                
        # Creating cores for ids and descriptions #    
        attribs = [['-'.join(a)]*len(prefix_list) for a in attribs]
        if id_no != -1:
            iid=[[self.iid[id_no]]*len(prefix_list)]
        else:
            iid=[[i]*len(prefix_list) for i in self.iid]
        iid = [item for m in iid for item in m]
        if not len(attribs) == 1:
            attribs = [item for m in attribs for item in m]
        

        # Need to take care of cases when there are more than one lines to be filled
        if not len(prefix_list)==1:
            prefix_list=[list(i) for i in zip(*prefix_list)]
            #max_len = max([len(i) for i in prefix_list])
            for p in prefix_list:
                if not all([e for e in p]):
                    ind = [i for i, x in enumerate(p) if x == '']
                    for i in ind:
                        p[i]=p[0]
            
            prefix_list=[list(i) for i in zip(*prefix_list)]
                    
        # creating the list for writing the csv file
        header_del_ind = []
        temp_list = []
        n_combs=len(attribs)
        if len(attribs) == 1:
            attribs = [item for m in attribs for item in m]
        if mute!=1:
            if print_type==1:
                print('\tCreating the content to be written to the Stock Items File')
            elif print_type==2 and print_flag==0:
                print('\tCreating the content to be written to the Routing File')
            elif print_type==3 and print_flag==0:
                print('\tCreating the content to be written to the Components File')

        for i in range (len(prefix_list[0])):
#            for r in range(len(prefix_list)):
            if prefix_flag[i] == '1':
                prefix = [m[i] for m in prefix_list]*n_combs
                #prefix = [item for m in prefix for item in m]
            if prefix_flag[i] == '2':
                suffix = [m[i] for m in prefix_list]*n_combs
                header_del_ind.append(i)
                if i == 3:
                    idesc = [m+n+o for m,n,o in zip(prefix,attribs,suffix)]
                    if "-IL" in idesc[0]:
                        idesc = [descs.replace("-IL","-L") for descs in idesc]
                    self.idesc = idesc
                    temp_list.append(idesc)
                if i == 1:
                    iids = [m+n+o for m,n,o in zip(prefix,iid,suffix)]
                    temp_list.append(iids)
            if prefix_flag[i] == '0' or prefix_flag[i] == '':
                temp = [m[i] for m in prefix_list]*n_combs
                #temp = [item for m in temp for item in m]
                temp_list.append(temp)
                
        header_del_ind = header_del_ind[::-1]
        
        if header_edit_flag==0:
            for header in header_del_ind:
                del self.header[header]

            if len(temp_list) != len(self.header):
                raise Exception('Debug the code!, error in number of column numbers in header and content of the file')
        # transposing the list so that each row is same as header file and appending it to the list
        temp_list = [list(i) for i in zip(*temp_list)]
        #header_list.extend(list(zip(*temp_list))) 
        #print ('Populating the Stock Items file')
        #self.transfer_csv(sfile,header_list,1)
        
        if attrib is None:
            self.content=temp_list
        else:            
            return(temp_list)
            
#        else: 
        
    def write_file(self,sfile,mute=0):
        header=[self.header]
        for content in self.content:
            f = lambda c: c if not '""' in c else c.replace('""','')
            content=[f(i) for i in content]
            header.append(content)
        if mute!=1:
            print ('\tPopulating the Output file')
        self.transfer_csv(sfile,header,1,mute=mute)
        return None
    
    def create_components_content(self,Gflag=0,mute=0):
        if mute!=1:
            print('\tChoosing components!')
        
        prefix_flags=self.content[0]
        del self.content[0]
        temp_list=[]
        from copy import deepcopy
        attrib_comb = deepcopy(self.attrib_comb)
#        if Gflag!=0:
#            attrib_comb=[i[:-1] for i in attrib_comb]
        i=len(attrib_comb)-1
        ind=0
        comp_ind=self.header.index("Component")
        seq_ind=self.header.index("Sequence")
        qty_ind=self.header.index("Usage Qty")
        lin_ind=self.header.index("Line No")

        for attrib_list in attrib_comb:
#            components_list = self.select_component(attrib_list)
#            if Gflag!=0:
#                
            components_list = self.select_component2(attrib_list)
            if len(components_list) == 0:
                m = 'Error in COMPONENTS_LIST, no component selected for the attribute combination: ' +\
                ', '.join([c for c in attrib_list if c !=''])
                raise Exception(m)                                
            
            
            transposed_content=[list(i) for i in zip(*self.content)]
            transposed_content[comp_ind]=[col[0] for col in components_list]
            transposed_content[seq_ind]=[col[1] for col in components_list]
            transposed_content[qty_ind]=[col[2] for col in components_list]
            
            
            if len(components_list[0])==4: # Fixed QTY is present
                fixed_ind=self.header.index("Fixed Qty")
                transposed_content[fixed_ind]=[col[3] for col in components_list]
            
            for ind in range(len(transposed_content)):
                if len(transposed_content[ind]) == 1:
                    transposed_content[ind] = [transposed_content[ind][0]]*len(components_list)
            
            transposed_content[lin_ind] =[str(num*10) for num in range(1,len(components_list)+1)]       
            transposed_content=[list(i) for i in zip(*transposed_content)]
            temp=[prefix_flags]
            temp.extend(transposed_content)
            if Gflag!=0:
                id_no=0
                header_ind=self.header_cntr-1
            else:
                id_no=len(attrib_comb)-1-i
                header_ind=i
            temp = self.populate_items(temp,id_no,3,i,header_ind,attrib_list,mute=mute)
            temp_list.extend(temp)
            i-=1
            if Gflag!=0:
                self.header_cntr -=1
            
        self.content = temp_list
        
    def create_routing_content(self,Gflag=0,mute=0):
        if mute!=1:
            print('\tChoosing components!')
        prefix_flags=self.content[0]
        del self.content[0]
        temp_list=[]
        from copy import deepcopy
        attrib_comb = deepcopy(self.attrib_comb)
        #if Gflag!=0:
            #attrib_comb=[i[:-1] for i in attrib_comb]
        i=len(attrib_comb)-1
        for attrib_list in attrib_comb:
            routing_list = self.select_component2(attrib_list,r_flag=1)
            # Transposing the content to ensure each column is handled individually
            transposed_content=[list(i) for i in zip(*self.content)]
            
            for ind in range(len(transposed_content)):
                if len(transposed_content[ind]) == 1:
                    transposed_content[ind] = [transposed_content[ind][0]]*len(routing_list)
            
            # Transposing the routing to add individual elements to the list                
            routing_list = [list(i) for i in zip(*routing_list)]
            
            for cont_ind in range(len(routing_list)):
                transposed_content[cont_ind+2] = routing_list[cont_ind] 
            
            
            transposed_content=[list(i) for i in zip(*transposed_content)]
            temp=[prefix_flags]
            temp.extend(transposed_content)
            temp = self.populate_items(temp,len(attrib_comb)-1-i,2,i,i,attrib_list,mute=mute)
            temp_list.extend(temp)
            i-=1   
        self.content = temp_list            
            
            
        
        
        
        
        
        
        
        
        
        
        