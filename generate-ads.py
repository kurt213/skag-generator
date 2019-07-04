
# coding: utf-8
# In[1]:

import pandas as pd
from datetime import datetime
import xlrd
import itertools


# In[2]:
class SheetInput:
    
    def __init__(self, ads_input):
        # excel_columns = [getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        # Read excel file
        wb = xlrd.open_workbook(ads_input)
        sheet = wb.sheet_by_index(0)
        self.sheet = sheet
        self.bottom_row = sheet.nrows
        self.header_row = self.header_row_method(self.bottom_row)
        
    def header_row_method(self, bottom_row):
        for i in range(bottom_row):
            if self.sheet.cell_value(i, 0) == 'keyword 1 - base':
                header_row = i        
        return header_row
        
    def read_column(self, column_number):
        col_list = []
        for r in range(self.header_row + 1, self.bottom_row):
            if len(self.sheet.cell_value(r, column_number)) > 0:
                col_list.append(self.sheet.cell_value(r, column_number))
        return col_list  

class KeywordList:
    
    def __init__(self, keyword_1, keyword_2, keyword_3, keyword_4):
        self.keyword_1 = keyword_1
        self.keyword_2 = keyword_2
        self.keyword_3 = keyword_3
        self.keyword_4 = keyword_4

    def generate_list(self):
        keyword_chain = [self.keyword_1, self.keyword_2, self.keyword_3, self.keyword_4]
        for idx, k in enumerate(keyword_chain):
            if len(keyword_chain[idx]) == 0:
                del keyword_chain[idx]
        keyword_list = list(itertools.product(*keyword_chain))
        return keyword_list
       
class KeywordManipulate:
    
    def __init__(self, kw_list):
        self.kw_list = kw_list
    
    # Converts a string to a different match formats
    def broad_match(self, words):
        broad_words = []
        combine_words = " ".join(words)
        split_words = combine_words.split(" ")
        for w in split_words:
            broad_words.append('+' + w)
        return " ".join(broad_words)

    def exact_match(self, words):
        return '[' + " ".join(words) + ']'
    
    def phrase_match(self, words):
        return '"' + " ".join(words) + '"'

    # substitutes ad 'kw#' placeholders to keywords
    def sub_kw(self, input_string):
        replace_tuple = []
        # Create replacement tuples
        for key, t in enumerate(self.kw_list):
            replace_tuple.append(('kw' + str(key + 1), t))
        # Replace keywords in string
        for r in replace_tuple:
            input_string = input_string.replace(*r)
        return input_string  

class SheetOutput:

    ad_group_headers = ('Campaign', 'Ad Group', 'Ad Group Status', 'Max CPC')
    keyword_headers = ('Campaign', 'Ad Group', 'Keyword', 'Status', 'Max CPC', 'Final URL')
    ad_headers = ('Campaign', 'Ad Group', 'Headline 1', 'Headline 2', 'Headline 3', 
                    'Description Line 1', 'Description Line 2', 'Description Line 3',
                    'Path 1', 'Path 2', 'Final URL')
    time_now = datetime.today().strftime('%Y-%m-%d')

    def __init__(self, ad_groups_sheet, keywords_sheet, ads_sheet):
        ad_groups_sheet = ad_groups_sheet
        keywords_sheet = keywords_sheet
        ads_sheet = ads_sheet
        self.df_ad_groups = pd.DataFrame(data=ad_groups_sheet, columns=self.ad_group_headers)
        self.df_keywords = pd.DataFrame(data=keywords_sheet, columns=self.keyword_headers)
        self.df_ads = pd.DataFrame(data=ads_sheet, columns=self.ad_headers)
    
    def convert_to_csv(self):
        self.df_ad_groups.to_csv('Output/ad_groups_' + self.time_now + '.csv', index=False)
        self.df_keywords.to_csv('Output/keywords_' + self.time_now + '.csv', index=False)
        self.df_ads.to_csv('Output/ads_' + self.time_now + '.csv', index=False)

    def convert_to_excel(self):
        writer = pd.ExcelWriter('Output/skag_output_' + self.time_now + '.xlsx', engine='xlsxwriter')
        self.df_ad_groups.to_excel(writer, sheet_name='Ad Groups', index=False)
        self.df_keywords.to_excel(writer, sheet_name='Keywords', index=False)
        self.df_ads.to_excel(writer, sheet_name='Ads', index=False)
        writer.save()



