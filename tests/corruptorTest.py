# corruptorTest.py - Test module that provides testing functions for the
#                    module corruptor.py of the data generation system.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for corruptor.py.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then system modules)

import os
import random
import sys
import time
import unittest
import difflib
sys.path.append('..')

import corruptor
import basefunctions

random.seed(42)  # Set seed for random generator

# =============================================================================

random.seed(1)

# Define the number of tests to be done for the functionality tests
#
num_tests = 10000

# Define dummy correct test functions that take a string as input and return
# an integer in the range of the length of the string
#
def test_function0(s):
  return len(s)-1
def test_function1(s):
  return len(s)+3-4
def test_function2(s):
  return 0

# Define several functions that should trigger an exception
#
def test_exce_function0(s):
  return 999.99
def test_exce_function1(s):
  return len(s)*2
def test_exce_function2(s):
  return 'test'

def char_set_funct1(s):
  return s
def char_set_funct2(s):
  return s[0:len(s)/2]

def exce_char_set_funct1(s):
  return 123
def exce_char_set_funct2(s):
  return []
def exce_char_set_funct3(s):
  return None
def exce_char_set_funct3():
  return 'test'

# Define example data structures for corruptor
#
edit_corruptor = \
    corruptor.CorruptValueEdit(\
          position_function = corruptor.position_mod_normal,
          char_set_funct = basefunctions.char_set_ascii,
          insert_prob = 0.5,
          delete_prob = 0.5,
          substitute_prob = 0.0,
          transpose_prob = 0.0)

edit_corruptor2 = \
    corruptor.CorruptValueEdit(\
          position_function = corruptor.position_mod_uniform,
          char_set_funct = basefunctions.char_set_ascii,
          insert_prob = 0.25,
          delete_prob = 0.25,
          substitute_prob = 0.25,
          transpose_prob = 0.25)

