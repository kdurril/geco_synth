# generatorTest.py - Test module that provides testing functions for the
#                    module generator.py of the data generation system.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for generator.py.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then system modules)

import os
import random
import sys
import time
import unittest
sys.path.append('..')

import generator
import basefunctions
import attrgenfunct
import contdepfunct

random.seed(42)  # Set seed for random generator

# =============================================================================

# Define the number of tests to be done for the functionality tests
#
num_tests = 10000

# Define dummy correct test functions with between 0 and 5 arguments and that
# return a string
#
def test_function0():
  return 'test0'
def test_function1(a1):
  return 'test1: '+str(a1)
def test_function2(a1,a2):
  return 'test2: '+str(a1)+','+str(a2)
def test_function3(a1,a2,a3):
  return 'test3: '+str(a1)+','+str(a2)+','+str(a3)
def test_function4(a1,a2,a3,a4):
  return 'test4: '+str(a1)+','+str(a2)+','+str(a3)+','+str(a4)
def test_function5(a1,a2,a3,a4,a5):
  return 'test5: '+str(a1)+','+str(a2)+','+str(a3)+','+str(a4)+','+str(a5)

# Define several functions that should trigger an exception
#
def test_exce_function0():
  return 999.99
def test_exce_function1():
  return 1999
def test_exce_function2(a1,a2,a3,a4,a5,a6):
  return ''

# Define dummy correct test functions that take a floating-point value as 
# input and that return a floating-point value
def test_cont_function1(f1):
  return f1*2.0
def test_cont_function2(f1):
  return f1
def test_cont_function3(f1):
  return 10.0
def test_cont_function4(f1):
  return -123.456

# Define dummy exception test functions that do not
# return a floating-point value
def test_exce_cont_function1(f1):
  return str(f1*2.0)
def test_exce_cont_function2(f1):
  return int(10)
def test_exce_cont_function3(f1):
  return 'test'

# Define example data structures for attributes
#
gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'attr1',
      freq_file_name = '../lookup-files/givenname_f_freq.csv',
      has_header_line = False,
      unicode_encoding = 'ascii')

postcode_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'attr2',
      freq_file_name = '../lookup-files/postcode_act_freq.csv',
      has_header_line = False,
      unicode_encoding = 'ascii')

age_uniform_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'attr3',
      function = attrgenfunct.generate_uniform_age,
      parameters = [0,120])

gender_city_comp_attr = \
    generator.GenerateCateCateCompoundAttribute(\
      categorical1_attribute_name = 'gender',
      categorical2_attribute_name = 'city',
      lookup_file_name = '../lookup-files/gender-city.csv',
      has_header_line = True,
      unicode_encoding = 'ascii')