# In[3]:
# set excel file
ads_input = ("input_file.xlsx")
excel_input = SheetInput(ads_input)

# set param variables
campaign_name = excel_input.sheet.cell_value(0, 1)
exact_match = excel_input.sheet.cell_value(3, 1)
phrase_match = excel_input.sheet.cell_value(4, 1)
bmm = excel_input.sheet.cell_value(5, 1)

# Set lists
keyword_1 = excel_input.read_column(0)
keyword_2 = excel_input.read_column(1)
keyword_3 = excel_input.read_column(2)
keyword_4 = excel_input.read_column(3)
headline_1 = excel_input.read_column(5)
headline_2 = excel_input.read_column(6)
headline_3 = excel_input.read_column(7)
desc_line_1 = excel_input.read_column(8)
desc_line_2 = excel_input.read_column(9)
desc_line_3 = excel_input.read_column(10)
path_1 = excel_input.read_column(11)
path_2 = excel_input.read_column(12)
final_url = excel_input.read_column(14)

# Find longest list for ad generation
max_ad_list = max(len(i) for i in [headline_1, headline_2, headline_3, desc_line_1, desc_line_2, desc_line_3, path_1, path_2])



# In[4]:
# Create keyword tuples list
keyword_input = KeywordList(keyword_1, keyword_2, keyword_3, keyword_4)
kw_base_list = keyword_input.generate_list()
keyword_convert = KeywordManipulate(kw_base_list)

# Lists for output
adgroups_list = []
keywords_list = []
ads_list = []

for kw in kw_base_list:
    # Ad Groups
    ad_group_name = ' '.join(str(i) for i in kw)
    ad_group_status = 'ENABLED'
    max_cpc = 0.1
    adgroups_list.append((campaign_name, ad_group_name, ad_group_status, max_cpc))
    
    # Keywords
    match_keyword = ""
    keyword_status = 'enabled'
    
    word_sub = KeywordManipulate(kw)
    url_replace = word_sub.sub_kw(final_url[0])
    if (exact_match == 'Yes'):
        match_keyword = keyword_convert.exact_match(kw)
        keywords_list.append((campaign_name, ad_group_name, keyword_status, max_cpc, match_keyword, url_replace))
    if (phrase_match == 'Yes'):
        match_keyword = keyword_convert.phrase_match(kw)
        keywords_list.append((campaign_name, ad_group_name, keyword_status, max_cpc, match_keyword, url_replace))
    if (bmm == 'Yes'):
        match_keyword = keyword_convert.broad_match(kw)
        keywords_list.append((campaign_name, ad_group_name, keyword_status, max_cpc, match_keyword, url_replace))

    # Ads - loop through combinations and generate
    for a in range(0, max_ad_list):
        ads_list.append((campaign_name,
                        ad_group_name,
                        word_sub.sub_kw(headline_1[a]),
                        word_sub.sub_kw(headline_2[a]),
                        word_sub.sub_kw(headline_3[a]),
                        word_sub.sub_kw(desc_line_1[a]),
                        word_sub.sub_kw(desc_line_2[a]),
                        word_sub.sub_kw(desc_line_3[a]),
                        word_sub.sub_kw(path_1[a]),
                        word_sub.sub_kw(path_2[a]),
                        url_replace
                        ))
    


# In[8]:
sheet_output = SheetOutput(adgroups_list, keywords_list, ads_list)
try:
    sheet_output.convert_to_csv()
    print('skag csv created successfully')
except:
    print('error creating skag csv')

try:
    sheet_output.convert_to_excel()
    print('skag excel created successfully')
except:
    print('error creating skag excel')



#%%
