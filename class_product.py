# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
        self.non_combs=[]
        self.var = ''
    # ******************* Read and Write CSV_File ******************* #
    
    def transfer_csv(self,csv_file,content=None,rwflag=0):
        import csv
        import sys
        if rwflag == 0: # Reading
            csv_out = []
            with open(csv_file) as cf:
                csv_dump = csv.reader(cf,delimiter=',')
                for row in csv_dump:
                    csv_out.append(row)
            if csv_out != [[]]:       
                csv_out = [d for d in csv_out if not d[0]=='#']   # Discards lines starting with # comment
            else:
                csv_out=[]
                
            return(csv_out)
        if rwflag == 1: # Writing
            with open(csv_file,'w',newline='') as cf:
                    writer = csv.writer(cf)
                    writer.writerows(content)
            print('\tWriting Complete')
        else:
            print('\tIncorrect Read-Write Flag')
            sys.exit()
    
    # ******************* Read Component List File ******************* #
    
    def read_comp_infile(self,cf_name):
        from sort_by_another import sort_by_another
        
        comp_file = self.transfer_csv(cf_name)
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
        self.attr_code = []
        attribs = self.attribs
        attribs.insert(0,[''])
        # Need to create index list to later arrange the components before printing
        index_list = list(range(len(comp_file)))
        comp_file = [comp_file[i]+[index_list[i]] for i in range(len(comp_file))]
        # Creating the atrribute codes
        
        self.convert_attr_to_code()
        # Sorting based on attribute code
        ind_list = sort_by_another(self.attr_code,ret_type=1)
        self.attr_value = [[self.attr_value[row][ind] for ind in ind_list]\
                           for row in range(len(self.attr_value))]
        comp_file = [comp_file[ind] for ind in ind_list]
            
        self.attr_code = sort_by_another(self.attr_code,ret_type=0)
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
                list(itertools.filterfalse(lambda x: x if [x[y] for y in non_combs_code[l]]==self.non_combs[l] else 0,self.attrib_comb))
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
   
    def select_component(self,attr):
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
        # Converting the Sequence to int for sorting
        for ind in range(len(final_comp_list)):
            final_comp_list[ind][1] = int(final_comp_list[ind][1])
        final_comp_list = sorted(final_comp_list, key=itemgetter(1,-1))   
        final_comp_list = [i[:-1] for i in final_comp_list]
        # Converting sequence back to a string
        for ind in range(len(final_comp_list)):    
            final_comp_list[ind][1] = str(final_comp_list[ind][1])
        return(final_comp_list)
        
   # ****************** Read the attributes ****************** #     
    
    def read_attribs(self,path):
        import os
        attribs= self.transfer_csv(path+r'\Attributes_input.csv',0)
        if os.path.isfile(path+r'\var.txt'):
            self.var = self.transfer_csv(path+r'\var.txt',0)[0][0]
        del attribs[0] # deleting the header
        # Transposing the list for creating combinations
        attribs = list(zip(*attribs))
        # Filtering the empty elements # 
        attribs=list(filter(None,[list(filter(None,l)) for l in attribs]))
        self.attribs = list(filter(None,[list(filter(None,l)) for l in attribs]))
        
        # **************** Reading non_combs ******************* #
        
        self.non_combs= self.transfer_csv(path+r'\Non-Combs.csv',0)        
    
    # ****************** Convert attributes to code ****************** #     

    def convert_attr_to_code(self,attr_value=None):
        attr_code=[]
        attr_flag = [0 if attr_value == None else 1][0]
        if attr_value is None:
            attr_value = self.attr_value
        for j in attr_value:
            boolean_list = [[any(x in [m] for x in n) for n in self.attribs] for m in j]
            True_flag = [int(True in m) for m in boolean_list]
            attr_code.append([boolean_list[m].index(True) \
                                   if True_flag[m] != 0 else -1 for m in range(len(boolean_list))])
        if attr_flag==0:
            self.attr_code = attr_code
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
    
    def populate_items(self,s_items=None,id_no=-1,print_type=0,print_flag=1,header_edit_flag=0,attrib=None):  # Creates the list of all the stockitems to be populated 

        if attrib is None:
            attribs = self.attrib_comb
                
        else:
            attribs=[attrib]
            
            
        if s_items is None:  # Stock_Items or Routing
            s_items = self.content
            
            
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
        
        if print_type==1:
            print('\tCreating the content to be written to the Stock Items File')
        elif print_type==2:
            print('\tCreating the content to be written to the Routing File')
        elif print_type==3 and print_flag==0:
            print('\t\tCreating the content to be written to the Components File')

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
                    self.idesc = idesc
                    temp_list.append(idesc)
                if i == 1:
                    iids = [m+n+o for m,n,o in zip(prefix,iid,suffix)]
                    temp_list.append(iids)
            if prefix_flag[i] == '0':
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
        
    def write_file(self,sfile):
        header=[self.header]
        for content in self.content:
            header.append(content)
        print ('\tPopulating the Output file')
        self.transfer_csv(sfile,header,1)
        return None
    
    def create_components_content(self):
        print('\tChoosing components!')
        prefix_flags=self.content[0]
        del self.content[0]
        temp_list=[]
        i=len(self.attrib_comb)-1
        for attrib_list in self.attrib_comb:
            components_list = self.select_component(attrib_list)
            comp_ind=self.header.index("Component")
            seq_ind=self.header.index("Sequence")
            qty_ind=self.header.index("Usage Qty")
            lin_ind=self.header.index("Line No")
            
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
            temp = self.populate_items(temp,len(self.attrib_comb)-1-i,3,i,i,attrib_list)
            temp_list.extend(temp)
            i-=1
            
        self.content = temp_list
        
            
            
            
        
        
        
        
        
        
        
        
        
        
        