gender_income_comp_attr = \
    generator.GenerateCateContCompoundAttribute(\
          categorical_attribute_name = 'gender2',
          continuous_attribute_name = 'income',
          continuous_value_type = 'float1',
          lookup_file_name = '../lookup-files/gender-income.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

gender_city_income_comp_attr = \
    generator.GenerateCateCateContCompoundAttribute(\
          categorical1_attribute_name = 'gender3',
          categorical2_attribute_name = 'city2',
          continuous_attribute_name = 'income2',
          continuous_value_type = 'float4',
          lookup_file_name = '../lookup-files/gender-city-income.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

age_blood_pressure_comp_attr = \
    generator.GenerateContContCompoundAttribute(\
          continuous1_attribute_name = 'age',
          continuous2_attribute_name = 'blood-pressure',
          continuous1_funct_name =     'uniform',
          continuous1_funct_param =    [10,110],
          continuous2_function = contdepfunct.blood_pressure_depending_on_age,
          continuous1_value_type = 'int',
          continuous2_value_type = 'float3')

# Define example attribute data lists 
#
attr_data_list1 = [gname_attr]
attr_data_list2 = [gname_attr, postcode_attr]
attr_data_list3 = [gname_attr, postcode_attr, age_uniform_attr]
attr_data_list4 = [gname_attr, gender_city_comp_attr, postcode_attr]

# Define argument test cases here
#
test_argument_data_dict = {
  ('generator','GenerateAttribute','constructor (__init__)'): \
    ['base',['attribute_name'],
     {'attribute_name':[[['test'],['1234'],['myattribute']],
                        [[''],[12],[12.54],[{}],[[]]]]}],
#
  ('generator','GenerateFuncAttribute','constructor (__init__)'): \
    ['derived',['attribute_name','function','parameters'],
     {'attribute_name':[[['test',test_function0,[]],
                         ['1234',test_function1,[66]],
                         ['myattribute',test_function2,[66,'pop']],
                         ['myatt1',test_function3,['pop2','55','']],
                         ['myatt2',test_function4,[11,22,33,44]],
                         ['myatt',test_function5,[11,None,'33',44,'55']]],
                        [['',test_function0,[]],
                         [1234,test_function1,[66]],
                         [{},test_function2,[66,'pop']],
                         [-12.54,test_function3,['pop2','55','']],
                         [[],test_function4,[11,22,33,44]],
                         [None,test_function5,[11,None,'33',44,'55']]]],
      'function':[[['test',test_function0,[]],
                   ['1234',test_function1,[66]],
                   ['myattribute',test_function2,[66,'pop']],
                   ['myatt1',test_function3,['pop2','55','']],
                   ['myatt2',test_function4,[11,22,33,44]],
                   ['myatt',test_function5,[11,None,'33',44,'55']]],
                  [['test',test_exce_function0,None],
                   ['1234',test_exce_function1,[66]],
                   ['myattribute',test_exce_function2,[66,'pop']]]],
      'parameters':[[['test',test_function0,[]],
                     ['1234',test_function1,[66]],
                     ['myattribute',test_function2,[66,'pop']],
                     ['myatt1',test_function3,['pop2','55','']],
                     ['myatt2',test_function4,[11,22,33,44]],
                     ['myatt',test_function5,[11,None,'33',44,'55']]],
                    [['test',test_function0,[1,2,3,4,5,6,7,8]],
                     ['1234',test_function1,[66,6,7,4,8,56,9,0,66]],
                     ['myattribute',test_function2,['pop']],
                     ['myatt1',test_function3,[{}]]]]}],

#
  ('generator','GenerateFreqAttribute','constructor (__init__)'): \
    ['derived',['attribute_name','freq_file_name','has_header_line',\
                'unicode_encoding'],
     {'attribute_name':
       [[['test','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['1234','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myattribute','../lookup-files/givenname_f_freq.csv',\
                                                        False,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt2','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt','../lookup-files/givenname_f_freq.csv',False,'ascii']],
        [['','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         [1234,'../lookup-files/givenname_f_freq.csv',False,'ascii'],
         [{},'../lookup-files/givenname_f_freq.csv',False,'ascii'],
         [-12.54,'../lookup-files/givenname_f_freq.csv',False,'ascii'],
         [[],'../lookup-files/givenname_f_freq.csv',False,'ascii'],
         [None,'../lookup-files/givenname_f_freq.csv',False,'ascii']]],
      'freq_file_name':
       [[['myatt1','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt1','../lookup-files/givenname_m_freq.csv',False,'ascii'],
         ['myatt1','../lookup-files/postcode_act_freq.csv',False,'ascii']],
        [['myatt1',None,False,'ascii'],
         ['myatt1','../lookup-files/gender-income.csv',False,'ascii'],
         ['myatt1','.../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt1','',False,'ascii']]],
      'has_header_line':
       [[['myatt1','../lookup-files/givenname_f_freq.csv',True,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',1,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',0,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',1.00,'ascii']],
        [['myatt1','/lookup-files/givenname_f_freq.csv',None,'ascii'],
         ['myatt1','/lookup-files/givenname_f_freq.csv','true','ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',1.0001,'ascii'],
         ['myatt1','','1.0','ascii']]],
      'unicode_encoding':
       [[['myatt1','../lookup-files/givenname_f_freq.csv',False,'ascii'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',\
                                                     False,'iso-8859-1'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',False,'ASCII'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',\
                                                   False,'iso-2022-jp']],
        [['myatt1','../lookup-files/givenname_f_freq.csv',False,''],
         ['myatt1','../lookup-files/givenname_f_freq.csv',False,'hello'],
         ['myatt1','../lookup-files/givenname_f_freq.csv',False,None]]]}],

# 'GenerateCompoundAttribute' base class does not have any arguments to be
# initialiszed
#
  ('generator','GenerateCateCateCompoundAttribute','constructor (__init__)'): \
    ['derived',['categorical1_attribute_name','categorical2_attribute_name',\
                'lookup_file_name','has_header_line','unicode_encoding'],
     {'categorical1_attribute_name':
       [[['myattr1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['attr1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['attribute1','myattr2','../lookup-files/gender-city.csv',\
                                                                True,'ascii'],
         ['Surname','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['att1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['1234','myattr2','../lookup-files/gender-city.csv',True,'ascii']],
        [['','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         [1234,'myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         [{},'myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         [-12.54,'myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         [[],'myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         [None,'myattr2','../lookup-files/gender-city.csv',True,'ascii']]],
      'categorical2_attribute_name':
       [[['myatt1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','attribute2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','attr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','myatt2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','att2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','Given Name','../lookup-files/gender-city.csv',\
                                                           True,'ascii']],
        [['myatt1','','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1',1234,'../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1',{},'../lookup-files/gender-city.csv',True,'ascii'],
         ['myattr1',[],'../lookup-files/gender-city.csv',True,'ascii'],
         ['myattr1',-12.34,'../lookup-files/gender-city.csv',True,'ascii'],
         ['myattr1',None,'../lookup-files/gender-city.csv',True,'ascii']]],
      'lookup_file_name':
       [[['myatt1','myattr2','../lookup-files/gender-city.csv',True,'ascii']],
        [['myatt1','myattr2',None,True,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                             True,'ascii'],
         ['myatt1','myattr2','.../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','myattr2','',True,'ascii']]],
      'has_header_line':
       [[['myatt1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',1,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',1.00,'ascii']],
        [['myatt1','myattr2','../lookup-files/gender-city.csv',None,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',False,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',1.0001,'ascii'],
         ['myatt1','myattr2','','1.0','ascii']]],
      'unicode_encoding':
       [[['myatt1','myattr2','../lookup-files/gender-city.csv',True,'ascii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',\
                                                         True,'iso-8859-1'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',\
                                                              True,'ASCII'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',\
                                                       True,'ISO-2022-JP']],
        [['myatt1','myattr2','../lookup-files/gender-city.csv',True,''],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',True,'asciii'],
         ['myatt1','myattr2','../lookup-files/gender-city.csv',True,None]]]}],

#
  ('generator','GenerateCateContCompoundAttribute','constructor (__init__)'): \
    ['derived',['categorical_attribute_name','continuous_attribute_name',\
                'lookup_file_name','has_header_line','unicode_encoding',\
                'continuous_value_type'],
     {'categorical_attribute_name':
       [[['myattr1','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         ['attr1','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         ['attribute1','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         ['Surname','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         ['att1','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         ['1234','myattr2','../lookup-files/gender-income.csv',False,\
                                                               'ascii','int']],
        [['','myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         [1234,'myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         [{},'myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         [-12.54,'myattr2','../lookup-files/gender-income.csv',False,\
                                                                'ascii','int'],
         [[],'myattr2','../lookup-files/gender-income.csv',False,\
                                                               'ascii','int'],
         [None,'myattr2','../lookup-files/gender-income.csv',False,\
                                                             'ascii','int']]],
      'continuous_attribute_name':
       [[['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         False,'ascii','int'],
         ['myatt1','attribute2','../lookup-files/gender-income.csv',\
                                                         False,'ascii','int'],
         ['myatt1','attr2','../lookup-files/gender-income.csv',\
                                                         False,'ascii','int'],
         ['myatt1','myatt2','../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1','att2','../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1','Given Name','../lookup-files/gender-income.csv',\
                                                       False,'ascii','int']],
        [['myatt1','','../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1',1234,'../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1',{},'../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myattr1',[],'../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myattr1',-12.34,'../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myattr1',None,'../lookup-files/gender-income.csv',\
                                                      False,'ascii','int']]],
      'lookup_file_name':
       [[['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                       False,'ascii','int']],
        [['myatt1','myattr2',None,False,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/givenname_m_freq.csv',\
                                                        False,'ascii','int'],
         ['myatt1','myattr2','.../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1','myattr2','',False,'ascii','int']]],
      'has_header_line':
       [[['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         False,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         False,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                            1,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                            0,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                        1.00,'ascii','int']],
        [['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         None,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                           '','ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                       'true','ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                       1.0001,'ascii','int'],
         ['myatt1','myattr2','','1.0','ascii','int']]],
      'unicode_encoding':
       [[['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                   False,'iso-8859-1','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                        False,'ASCII','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                 False,'ISO-2022-JP','int']],
        [['myatt1','myattr2','../lookup-files/gender-income.'\
                                        'csv',False,'','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                       False,'asciii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         False,None,'int']]],
      'continuous_value_type':
       [[['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                        False,'ascii','int'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float1'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float2'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float3'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float4'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float5'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float6'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float7'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                     False,'ascii','float8'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                    False,'ascii','float9']],
        [['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                           False,'ascii',''],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                         False,'ascii',None],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                      False,'ascii','float'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                    False,'ascii','float10'],
         ['myatt1','myattr2','../lookup-files/gender-income.csv',\
                                                False,'ascii','integer']]]}],

#
  ('generator','GenerateCateCateContCompoundAttribute',
           'constructor (__init__)'): \
    ['derived',['categorical1_attribute_name','categorical2_attribute_name',\
                'continuous_attribute_name','lookup_file_name',
                'has_header_line','unicode_encoding','continuous_value_type'],
     {'categorical1_attribute_name':
       [[['myattr1','myattr2','myattr3',
                '../lookup-files/gender-city-income.csv',False,'ascii','int'],
         ['attr1','myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         ['attribute1','myattr2','myattr3','../lookup-files/gender-city-income'
                                                    '.csv',False,'ascii','int'],
         ['Surname','myattr2','myattr3',
               '../lookup-files/gender-city-income.csv',False,'ascii','int'],
         ['att1','myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                         False,'ascii','int'],
         ['1234','myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                         False,'ascii','int']],
        [['','myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         [1234,'myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         [{},'myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         [-12.54,'myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         [[],'myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         [None,'myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                         False,'ascii','int']]],
      'categorical2_attribute_name':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-income.csv',
                                                          False,'ascii','int'],
         ['myatt1','attribute2','myattr3',
          '../lookup-files/gender-city-income.csv',False,'ascii','int'],
         ['myatt1','attr2','myattr3','../lookup-files/gender-city-income.csv',
                                                           False,'ascii','int'],
         ['myatt1','myatt2','myattr3','../lookup-files/gender-city-income.csv',
                                                           False,'ascii','int'],
         ['myatt1','att2','myattr3','../lookup-files/gender-city-income.csv',
                                                           False,'ascii','int'],
         ['myatt1','Given Name','myattr3','../lookup-files/gender-city-income'\
                                                   '.csv',False,'ascii','int']],
        [['myatt1','','myattr3','../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1',1234,'myattr3','../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1',{},'myattr3','../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1',[],'myattr3','../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1',-12.34,'myattr3','../lookup-files/gender-city-income.'\
                                                    'csv',False,'ascii','int'],
         ['myatt1',None,'myattr3','../lookup-files/gender-city-income.'\
                                                  'csv',False,'ascii','int']]],
      'continuous_attribute_name':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-income.'\
                                                    'csv',False,'ascii','int'],
         ['myatt1','myattr2','attr3','../lookup-files/gender-city-income.'\
                                                    'csv',False,'ascii','int'],
         ['myatt1','myattr2','att3','../lookup-files/gender-city-income.'\
                                                    'csv',False,'ascii','int'],
         ['myatt1','myattr2','myattribute3','../lookup-files/gender-city-'\
                                             'income.csv',False,'ascii','int'],
         ['myatt1','myattr2','Suburb','../lookup-files/gender-city-income'\
                                                   '.csv',False,'ascii','int'],
         ['myatt1','myattr2','1234','../lookup-files/gender-city-income.'\
                                                   'csv',False,'ascii','int']],
        [['myatt1','myattr2','','../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1','myattr2',1234,'../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myatt1','myattr2',-12.34,'../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myattr1','myattr2',None,'../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myattr1','myattr2',[],'../lookup-files/gender-city-income.csv',\
                                                          False,'ascii','int'],
         ['myattr1','myattr2',{},'../lookup-files/gender-city-income.csv',\
                                                        False,'ascii','int']]],
      'lookup_file_name':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv',False,'ascii','int']],
        [['myatt1','myattr2','myattr3',None,False,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-'\
                                               'city.csv',False,'ascii','int'],
         ['myatt1','myattr2','myattr3','.../lookup-files/gender-city-'\
                                             'income.csv',False,'ascii','int'],
         ['myatt1','myattr2','myattr3','',False,'ascii','int']]],
      'has_header_line':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                              'income.csv',True,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                             'income.csv',False,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                                 'income.csv',1,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                                 'income.csv',0,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                             'income.csv',1.00,'ascii','int']],
        [['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                              'income.csv',None,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv','true','ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv',1.0001,'ascii','int'],
         ['myatt1','myattr2','myattr3','','1.0','ascii','int']]],
      'unicode_encoding':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                             'income.csv',False,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                        'income.csv',False,'iso-8859-1','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                             'income.csv',False,'ASCII','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                      'income.csv',False,'ISO-2022-JP','int']],
        [['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                                  'income.csv',False,'','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv',False,'asciii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv',False,None,'int']]],
      'continuous_value_type':
       [[['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                            'income.csv',False,'ascii','int'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float1'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float2'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float3'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float4'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float5'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float6'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float7'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                         'income.csv',False,'ascii','float8'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                        'income.csv',False,'ascii','float9']],
        [['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                               'income.csv',False,'ascii',''],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                             'income.csv',False,'ascii',None],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                          'income.csv',False,'ascii','float'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                        'income.csv',False,'ascii','float10'],
         ['myatt1','myattr2','myattr3','../lookup-files/gender-city-'\
                                    'income.csv',False,'ascii','integer']]]}],

#
  ('generator','GenerateContContCompoundAttribute','constructor (__init__)'): \
    ['derived',['continuous1_attribute_name','continuous2_attribute_name',\
                'continuous1_funct_name','continuous1_funct_param',\
                'continuous2_function','continuous1_value_type',\
                'continuous2_value_type'],
     {'continuous1_attribute_name':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['1234','myattr2','uniform',[20,100],test_cont_function1,
                                                           'int','float1'],
         ['myattribute','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['test','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt2','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float1']],
        [['','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         [1234,'myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         [{},'myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         [-12.54,'myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         [[],'myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         [None,'myattr2','uniform',[20,100],test_cont_function1,\
                                                         'int','float1']]],
      'continuous2_attribute_name':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myatt2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','attribute2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','2ndattribute','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','Given Name','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','1234','uniform',[20,100],test_cont_function1,\
                                                          'int','float1']],
        [['myatt1','','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1',1234,'uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1',-12.34,'uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1',{},'uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1',[],'uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1',None,'uniform',[20,100],test_cont_function1,\
                                                         'int','float1']]],
      'continuous1_funct_name':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[50,10,0,100],test_cont_function1,\
                                                           'int','float1']],
        [['myatt1','myattr2','',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','unform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2',None,[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2',[],[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2',{},[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','nomal',[50,10,0,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2',1234,[50,10,0,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','norm_fun',[50,10,0,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2',['normal'],[50,10,0,100],\
                                     test_cont_function1,'int','float1']]],
      'continuous1_funct_param':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20.0,100.0],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[-20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[50,10,0,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30,20,10,120],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30.8,2.0,-10,120],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30,20,10,None],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30,20,None,120],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30,20,None,None],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[70,20,-10,200],test_cont_function1,\
                                                          'int','float1']],
          # min_val > max_val
        [['myatt1','myattr2','uniform',[100,20],test_cont_function1,\
                                                           'int','float1'],
          # min_val = max_val
         ['myatt1','myattr2','uniform',[30,30],test_cont_function1,\
                                                           'int','float1'],
          # 2 args for normal function, 4 required
         ['myatt1','myattr2','normal',[30,10],test_cont_function1,\
                                                           'int','float1'],
          # min_val > max_val
         ['myatt1','myattr2','normal',[30,20,100,10],test_cont_function1,\
                                                           'int','float1'],
          # min_val = max_val
         ['myatt1','myattr2','normal',[30,20,10,10],test_cont_function1,\
                                                           'int','float1'],
          # mu < min_val
         ['myatt1','myattr2','normal',[30,20,40,100],test_cont_function1,\
                                                           'int','float1'],
          # mu > max_val
         ['myatt1','myattr2','normal',[30,20,10,20],test_cont_function1,\
                                                           'int','float1'],
          # sigma < 0
         ['myatt1','myattr2','normal',[30,-20,10,120],test_cont_function1,\
                                                           'int','float1'],
          # sigma = 0
         ['myatt1','myattr2','normal',[30,0,10,120],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',[30,20,'',''],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','normal',['30','20','10','120'],\
                                     test_cont_function1,'int','float1']]],
      'continuous2_function':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function2,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function3,\
                                                           'int','float1']],
        [['myatt1','myattr2','uniform',[20,100],test_exce_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_exce_cont_function2,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_exce_cont_function3,\
                                                         'int','float1']]],
      'continuous1_value_type':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float1','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float2','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float3','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float4','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float5','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float6','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float7','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float8','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float9','float1']],
        [['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'float','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                             '','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                    'integer','float1']]],
      'continuous2_value_type':
       [[['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                             'int','int'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float1'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float2'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float3'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float4'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float5'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float6'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float7'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                          'int','float8'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                         'int','float9']],
        [['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                           'int','float'],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,'int',''],
         ['myatt1','myattr2','uniform',[20,100],test_cont_function1,\
                                                        'int','integer']]]}],
#
  ('generator','GenerateDataSet','constructor (__init__)'): \
    ['derived',['output_file_name','write_header_line',\
             'rec_id_attr_name','number_of_records','attribute_name_list',\
             'attribute_data_list','unicode_encoding'],
     {'output_file_name':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.log',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.txt',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test2.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                 attr_data_list2,'ascii']],
        [['',True,'rec_id',1000,['attr1','attr2'],attr_data_list2,'ascii'],
         [1234,True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         [{},True,'rec_id',1000,['attr1','attr2'],attr_data_list2,'ascii'],
         [-12.54,True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         [[],True,'rec_id',1000,['attr1','attr2'],attr_data_list2,'ascii'],
         [None,True,'rec_id',1000,['attr1','attr2'],\
                                                attr_data_list2,'ascii']]],
      'write_header_line':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',False,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',1,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',0,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',1.00,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',0.0,'rec_id',1000,['attr1','attr2'],\
                                                 attr_data_list2,'ascii']],
        [['test.csv','','rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv','True','rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',1234,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',{},'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',[],'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',-12.34,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',None,'rec_id',1000,['attr1','attr2'],\
                                                attr_data_list2,'ascii']]],
      'rec_id_attr_name':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_num',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'num',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'test',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'1234',1000,['attr1','attr2'],\
                                                 attr_data_list2,'ascii']],
        [['test.csv',True,'',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,1234,1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,-12.34,1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,None,1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,[],1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,{},1000,['attr1','attr2'],\
                                                attr_data_list2,'ascii']]],
      'number_of_records':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',10000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',1234,['attr1','attr2'],\
                                                 attr_data_list2,'ascii']],
        [['test.csv',True,'rec_id',None,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id','1000',['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',123.4,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id','',['attr1','attr2'],\
                                                attr_data_list2,'ascii']]],
      'attribute_name_list':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2','attr3'],\
                                                  attr_data_list3,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1'],\
                                                 attr_data_list1,'ascii']],
        [['test.csv',True,'rec_id',1000,None,attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,[],attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['rec_id'],attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr2'],attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1',''],\
                                                attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr1'],\
                                                attr_data_list2,'ascii']]],
      'attribute_data_list':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1'],attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2','attr3'],\
                                                 attr_data_list3,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','gender','city','attr2'],\
                                                 attr_data_list4,'ascii']],
        [['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list1,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],[1,2,3],'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],'test','ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],{},'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],None,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],[],'ascii']]],
      'unicode_encoding':
       [[['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                   attr_data_list2,'ascii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                              attr_data_list2,'iso-8859-1'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                             attr_data_list2,'iso-2022-jp'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'ASCII']],
        [['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                   attr_data_list2,''],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                  attr_data_list2,'asccii'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                   attr_data_list2,'8859-1'],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                                   attr_data_list2,[]],
         ['test.csv',True,'rec_id',1000,['attr1','attr2'],\
                                               attr_data_list2,None]]]}],
}

# =============================================================================

class TestCase(unittest.TestCase):

  # Initialise test case  - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  def setUp(self):
    pass # Nothing to initialize

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

      print '1:', method_keyword_argument_list
      print '2:', test_data_details

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
              getattr(generator,test_method_name)(key_word_dict)
            except:
              passed = False
          else:
            try:
              getattr(generator,test_method_name)(**key_word_dict)
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
                getattr(generator,test_method_name),key_word_dict)
            except:
              passed = False
          else:
            try:
              self.assertRaises(Exception,
                getattr(generator,test_method_name),**key_word_dict)
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

  def testFunct_GenerateFreqAttribute(self):
    """Test that this method returns a correct string value for attribute.
    """

    print 'Testing functionality of "GenerateFreqAttribute"'

    num_passed = 0
    num_failed = 0

    # Load the lookup file and store the values in a dictionary
    #
    header_list,gname_file_data = basefunctions.read_csv_file(\
           '../lookup-files/givenname_f_freq.csv','ascii', False)

    header_list,postcode_file_data = basefunctions.read_csv_file(\
           '../lookup-files/postcode_act_freq.csv','ascii', False)

    gname_freq_val_list =    []
    postcode_freq_val_list = []

    for freq_pair_list in gname_file_data:
      attr_val = freq_pair_list[0].strip()
      if attr_val not in gname_freq_val_list:
        gname_freq_val_list.append(attr_val)

    for freq_pair_list in postcode_file_data:
      attr_val = freq_pair_list[0].strip()
      if attr_val not in postcode_freq_val_list:
        postcode_freq_val_list.append(attr_val)

    passed = True

    for t in range(num_tests):
      gname_attr_val = gname_attr.create_attribute_value()
      if gname_attr_val not in gname_freq_val_list:
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    for t in range(num_tests):
      postcode_attr_val = postcode_attr.create_attribute_value()
      if postcode_attr_val not in postcode_freq_val_list:
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == 2*num_tests

    test_result_str = 'generator,GenerateFreqAttribute,create_attribute_value,'\
                      + 'n/a,funct,%d,' % (2*num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_GenerateFuncAttribute(self):
    """Test that this method returns a correct string value for attribute.
    """

    print 'Testing functionality of "GenerateFuncAttribute"'

    num_passed = 0
    num_failed = 0

    passed = True

    for t in range(num_tests):
      age_attr_val = age_uniform_attr.create_attribute_value()
      if not isinstance(age_attr_val, str):
        passed = False
      try:
        int_val = int(age_attr_val)
        if not isinstance(int_val, int):
          passed = False
        elif int_val > 120:
          passed = False
        elif int_val < 0:
          passed = False
      except:
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'generator,GenerateFuncAttribute,create_attribute_value,'\
                      + 'n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_GenerateCateCateCompoundAttribute(self):
    """Test that this method returns two correct string values for the
       compound attribute of two categorical attributes.
    """

    print 'Testing functionality of "GenerateCateCateCompoundAttribute"'

    num_passed = 0
    num_failed = 0

    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
           '../lookup-files/gender-city.csv','ascii', True)

    cate_val_dict = {} # attr1 values are the keys and the values are
                       # the corresponding attr2 values.

    i = 0  # Line counter in file data

    while i < len(file_data):
      rec_list = file_data[i]
      cate_attr1_val =  rec_list[0].strip()

      # Process values for second categorical attribute in this line
      #
      cate_attr2_data = rec_list[2:]  # All values and counts of attribute 2
      cate_attr2_val_list = []  # Values in second categorical attribute for
                                # this categorical value from first attribute
      while (cate_attr2_data != []):
        if (len(cate_attr2_data) == 1):
          if (cate_attr2_data[0] != '\\'):
            raise Exception, 'Line in categorical look-up file has illegal' + \
                             'format.'
          # Get the next record from file data with a continuation of the
          # categorical values from the second attribute
          #
          i += 1
          cate_attr2_data = file_data[i]
        cate_attr2_val =   cate_attr2_data[0]
        cate_attr2_val_list.append(cate_attr2_val)
        cate_attr2_data = cate_attr2_data[2:]
      cate_val_dict[cate_attr1_val] = cate_attr2_val_list
      i += 1

    #print cate_val_dict

    passed = True

    for t in range(num_tests):
      gender_attr_val, city_attr_val = \
         gender_city_comp_attr.create_attribute_values()

      if gender_attr_val not in cate_val_dict:
        passed = False
      else:
        city_attr_vals = cate_val_dict[gender_attr_val]
        if city_attr_val not in city_attr_vals:
          passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'generator,GenerateCateCateCompoundAttribute,create_'\
                      + 'attribute_values,n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_GenerateCateContCompoundAttribute(self):
    """Test that this method returns two correct string values for the
       compound attribute of one categorical attribute and one continuous
       attribute.
    """

    print 'Testing functionality of "GenerateCateContCompoundAttribute"'

    num_passed = 0
    num_failed = 0

    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
           '../lookup-files/gender-income.csv','ascii', False)

    cate_cont_val_dict = {} # attr1 values are the keys and the values are
                            # the corresponding attr2 values.

    for val_pair_list in file_data:
      cate_attr_val = val_pair_list[0].strip()
      cont_attr_list = val_pair_list[2:]
      cate_cont_val_dict[cate_attr_val] = cont_attr_list

    #print cate_cont_val_dict

    passed = True

    for t in range(num_tests):
      gender_attr_val, income_attr_val = \
          gender_income_comp_attr.create_attribute_values()

      if gender_attr_val not in cate_cont_val_dict:
        passed = False
      else:
        income_attr_list = cate_cont_val_dict[gender_attr_val]
        function_name = income_attr_list[0]
        try:
          income_val = float(income_attr_val)
          if function_name == 'uniform':
            min_val_uniform = float(income_attr_list[1])
            max_val_uniform = float(income_attr_list[2])
            if (income_val > max_val_uniform) or (income_val < min_val_uniform):
              passed = False
          elif function_name == 'normal':
            if income_attr_list[3] != u'None':
              min_val_normal = float(income_attr_list[3])
              if (income_val < min_val_normal):
                passed = False 
            if income_attr_list[4] != u'None':
              max_val_normal = float(income_attr_list[4])
              if (income_val > max_val_normal):
                passed = False
        except:
          passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'generator,GenerateCateContCompoundAttribute,create_'\
                      + 'attribute_values,n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_GenerateCateCateContCompoundAttribute(self):
    """Test that this method returns three correct string values for the
       compound attribute of two categorical attributes and one continuous
       attribute.
    """

    print 'Testing functionality of "GenerateCateCateContCompoundAttribute"'

    num_passed = 0
    num_failed = 0


    # Load the lookup file and store the values in a dictionary
    #
    header_list,file_data = basefunctions.read_csv_file(\
           '../lookup-files/gender-city-income.csv', 'ascii', False)

    cate_cate_cont_dict = {} # attr1 values are the keys and the values are
                             # dictionaries with the corresponding attr2  
                             # values being the keys and the values are lists 
                             # that contain the corresponding attr3 values.

    list_counter = 0  # Counter in the list of file data

    num_file_rows = len(file_data)
    rec_list = file_data[list_counter]

    while list_counter < num_file_rows:  # Process one row after another
      cate_attr1_val =  rec_list[0].strip()

      # Loop to process values of the second categorical attribute and the
      # corresponding continuous functions
      #
      list_counter += 1
      rec_list = file_data[list_counter]  # Get values from next line

      this_cont_funct_dict = {} # Values of categorical attribute 2
      
      # As long as there are data from the second categorical attribute 
      #
      while (len(rec_list) > 2):
        cate_attr2_val =  rec_list[0].strip()
        
        cont_attr_funct = rec_list[2].strip()

        if (cont_attr_funct == 'uniform'):
          cont_attr_funct_min_val = float(rec_list[3])
          cont_attr_funct_max_val = float(rec_list[4])
          this_cont_funct_dict[cate_attr2_val] = [cont_attr_funct,
                                                  cont_attr_funct_min_val,
                                                  cont_attr_funct_max_val]
        elif (cont_attr_funct == 'normal'):
          cont_attr_funct_mu =    float(rec_list[3])
          cont_attr_funct_sigma = float(rec_list[4])
          try:
            cont_attr_funct_min_val = float(rec_list[5])
          except:
            cont_attr_funct_min_val = None
          try:
            cont_attr_funct_max_val = float(rec_list[6])
          except:
            cont_attr_funct_max_val = None
          this_cont_funct_dict[cate_attr2_val] = [cont_attr_funct,
                                             cont_attr_funct_mu,
                                             cont_attr_funct_sigma,
                                             cont_attr_funct_min_val,
                                             cont_attr_funct_max_val]
        list_counter += 1
        if (list_counter < num_file_rows):
          rec_list = file_data[list_counter]
        else:
          rec_list = []
      cate_cate_cont_dict[cate_attr1_val] = this_cont_funct_dict

    #print cate_cate_cont_dict

    passed = True

    for t in range(num_tests):
      gender_attr_val, city_attr_val, income_attr_val = \
                   gender_city_income_comp_attr.create_attribute_values()
      if gender_attr_val not in cate_cate_cont_dict:
        passed = False
      else:
        city_attr_vals = cate_cate_cont_dict[gender_attr_val]
        if city_attr_val not in city_attr_vals:
          passed = False
        else:
          income_attr_list = city_attr_vals[city_attr_val]
          function_name = income_attr_list[0]
          try:
            income_val = float(income_attr_val)
            if function_name == 'uniform':
              min_val_uniform = float(income_attr_list[1])
              max_val_uniform = float(income_attr_list[2])
              if (income_val > max_val_uniform) or \
                            (income_val < min_val_uniform):
                passed = False
            elif function_name == 'normal':
              if income_attr_list[3] != None:
                min_val_normal = float(income_attr_list[3])
                if (income_val < min_val_normal):
                  passed = False 
              if income_attr_list[4] != None:
                max_val_normal = float(income_attr_list[4])
                if (income_val > max_val_normal):
                  passed = False
          except:
            passed = False


      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'generator,GenerateCateCateContCompound' + \
                      'Attribute,create_attribute_values,n/a,funct,%d,' % \
                      (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_GenerateContContCompoundAttribute(self):
    """Test that this method returns two correct string values for the
       compound attribute of two continuous attributes.
    """

    print 'Testing functionality of "GenerateContContCompoundAttribute"'

    num_passed = 0
    num_failed = 0

    passed = True

    for t in range(num_tests):
      age_attr_val, bp_attr_val = \
          age_blood_pressure_comp_attr.create_attribute_values()
      try:
        age_val = int(age_attr_val)
        if not isinstance(age_val,int):
          passed = False
        elif (age_val < 10) or (age_val > 110):
            passed = False
      except:
        passed = False
      try:
        bp_val = float(bp_attr_val)
        if basefunctions.float_to_str(bp_val,'float3') != bp_attr_val:
          passed = False
      except:
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'generator,GenerateContContCompoundAttribute,create_' + \
                       'attribute_values,n/a,funct,%d,' % (num_tests)
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
out_file_name = './logs/generatorTest-%s.csv' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write('Test results generated by generatorTest.py'  + os.linesep)

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
test_case_ins = TestCase('testFunct_GenerateFreqAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateFreqAttribute()

test_case_ins = TestCase('testFunct_GenerateFuncAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateFuncAttribute()

test_case_ins = TestCase('testFunct_GenerateCateCateCompoundAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateCateCateCompoundAttribute()

test_case_ins = TestCase('testFunct_GenerateCateContCompoundAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateCateContCompoundAttribute()

test_case_ins = TestCase('testFunct_GenerateCateCateContCompoundAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateCateCateContCompoundAttribute()

test_case_ins = TestCase('testFunct_GenerateContContCompoundAttribute')
test_res_list += \
  test_case_ins.testFunct_GenerateContContCompoundAttribute()

# Write test output results into the log file
#
for line in test_res_list:
  out_file.write(line + os.linesep)

out_file.close()

print 'Test results are written to', out_file_name

for line in test_res_list:
  print line

# =============================================================================