surname_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(\
          lookup_file_name = '../lookup-files/surname-misspell.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

ocr_corruptor = corruptor.CorruptValueOCR(\
          position_function = corruptor.position_mod_normal,
          lookup_file_name = '../lookup-files/ocr-variations.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

keyboard_corruptor = corruptor.CorruptValueKeyboard(\
          position_function = corruptor.position_mod_normal,
          row_prob = 0.5,
          col_prob = 0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(\
          position_function = corruptor.position_mod_normal,
          lookup_file_name = '../lookup-files/phonetic-variations.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

missing_val_corruptor = corruptor.CorruptMissingValue()
postcode_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_val='missing')
given_name_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_value='unknown')

# Define example data structures for attr_mod_data_dictionary
#
attr_mod_data_dictionary1 = {'attr1':[(1.0,missing_val_corruptor)],
                            'attr2':[(0.1,surname_misspell_corruptor),
                                     (0.1,ocr_corruptor),
                                     (0.1,keyboard_corruptor),
                                     (0.7,phonetic_corruptor)]}
attr_mod_data_dictionary2 = {'attr3':[(0.1,edit_corruptor2),
                                      (0.1,ocr_corruptor),
                                      (0.1,keyboard_corruptor),
                                      (0.7,phonetic_corruptor)],
                            'attr4':[(0.8,keyboard_corruptor),
                                     (0.2,postcode_missing_val_corruptor)],
                            'attr5':[(0.1,edit_corruptor),
                                    (0.1,missing_val_corruptor),
                                    (0.4,keyboard_corruptor),
                                    (0.4,phonetic_corruptor)]}

# Exception data structure for attr_mod_data_dictionary
attr_mod_data_dictionary3 = {'attr6':[(1.0,edit_corruptor2)],
                            'attr7':[(0.7,missing_val_corruptor),
                                     (0.2,ocr_corruptor)],
                            'attr8':[(1.0,edit_corruptor)]}

# Define example data structures for attr_mod_prob_dictionary
#
attr_mod_prob_dictionary1 = {'attr1':0.4, 'attr2':0.6}
attr_mod_prob_dictionary2 = {'attr3':0.2,'attr4':0.3,'attr5':0.5}
# Exception data structure for attr_mod_prob_dictionary
attr_mod_prob_dictionary3 = {'attr6':0.3,'attr7':0.3,'attr8':0.3}

# Define argument test cases here
#
test_argument_data_dict = {
  ('corruptor','CorruptValue','constructor (__init__)'): \
    ['base',['position_function'],
     {'position_function':[[[test_function0],\
                            [test_function1],\
                            [test_function2]],
                          [[test_exce_function0],\
                           [test_exce_function1],\
                           [test_exce_function2],\
                           [{}],[[]],['test'],\
                           [''],[12.34],[None]]]}],

# 'position_function' is not required by this derived class
  ('corruptor','CorruptMissingValue','constructor (__init__)'): \
    ['derived',['missing_val'],
     {'missing_val':[[[''],['missing'],['n/a'],['unknown'],\
                      ['test'],['123.4']],
                     [[None],[123.4],[[]],[{}]]]}],

#
  ('corruptor','CorruptValueEdit','constructor (__init__)'): \
    ['derived',['position_function','char_set_funct','insert_prob',\
                'delete_prob','substitute_prob','transpose_prob'],
     {'position_function':\
               [[[test_function0,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [test_function1,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [test_function2,char_set_funct1,0.2,0.3,0.3,0.2]],\
                [[None,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [test_exce_function0,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [test_exce_function1,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [test_exce_function2,char_set_funct1,0.2,0.3,0.3,0.2],\
                 ['test',char_set_funct1,0.2,0.3,0.3,0.2],\
                 [123.4,char_set_funct1,0.2,0.3,0.3,0.2],\
                 [[],char_set_funct1,0.2,0.3,0.3,0.2],\
                 [{},char_set_funct1,0.2,0.3,0.3,0.2],\
                 ['',char_set_funct1,0.2,0.3,0.3,0.2]]],
      'char_set_funct':\
                [[[test_function0,char_set_funct1,0.2,0.3,0.3,0.2],\
                  [test_function0,char_set_funct2,0.2,0.3,0.3,0.2]],\
                 [[test_function0,exce_char_set_funct1,0.2,0.3,0.3,0.2],\
                  [test_function0,exce_char_set_funct2,0.2,0.3,0.3,0.2],\
                  [test_function0,exce_char_set_funct3,0.2,0.3,0.3,0.2],\
                  [test_function0,None,0.2,0.3,0.3,0.2],\
                  [test_function0,[],0.2,0.3,0.3,0.2],\
                  [test_function0,'',0.2,0.3,0.3,0.2],\
                  [test_function0,12.3,0.2,0.3,0.3,0.2],\
                  [test_function0,-110,0.2,0.3,0.3,0.2],\
                  [test_function0,{},0.2,0.3,0.3,0.2],\
                  [test_function0,'char_set_funct1',0.2,0.3,0.3,0.2]]],
      'insert_prob':\
                [[[test_function0,char_set_funct1,0.2,0.3,0.3,0.2],\
                  [test_function0,char_set_funct1,0.20,0.3000,0.3,0.200],\
                  [test_function0,char_set_funct1,0.25,0.0,0.65,0.100],\
                  [test_function0,char_set_funct1,0.5,0.5,0.0,0.0]],
                 [[test_function0,char_set_funct1,-0.2,0.5,0.5,0.0],\
                  [test_function0,char_set_funct1,0.2,0.3,0.3,0.3],\
                  [test_function0,char_set_funct1,10,20,30,40],\
                  [test_function0,char_set_funct1,'0.2','0.3','0.3','0.2'],\
                  [test_function0,char_set_funct1,0.3,0.2,None,None],\
                  [test_function0,char_set_funct1,None,None,None,None],\
                  [test_function0,char_set_funct1,[2,3,4,5],[2,3,4,5],\
                                                  [2,3,4,5],[2,3,4,5]],\
                  [test_function0,char_set_funct1,{},{},{},{}],\
                  [test_function0,char_set_funct1,0.2,0.3,0.2,0.19999]]],
      'delete_prob':\
              [[[test_function0,char_set_funct1,0.225,0.275,0.350,0.150],\
                [test_function0,char_set_funct1,0.5,0.0,0.4,0.1],\
                [test_function0,char_set_funct1,0.05,0.45,0.25,0.25]],
               [[test_function0,char_set_funct1,25,25,25,25],\
                [test_function0,char_set_funct1,'25%','30%','15%','30%'],\
                [test_function0,char_set_funct1,[0.2],[0.3],[0.3],[0.2]],\
                [test_function0,char_set_funct1,0.2,None,0.3,0.5],\
                [test_function0,char_set_funct1,0.2,'',0.3,0.5],\
                [test_function0,char_set_funct1,0.4,-0.4,0.3,0.3]]],
      'substitute_prob':\
             [[[test_function0,char_set_funct1,0.2,0.2,0.4,0.2],\
               [test_function0,char_set_funct1,0.200,0.350,0.350,0.100],\
               [test_function0,char_set_funct1,0.3,0.4,0.02,0.28]],
              [[test_function0,char_set_funct1,0.2,0.3,-0.3,0.2],\
               [test_function0,char_set_funct1,0.3,0.3,None,0.4],\
               [test_function0,char_set_funct1,0.4,0.3,'',0.3],\
               [test_function0,char_set_funct1,0.2,0.3,3.0,0.2],\
               [test_function0,char_set_funct1,0.2,0.3,[0.4],0.2]]],
      'transpose_prob':\
                [[[test_function0,char_set_funct1,0.2,0.2,0.2,0.4],\
                  [test_function0,char_set_funct1,0.200,0.300,0.498,0.002],\
                  [test_function0,char_set_funct1,0.2,0.3,0.5,0.0]],
                 [[test_function0,char_set_funct1,0.2,0.3,0.3,-0.2],\
                  [test_function0,char_set_funct1,0.2,0.3,0.3,'0.2'],\
                  [test_function0,char_set_funct1,0.4,0.3,0.3,[]],\
                  [test_function0,char_set_funct1,0.4,0.3,0.3,None],\
                  [test_function0,char_set_funct1,0.2,0.3,0.3,'20%']]]}],
#
  ('corruptor','CorruptValueKeyboard','constructor (__init__)'): \
    ['derived',['position_function','row_prob','col_prob'],
     {'position_function':[[[test_function0,0.4,0.6],\
                            [test_function1,0.4,0.6],\
                            [test_function2,0.4,0.6]],\
                          [[None,0.4,0.6],\
                           [test_exce_function0,0.4,0.6],\
                           [test_exce_function1,0.4,0.6],\
                           [test_exce_function2,0.4,0.6],\
                           ['test',0.4,0.6],\
                           [123.4,0.4,0.6],\
                           [[],0.4,0.6],\
                           [{},0.4,0.6],\
                           ['',0.4,0.6]]],
      'row_prob':[[[test_function0,0.4,0.6],\
                      [test_function0,0.5,0.5],\
                      [test_function0,0.0,1.0],\
                      [test_function0,0.9,0.1]],
                     [[test_function0,0.4,0.7],\
                      [test_function0,0.3,0.3],\
                      [test_function0,0.5,0.495],\
                      [test_function0,30,40],\
                      [test_function0,'0.3','0.2'],\
                      [test_function0,-0.3,0.7],\
                      [test_function0,None,None],\
                      [test_function0,[2,3,4,5],[2,3,4,5]],\
                      [test_function0,{},{}],\
                      [test_function0,0.2,0.19999]]],
      'col_prob':[[[test_function0,0.6,0.4],\
                      [test_function0,0.35,0.65],\
                      [test_function0,1.0,0.0]],
                     [[test_function0,1.0,-0.1],\
                      [test_function0,'15%','30%'],\
                      [test_function0,0.7,'0.3'],\
                      [test_function0,0.5,0.495],\
                      [test_function0,0.3,''],\
                      [test_function0,0.3,[0.5]],\
                      [test_function0,0.3,None]]]}],

#
  ('corruptor','CorruptValueOCR','constructor (__init__)'): \
    ['derived',['position_function','lookup_file_name','has_header_line',\
                'unicode_encoding'],
     {'position_function':
       [[[test_function0,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function1,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function2,'../lookup-files/ocr-variations.csv',False,'ascii']],
        [['','../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_exce_function0,'../lookup-files/ocr-variations.csv',\
                                                              False,'ascii'],
         [test_exce_function1,'../lookup-files/ocr-variations.csv',\
                                                              False,'ascii'],
         [test_exce_function2,'../lookup-files/ocr-variations.csv',\
                                                              False,'ascii'],
         ['test_exce_function0','../lookup-files/ocr-variations.csv',\
                                                              False,'ascii'],
         [{},'../lookup-files/ocr-variations.csv',False,'ascii'],
         [-12.54,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [[],'../lookup-files/ocr-variations.csv',False,'ascii'],
         [None,'../lookup-files/ocr-variations.csv',False,'ascii']]],
      'lookup_file_name':
       [[[test_function0,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function0,'../lookup-files/ocr-variations-upper-lower.csv',\
                                                             False,'ascii']],
        [[test_function0,None,False,'ascii'],
         [test_function0,'../lookup-files/gender-income.csv',False,'ascii'],
         [test_function0,'.../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function0,'',False,'ascii']]],
      'has_header_line':
       [[[test_function0,'../lookup-files/ocr-variations.csv',True,'ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',1,'ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',0,'ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',1.00,'ascii']],
        [[test_function0,'/lookup-files/ocr-variations.csv',None,'ascii'],
         [test_function0,'/lookup-files/ocr-variations.csv','true','ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',1.0001,'ascii'],
         [test_function0,'','1.0','ascii']]],
      'unicode_encoding':
       [[[test_function0,'../lookup-files/ocr-variations.csv',False,'ascii'],
         [test_function0,'../lookup-files/ocr-variations.csv',\
                                                     False,'iso-8859-1'],
         [test_function0,'../lookup-files/ocr-variations.csv',False,'ASCII'],
         [test_function0,'../lookup-files/ocr-variations.csv',\
                                                   False,'iso-2022-jp']],
        [[test_function0,'../lookup-files/ocr-variations.csv',False,''],
         [test_function0,'../lookup-files/ocr-variations.csv',False,'hello'],
         [test_function0,'../lookup-files/ocr-variations.csv',False,None]]]}],

#
# Position_function is not required by this corrupter derived class
  ('corruptor','CorruptValuePhonetic','constructor (__init__)'): \
    ['derived',['lookup_file_name','has_header_line',\
                'unicode_encoding'],
     {'lookup_file_name':
       [[['../lookup-files/phonetic-variations.csv',False,'ascii']],
        [[None,False,'ascii'],
         ['../lookup-files/gender-income.csv',False,'ascii'],
         ['.../lookup-files/phonetic-variations.csv',False,'ascii'],
         ['',False,'ascii']]],
      'has_header_line':
       [[['../lookup-files/phonetic-variations.csv',True,'ascii'],
         ['../lookup-files/phonetic-variations.csv',False,'ascii'],
         ['../lookup-files/phonetic-variations.csv',1,'ascii'],
         ['../lookup-files/phonetic-variations.csv',0,'ascii'],
         ['../lookup-files/phonetic-variations.csv',1.00,'ascii']],
        [['/lookup-files/phonetic-variations.csv',None,'ascii'],
         ['/lookup-files/phonetic-variations.csv','true','ascii'],
         ['../lookup-files/phonetic-variations.csv',1.0001,'ascii'],
         ['','1.0','ascii']]],
      'unicode_encoding':
       [[['../lookup-files/phonetic-variations.csv',False,'ascii'],
         ['../lookup-files/phonetic-variations.csv',\
                                                 False,'iso-8859-1'],
         ['../lookup-files/phonetic-variations.csv',False,'ASCII'],
         ['../lookup-files/phonetic-variations.csv',\
                                               False,'iso-2022-jp']],
        [['../lookup-files/phonetic-variations.csv',False,''],
         ['../lookup-files/phonetic-variations.csv',False,'hello'],
         ['../lookup-files/phonetic-variations.csv',False,None]]]}],

#
# Position_function is not required by this corrupter derived class
  ('corruptor','CorruptCategoricalValue','constructor (__init__)'): \
    ['derived',['lookup_file_name','has_header_line',\
                'unicode_encoding'],
     {'lookup_file_name':
       [[['../lookup-files/surname-misspell.csv',False,'ascii']],
        [[None,False,'ascii'],
         ['../lookup-files/gender-income.csv',False,'ascii'],
         ['.../lookup-files/surname-misspell.csv',False,'ascii'],
         ['',False,'ascii']]],
      'has_header_line':
       [[['../lookup-files/surname-misspell.csv',True,'ascii'],
         ['../lookup-files/surname-misspell.csv',False,'ascii'],
         ['../lookup-files/surname-misspell.csv',1,'ascii'],
         ['../lookup-files/surname-misspell.csv',0,'ascii'],
         ['../lookup-files/surname-misspell.csv',1.00,'ascii']],
        [['/lookup-files/surname-misspell.csv',None,'ascii'],
         ['/lookup-files/surname-misspell.csv','true','ascii'],
         ['../lookup-files/surname-misspell.csv',1.0001,'ascii'],
         ['','1.0','ascii']]],
      'unicode_encoding':
       [[['../lookup-files/surname-misspell.csv',False,'ascii'],
         ['../lookup-files/surname-misspell.csv',\
                                                     False,'iso-8859-1'],
         ['../lookup-files/surname-misspell.csv',False,'ASCII'],
         ['../lookup-files/surname-misspell.csv',\
                                                   False,'iso-2022-jp']],
        [['../lookup-files/surname-misspell.csv',False,''],
         ['../lookup-files/surname-misspell.csv',False,'hello'],
         ['../lookup-files/surname-misspell.csv',False,None]]]}],

#
  ('corruptor','CorruptDataSet','constructor (__init__)'): \
    ['derived',['number_of_mod_records','number_of_org_records',\
                'attribute_name_list','max_num_dup_per_rec',\
                'num_dup_dist','max_num_mod_per_attr',\
                'num_mod_per_rec','attr_mod_prob_dict',\
                'attr_mod_data_dict'],
     {'number_of_mod_records':
       [[[100,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [8345,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [9999,1000,['attr1','attr2'],10,'zipf',2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]],
        [['',1000,['attr1','attr2'],10,'zipf',2,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         ['10000',1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [100000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [{},1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [-10000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [100.25,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [[],1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [None,1000,['attr1','attr2'],10,'zipf',2,2,\
                 attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'number_of_org_records':
       [[[1000,500,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,999,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,12345,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,999999,['attr1','attr2'],10,'zipf',2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]],
        [[1000,'',['attr1','attr2'],10,'zipf',2,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,'500',['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,None,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,10,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,-500,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,[500],['attr1','attr2'],10,'zipf',2,2,\
                 attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'attribute_name_list':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr2','attr1'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',2,3,\
                   attr_mod_prob_dictionary2,attr_mod_data_dictionary2],
         [1000,1000,['attr4','attr5','attr3'],10,'zipf',3,3,\
                  attr_mod_prob_dictionary2,attr_mod_data_dictionary2]],
        [[1000,1000,['',''],10,'zipf',2,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,[],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,None,10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,('attr1','attr2'),10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr3','attr4'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                attr_mod_prob_dictionary2,attr_mod_data_dictionary2]]],

      'max_num_dup_per_rec':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],50,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],2,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],99,'zipf',2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]],
        [[1000,1000,['attr1','attr2'],'10','zipf',2,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10.5,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],-10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],None,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],[10],'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],{},'zipf',2,2,\
                 attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'num_dup_dist':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'uniform',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'poisson',2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]],
        [[1000,1000,['attr1','attr2'],10,'',2,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,None,2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf_dict',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,1234,2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,['zipf','uniform'],2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,{},2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'max_num_mod_per_attr':
       [[[1000,1000,['attr1','attr2'],10,'zipf',1,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',2,2,\
                 attr_mod_prob_dictionary2,attr_mod_data_dictionary2],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',1,2,\
                attr_mod_prob_dictionary2,attr_mod_data_dictionary2]],
        [[1000,1000,['attr1','attr2'],10,'zipf',-3,2, \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',3.5,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf','3',2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',None,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',{},2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf','',2,\
                 attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'num_mod_per_rec':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                  attr_mod_prob_dictionary1,attr_mod_data_dictionary1]],
        [[1000,1000,['attr1','attr2'],10,'zipf',2,'4', \
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,10,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,-4.5,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,[4],\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,None,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,'',\
                 attr_mod_prob_dictionary1,attr_mod_data_dictionary1]]],

      'attr_mod_prob_dict':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr4','attr5','attr3'],10,'zipf',3,3,\
                  attr_mod_prob_dictionary2,attr_mod_data_dictionary2]],
        [[1000,1000,['attr3','attr4','attr5'],10,'zipf',2,3, \
                   attr_mod_prob_dictionary3,attr_mod_data_dictionary2],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',1,3,\
                   attr_mod_prob_dictionary3,attr_mod_data_dictionary3],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',3,3,\
                   attr_mod_prob_dictionary2,attr_mod_data_dictionary3],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                 'attr_mod_prob_dictionary1',attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                          '',attr_mod_data_dictionary1],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                        [],attr_mod_data_dictionary1]]],

      'attr_mod_data_dict':
       [[[1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                   attr_mod_prob_dictionary1,attr_mod_data_dictionary1],
         [1000,1000,['attr3','attr4','attr5'],10,'zipf',3,3,\
                  attr_mod_prob_dictionary2,attr_mod_data_dictionary2]],
        [[1000,1000,['attr3','attr4','attr5'],10,'zipf',3,3, \
                   attr_mod_prob_dictionary3,attr_mod_data_dictionary3],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                 attr_mod_prob_dictionary1,[attr_mod_data_dictionary1]],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                   attr_mod_prob_dictionary1,[0.6,0.4]],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                          attr_mod_prob_dictionary1,''],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                          attr_mod_prob_dictionary1,[]],
         [1000,1000,['attr1','attr2'],10,'zipf',2,2,\
                                    attr_mod_prob_dictionary1,None]]]}],

}

# =============================================================================

class TestCase(unittest.TestCase):

  # Initialise test case  - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  def setUp(self):

    # Randomly generate different types of strings
    #
    self.letter_string_list = []
    self.digit_string_list = []
    self.mixed_string_list = []

    for t in range(num_tests):
      l_letter = random.randint(1,20)  # Random length of string
      l_digit = random.randint(1,10)
      l_mixed = random.randint(1,30)

      s_letter = ''
      for i in range(l_letter):
        s_letter += random.choice('abcdefghijklmnopqrstuvwxyz')
      s_digit = ''
      for i in range(l_digit):
        s_digit += random.choice('0123456789')
      s_mixed = ''
      for i in range(l_mixed):
        s_mixed += random.choice('012345678abcdefghijklmnopqrstuvwxyz')

      self.letter_string_list.append(s_letter)
      self.digit_string_list.append(s_digit)
      self.mixed_string_list.append(s_mixed)

  # Clean up test case  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  def tearDown(self):
    pass  # Nothing to clean up

  # ---------------------------------------------------------------------------
  # Start test cases

  def testArguments(self, test_data):
    """Test if a function or method can be called or initialised correctly with
       different values for their input arguments (parameters).

       The argument 'test_data' must be a dictionary with the following
       structure:

       - Keys are tuples consisting of three strings:
         (module_name, class_name, function_or_method_name)
       - Values are lists made of three elements:
         1) If this Class is a base class ('base') or a derived class
            ('derived'). These two require slightly different testing calls.
         2) A list that contains all the input arguments of the method, in the
            same order as the values of these arguments are given in the
            following dictionaries.
         3) Dictionaries where the keys are the names of the input argument
            that is being tested, and the values of these dictionaries are a
            list that contains two lists. The first list contains valid input
            arguments ('normal' argument tests) that should pass the test,
            while the second list contains illegal input arguments ('exception'
            argument tests) that should raise an exception.

         The lists of test cases are itself lists, each containing a number of
         input argument values, as many as are expected by the function or
         method that is being tested.

       This function returns a list containing the test results, where each
       list element is a string with comma separated values (CSV) which are to
       be written into the testing log file.
    """

    test_res_list = []  # The test results, one element per element in the test
                        # data dictionary

    for (test_method_names, test_method_data) in test_data.iteritems():

      test_type =                    test_method_data[0]
      method_keyword_argument_list = test_method_data[1]
      test_data_details =            test_method_data[2]

      assert test_type[:3] in ['bas','der']

      # For methods we need to test their __init__ function by calling the
      # name of the constructor, which is the name of the class.
      # (this is different from testing a function that is not in a class!)
      #
      test_method_name = test_method_names[1]

      print 'Testing arguments for method/function:', test_method_name

      for argument_name in test_data_details:
        print '  Testing input argument:', argument_name

        norm_test_data = test_data_details[argument_name][0]
        exce_test_data = test_data_details[argument_name][1]
        print '    Normal test cases:   ', norm_test_data
        print '    Exception test cases:', exce_test_data

        # Conduct normal tests - - - - - - - - - - - - - - - - - - - - - - - -
        #
        num_norm_test_cases =  len(norm_test_data)
        num_norm_test_passed = 0
        num_norm_test_failed = 0
        norm_failed_desc_str = ''

        for test_input in norm_test_data:
          passed = True  # Assume the test will pass :-)

          key_word_dict = {}
          for i in range(len(method_keyword_argument_list)):
            key_word_dict[method_keyword_argument_list[i]] = test_input[i]
          print 'Keyword dict normal:', key_word_dict

          if (test_type[:3] == 'bas'):
            try:
              getattr(corruptor,test_method_name)(key_word_dict)
            except:
              passed = False
          else:  # For derived classes
            try:
              getattr(corruptor,test_method_name)(**key_word_dict)
            except:
              passed = False

          # Now process test results
          #
          if (passed == False):
            num_norm_test_failed += 1
            norm_failed_desc_str += 'Failed test for input ' + \
                                    "'%s'; " % (str(test_input))
          else:
            num_norm_test_passed += 1

        assert num_norm_test_failed+num_norm_test_passed == num_norm_test_cases

        norm_test_result_str = test_method_names[0] + ',' + \
                               test_method_names[1] + ',' + \
                               test_method_names[2] + ',' + \
                               argument_name + ',normal,' + \
                               '%d,' % (num_norm_test_cases)
        if (num_norm_test_failed == 0):
          norm_test_result_str += 'all tests passed'
        else:
          norm_test_result_str += '%d tests failed,' % (num_norm_test_failed)
          norm_test_result_str += '"'+norm_failed_desc_str[:-2]+'"'

        test_res_list.append(norm_test_result_str)

        # Conduct exception tests - - - - - - - - - - - - - - - - - - - - - - -
        #
        num_exce_test_cases =  len(exce_test_data)
        num_exce_test_passed = 0
        num_exce_test_failed = 0
        exce_failed_desc_str = ''

        for test_input in exce_test_data:
          passed = True  # Assume the test will pass (i.e. raise an exception)

          key_word_dict = {}
          for i in range(len(method_keyword_argument_list)):
            key_word_dict[method_keyword_argument_list[i]] = test_input[i]
          print 'Keyword dict exception:', key_word_dict

          if (test_type[:3] == 'bas'):
            try:
              self.assertRaises(Exception,
                getattr(corruptor,test_method_name),key_word_dict)
            except:
              passed = False
          else:  # For derived classes
            try:
              self.assertRaises(Exception,
                getattr(corruptor,test_method_name),**key_word_dict)
            except:
              passed = False

          # Now process test results
          #
          if (passed == False):
            num_exce_test_failed += 1
            exce_failed_desc_str += 'Failed test for input ' + \
                                    "'%s'; " % (str(test_input))
          else:
            num_exce_test_passed += 1

        assert num_exce_test_failed+num_exce_test_passed == num_exce_test_cases

        exce_test_result_str = test_method_names[0] + ',' + \
                               test_method_names[1] + ',' + \
                               test_method_names[2] + ',' + \
                               argument_name + ',exception,' + \
                               '%d,' % (num_exce_test_cases)
        if (num_exce_test_failed == 0):
          exce_test_result_str += 'all tests passed'
        else:
          exce_test_result_str += '%d tests failed,' % (num_exce_test_failed)
          exce_test_result_str += '"'+exce_failed_desc_str[:-2]+'"'

        test_res_list.append(exce_test_result_str)

      test_res_list.append('')  # Empty line between tests of methods

    return test_res_list

  # ---------------------------------------------------------------------------

  def testFunct_position_mod_uniform(self):
    """Test that this position function only returns positions with then range
       of the given string length.
    """

    print 'Testing functionality of "position_mod_uniform"'

    num_passed = 0
    num_failed = 0

    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:
      t_len = len(test_str)
      pos = corruptor.position_mod_uniform(test_str)

      if (pos < 0) or (pos >= t_len):
        num_failed += 1
      else:
        num_passed += 1

    assert num_passed + num_failed == len(all_tests)
 
    test_result_str = 'corruptor,n/a,position_mod_uniform,' + \
                      'n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_position_mod_normal(self):
    """Test that this position function only returns positions with then range
       of the given string length.
    """

    print 'Testing functionality of "position_mod_normal"'

    num_passed = 0
    num_failed = 0

    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:
      t_len = len(test_str)
      pos = corruptor.position_mod_normal(test_str)

      if (pos < 0) or (pos >= t_len):
        num_failed += 1
      else:
        num_passed += 1

    assert num_passed + num_failed == len(all_tests)
 
    test_result_str = 'corruptor,n/a,position_mod_normal,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_CorruptMissingValue(self):
    """Test that this method only returns the specified missing value.
    """

    print 'Testing functionality of "CorruptMissingValue"'

    num_passed = 0
    num_failed = 0

    empty_corruptor = corruptor.CorruptMissingValue()
    miss_corruptor =  corruptor.CorruptMissingValue(missing_val = 'miss')
    na_corruptor =    corruptor.CorruptMissingValue(missing_val = 'n/a')

    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:
      passed = True
      res_str = empty_corruptor.corrupt_value(test_str)
      if (res_str != ''):
        passed = False

      res_str = miss_corruptor.corrupt_value(test_str)
      if (res_str != 'miss'):
        passed = False

      res_str = miss_corruptor.corrupt_value(test_str)
      if (res_str != 'miss'):
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == len(all_tests)

    test_result_str = 'corruptor,CorruptMissingValue,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_CorruptValueEdit(self):
    """Test that this method only returns modified values with a single edit
       according to the argument setting.
    """

    print 'Testing functionality of "CorruptValueEdit"'

    num_passed = 0
    num_failed = 0

    ins_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       1.0,
                           delete_prob =       0.0,
                           substitute_prob =   0.0,
                           transpose_prob =    0.0)

    del_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       0.0,
                           delete_prob =       1.0,
                           substitute_prob =   0.0,
                           transpose_prob =    0.0)

    sub_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       0.0,
                           delete_prob =       0.0,
                           substitute_prob =   1.0,
                           transpose_prob =    0.0)

    tra_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       0.0,
                           delete_prob =       0.0,
                           substitute_prob =   0.0,
                           transpose_prob =    1.0)

    ins_del_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       0.5,
                           delete_prob =       0.5,
                           substitute_prob =   0.0,
                           transpose_prob =    0.0)

    sub_tra_edit_corruptor = corruptor.CorruptValueEdit( \
                           position_function = corruptor.position_mod_uniform,
                           char_set_funct =    basefunctions.char_set_ascii,
                           insert_prob =       0.0,
                           delete_prob =       0.0,
                           substitute_prob =   0.5,
                           transpose_prob =    0.5)

    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:
      passed = True

      res_str = ins_edit_corruptor.corrupt_value(test_str)
      if (len(res_str) != len(test_str)+1):
        passed = False
      if test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      res_str = del_edit_corruptor.corrupt_value(test_str)
      if (len(res_str) != len(test_str)-1):
        passed = False
      if (res_str != '') and test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif (res_str != '') and test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      res_str = sub_edit_corruptor.corrupt_value(test_str)
      if (len(res_str) != len(test_str)):
        passed = False
      if test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      res_str = tra_edit_corruptor.corrupt_value(test_str)
      if (len(res_str) != len(test_str)):
        passed = False
      if test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      res_str = ins_del_edit_corruptor.corrupt_value(test_str)
      if (abs(len(res_str) - len(test_str)) != 1):
        passed = False
      if (res_str != '') and test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif (res_str != '') and test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      res_str = sub_tra_edit_corruptor.corrupt_value(test_str)
      if (len(res_str) != len(test_str)):
        passed = False
      if test_str.isalpha():
        if (not res_str.isalpha()):
          passed = False
      elif test_str.isdigit():
        if (not res_str.isdigit()):
          passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == len(all_tests)

    test_result_str = 'corruptor,CorruptValueEdit,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_CorruptValueKeyboard(self):
    """Test that this method only returns modified values with a single edit
       and correct character according to the argument setting.
    """

    print 'Testing functionality of "CorruptValueKeyboard"'

    num_passed = 0
    num_failed = 0

    rows = {'a':'s',  'b':'vn', 'c':'xv', 'd':'sf', 'e':'wr', 'f':'dg',
                 'g':'fh', 'h':'gj', 'i':'uo', 'j':'hk', 'k':'jl', 'l':'k',
                 'm':'n',  'n':'bm', 'o':'ip', 'p':'o',  'q':'w',  'r':'et',
                 's':'ad', 't':'ry', 'u':'yi', 'v':'cb', 'w':'qe', 'x':'zc',
                 'y':'tu', 'z':'x',
                 '1':'2',  '2':'13', '3':'24', '4':'35', '5':'46', '6':'57',
                 '7':'68', '8':'79', '9':'80', '0':'9'}

    cols = {'a':'qzw', 'b':'gh',  'c':'df', 'd':'erc','e':'ds34',
                 'f':'rvc', 'g':'tbv', 'h':'ybn', 'i':'k89',  'j':'umn',
                 'k':'im', 'l':'o', 'm':'jk',  'n':'hj',  'o':'l90', 'p':'0',
                 'q':'a12', 'r':'f45', 's':'wxz', 't':'g56',  'u':'j78',
                 'v':'fg', 'w':'s23',  'x':'sd', 'y':'h67',  'z':'as',
                 '1':'q',  '2':'qw', '3':'we', '4':'er', '5':'rt',  '6':'ty',
                 '7':'yu', '8':'ui', '9':'io', '0':'op'}

    row_keyboard_corruptor = corruptor.CorruptValueKeyboard( \
                           position_function = corruptor.position_mod_uniform,
                           row_prob =    1.0,
                           col_prob =    0.0)

    col_keyboard_corruptor = corruptor.CorruptValueKeyboard( \
                           position_function = corruptor.position_mod_uniform,
                           row_prob =       0.0,
                           col_prob =       1.0)


    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:
      passed = True
      test_str_mod_list = []
      res_str_mod_list =  []

      res_str = row_keyboard_corruptor.corrupt_value(test_str)

      if (len(res_str) != len(test_str)):
        passed = False

      else:
        for i in range(len(test_str)):
          if res_str[i] != test_str[i]:
            test_str_mod_list.append(test_str[i])
            res_str_mod_list.append(res_str[i])
        if ((len(test_str_mod_list) != 1) or (len(res_str_mod_list) != 1)):
          passed = False

        else:
          test_str_mod_char = test_str_mod_list[0]
          res_str_mod_char =  res_str_mod_list[0]
          row_chars = rows[test_str_mod_char]
          if res_str_mod_char not in row_chars:
            passed = False

      test_str_mod_list = []
      res_str_mod_list =  []

      res_str = col_keyboard_corruptor.corrupt_value(test_str)

      if (len(res_str) != len(test_str)):
        passed = False

      else:
        for i in range(len(test_str)):
          if res_str[i] != test_str[i]:
            test_str_mod_list.append(test_str[i])
            res_str_mod_list.append(res_str[i])
        if ((len(test_str_mod_list) != 1) or (len(res_str_mod_list) != 1)):
          passed = False

        else:
          test_str_mod_char = test_str_mod_list[0]
          res_str_mod_char = res_str_mod_list[0]
          col_chars = cols[test_str_mod_char]
          if res_str_mod_char not in col_chars:
            passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == len(all_tests)

    test_result_str = 'corruptor,CorruptValueKeyboard,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_CorruptValueOCR(self):
    """Test that this method returns modified values with the appropriate
       characters replaced according to the values in the lookup file.
    """

    print 'Testing functionality of "CorruptValueOCR"'

    num_passed = 0
    num_failed = 0

    max_chars = 3

    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
           '../lookup-files/ocr-variations.csv','ascii', False)

    ocr_dict = {}

    for ocr_pair_list in file_data:

      org_val = ocr_pair_list[0].strip()
      sub_val = ocr_pair_list[1].strip()

      if org_val not in ocr_dict:
        ocr_dict[org_val] = [sub_val]
      else:
        sub_val_list = ocr_dict[org_val]
        sub_val_list.append(sub_val)

      if sub_val not in ocr_dict:
        ocr_dict[sub_val] = [org_val]
      else:
        org_val_list = ocr_dict[sub_val]
        org_val_list.append(org_val)

    #print ocr_dict

    # Run the tests
    #
    all_tests = self.letter_string_list + self.digit_string_list + \
                self.mixed_string_list

    for test_str in all_tests:

      passed = True
      test_str_mod = u''
      res_str_mod =  u''

      res_str = ocr_corruptor.corrupt_value(test_str)

      if test_str != res_str:
        if (len(test_str) == len(res_str)): # same lenth
          passed = False
          iter_loop = True
          for i in range(len(test_str)):
            if res_str[i] != test_str[i]:
              x = 0
              while (iter_loop == True) and (x <= max_chars) and \
                                               ((i+x) < len(test_str)):
                test_str_mod += test_str[i+x]
                res_str_mod +=  res_str[i+x]
                if test_str_mod in ocr_dict:
                  subs_chars = ocr_dict[test_str_mod]
                  if res_str_mod in subs_chars:
                    passed = True
                    iter_loop = False
                x += 1

        else:    # different lengths          
          passed = False    
          if len(test_str) > len(res_str):
            smaller_string = res_str
            longer_string = test_str
          elif len(test_str) < len(res_str):
            smaller_string = test_str
            longer_string = res_str
          iter_loop = True
          for i in range(len(smaller_string)):
            test_str_mod = ''
            if smaller_string[i] != longer_string[i]:
              x = 0
              while (iter_loop == True) and (x <= max_chars) and \
                                     ((i+x) < len(longer_string)):
                test_str_mod += longer_string[i+x]
                y = 0
                res_str_mod = ''
                while (iter_loop == True) and (y <= max_chars) and \
                                     ((i+y) < len(smaller_string)):
                  res_str_mod +=  smaller_string[i+y]
                  if test_str_mod in ocr_dict:
                    subs_chars = ocr_dict[test_str_mod]
                    if res_str_mod in subs_chars:
                      passed = True
                      iter_loop = False
                  y += 1
                x += 1
            else:  # remaining characters in the longer string
              if i == len(smaller_string) - 1:
                test_str_mod = smaller_string[len(smaller_string) -1]
                res_str_mod = longer_string[len(smaller_string)-1:]
                if test_str_mod in ocr_dict:
                  subs_chars = ocr_dict[test_str_mod]
                  if res_str_mod in subs_chars:
                    passed = True


      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    #assert num_passed + num_failed == len(all_tests)

    test_result_str = 'corruptor,CorruptValueOCR,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']


  # ---------------------------------------------------------------------------

  def testFunct_CorruptValuePhonetic(self):
    """Test that this method returns modified values with the
       correct characters replaced according to the phonetic rules 
       specified in the lookup file.
    """

    print 'Testing functionality of "CorruptValuePhonetic"'

    num_passed = 0
    num_failed = 0

    max_chars = 5 # max number of characters that can be replaced  
                  # according to the lookup file

    slab_width = 2 # max number of characters to be searched for
                   # in forward and backward

    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
           '../lookup-files/phonetic-variations.csv','ascii', False)

    phonetic_dict = {}

    for rule_list in file_data:

      pos_val = rule_list[0].strip()
      org_val = rule_list[1].strip()
      sub_val = rule_list[2].strip()

      if org_val not in phonetic_dict:
        phonetic_dict[org_val] = [sub_val]
      else:
        sub_val_list = phonetic_dict[org_val]
        if sub_val not in sub_val_list:
          sub_val_list.append(sub_val)

      if sub_val not in phonetic_dict:
        phonetic_dict[sub_val] = [org_val]
      else:
        org_val_list = phonetic_dict[sub_val]
        if org_val not in org_val_list:
          org_val_list.append(org_val)  

    #print phonetic_dict

    # Load surnames from a lookup file
    #
    surname_list = []
    header_list,file_data = basefunctions.read_csv_file(\
         '../lookup-files/surname-misspell.csv','ascii', False)

    for val_pair in file_data:
      org_val = val_pair[0].strip()
      sub_val = val_pair[1].strip()

      if org_val not in surname_list:
        surname_list.append(org_val)
      if sub_val not in surname_list:
        surname_list.append(sub_val)

    # Run the tests
    #
    all_tests = self.letter_string_list + surname_list

    for test_str in all_tests:

      passed = True
      test_str_mod = u''
      res_str_mod =  u''

      res_str = phonetic_corruptor.corrupt_value(test_str)

      #test_str = 'szd'
      #res_str = 'sd'

      if test_str != res_str:
        if (len(test_str) == len(res_str)): # same length
          passed = False
          iter_loop = True
          for i in range(len(test_str)):
            if res_str[i] != test_str[i]:
              x = 0
              while (iter_loop == True) and (x <= max_chars) \
                                         and ((i+x) < len(test_str)):
                test_str_mod += test_str[i+x]
                res_str_mod +=  res_str[i+x]
                for k,v in phonetic_dict.items():
                  if (test_str_mod in k) or (k in test_str_mod):
                    subs_chars = phonetic_dict[k]
                    for v2 in subs_chars:
                      if (res_str_mod in v2) or (v2 in res_str_mod):
                        passed = True
                        iter_loop = False
                x += 1 

        else:   # different lengths       
          passed = False    
          if len(test_str) > len(res_str):
            smaller_string = res_str
            longer_string = test_str
          elif len(test_str) < len(res_str):
            smaller_string = test_str
            longer_string = res_str
          iter_loop = True
          for i in range(len(smaller_string)):
            test_str_mod = ''
            if smaller_string[i] != longer_string[i]:
              if (i >= slab_width):
                x = -slab_width
              else:
                x = -i
              while (iter_loop == True) and (x <= max_chars) \
                                     and (0 <= (i+x) < len(longer_string)):
                test_str_mod += longer_string[i+x]
                if (i >= slab_width):
                  y = -slab_width
                else:
                  y = -i
                res_str_mod = ''
                while (iter_loop == True) and (y <= max_chars) \
                                    and (0 <= (i+y) < len(smaller_string)):
                  res_str_mod +=  smaller_string[i+y]
                  for k,v in phonetic_dict.items():
                    if (test_str_mod in k) or (k in test_str_mod):
                      subs_chars = phonetic_dict[k]
                      for v2 in subs_chars:
                        if (res_str_mod in v2) or (v2 in res_str_mod):
                          passed = True
                          iter_loop = False
                  y += 1
                x += 1
            else:   # remaining characters of longer string
              if (i == len(smaller_string) - 1):  
                if (len(smaller_string) > slab_width):
                  test_str_mod = smaller_string[len(smaller_string)-1-slab_width:]
                else:
                  test_str_mod = smaller_string[len(smaller_string)-1-i:]
                if (len(longer_string) > slab_width):
                  res_str_mod = longer_string[len(smaller_string)-1-slab_width:]
                else:
                  res_str_mod = longer_string[len(smaller_string)-1-i:]
                for k,v in phonetic_dict.items():
                  if (test_str_mod in k) or (k in test_str_mod):
                    subs_chars = phonetic_dict[k]
                    for v2 in subs_chars:
                      if (res_str_mod in v2) or (v2 in res_str_mod):
                        passed = True

          if passed == False:
             # check for characters removed from the original str -test_str
             diff_list = []
             d = difflib.Differ()
             l = list(d.compare(test_str, res_str))
             for diff_val in l:
               if diff_val.startswith("- "):
                 diff_list.append(diff_val[-1:])
             if (len(test_str) - len(res_str) == 1):
               if (len(diff_list) == 1) and (diff_list[0] \
                                                     in ['h','e','w','x']):
                 passed = True
             elif (len(test_str) - len(res_str) == 2):
               if (len(diff_list) == 2):
                 if ('g' in diff_list) and ('h' in diff_list):
                   passed = True
                 elif ('x' in diff_list) and ('c' in diff_list):
                   passed = True
                 elif diff_list[0]=='x' and diff_list[1]=='x':
                   passed = True


          if passed == False:
             print 'fail test,',test_str,res_str,test_str_mod,res_str_mod

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == len(all_tests)

    test_result_str = 'corruptor,CorruptValuePhonetic,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(all_tests))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']


  # ---------------------------------------------------------------------------

  def testFunct_CorruptCategoricalValue(self):
    """Test that this method only returns modified values with the correct
       misspelling according to the argument setting.
    """

    print 'Testing functionality of "CorruptCategoricalValue"'

    num_passed = 0
    num_failed = 0

    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
         '../lookup-files/surname-misspell.csv','ascii', False)

    misspell_dict = {}
    org_val_list = []

    for misspell_pair_list in file_data:

      org_val = misspell_pair_list[0].strip()
      sub_val = misspell_pair_list[1].strip()

      if org_val not in misspell_dict:
        misspell_dict[org_val] = [sub_val]
        org_val_list.append(org_val)
      else:
        sub_val_list = misspell_dict[org_val]
        sub_val_list.append(sub_val)

    #print misspell_dict

    # Run the tests
    #

    for test_str in org_val_list:
      passed = True

      res_str = surname_misspell_corruptor.corrupt_value(test_str)

      if (res_str != test_str):
        if (res_str not in misspell_dict[test_str]):
          passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == len(org_val_list)

    test_result_str = 'corruptor,CorruptCategoricalValue,corrupt_value,' + \
                      'n/a,funct,%d,' % (len(org_val_list))
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

# =============================================================================
# Generate a time string to be used for the log file
#
curr_time_tuple = time.localtime()
curr_time_str = str(curr_time_tuple[0]) + str(curr_time_tuple[1]).zfill(2) + \
                str(curr_time_tuple[2]).zfill(2) + '-' + \
                str(curr_time_tuple[3]).zfill(2) + \
                str(curr_time_tuple[4]).zfill(2)

# Write test output header line into the log file
#
out_file_name = './logs/corruptorTest-%s.csv' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write('Test results generated by corruptorTest.py'  + os.linesep)

out_file.write('Test started: ' + curr_time_str + os.linesep)

out_file.write(os.linesep)

out_file.write('Module name,Class name,Method name,Arguments,Test_type,' + \
               'Patterns tested,Summary,Failure description' + os.linesep)
out_file.write(os.linesep)

# Create instances for the testcase class that calls all tests
#
test_res_list = []
test_case_ins = TestCase('testArguments')
test_res_list += test_case_ins.testArguments(test_argument_data_dict)

# Add inidividual functionality tests here
#
test_case_ins = TestCase('testFunct_position_mod_uniform')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_position_mod_uniform()

test_case_ins = TestCase('testFunct_position_mod_normal')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_position_mod_normal()

test_case_ins = TestCase('testFunct_CorruptMissingValue')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptMissingValue()

test_case_ins = TestCase('testFunct_CorruptValueEdit')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptValueEdit()

test_case_ins = TestCase('testFunct_CorruptValueKeyboard')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptValueKeyboard()

test_case_ins = TestCase('testFunct_CorruptValueOCR')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptValueOCR()

test_case_ins = TestCase('testFunct_CorruptValuePhonetic')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptValuePhonetic()

test_case_ins = TestCase('testFunct_CorruptCategoricalValue')
test_case_ins.setUp()
test_res_list += test_case_ins.testFunct_CorruptCategoricalValue()

# Write test output results into the log file
#
for line in test_res_list:
  out_file.write(line + os.linesep)

out_file.close()

print 'Test results are written to', out_file_name

for line in test_res_list:
  print line

# =============================================================================
