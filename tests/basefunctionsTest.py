# basefunctionsTest.py - Test module that provides testing functions for the
#                       module basefunctions.py of the data generation system.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for basefunctions.py.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then system modules)

import os
import random
import sys
import time
import filecmp
import unittest
sys.path.append('..')

import basefunctions

random.seed(42)  # Set seed for random generator

# =============================================================================

# Functions to be used as the testcases for testing the arguments of the
# check_is_function_or_method
#
def f1(x):		
  print x

def f2():
  print 'hello'

# Define argument test cases here
#
test_argument_data_dict = {
  ('basefunctions','n/a','check_is_not_none'): \
    {'variable':[[['testArgument','test'],['hello','test'],
                  ['1.0','test']],
                 [[None,'test'],['','test'],[123,'test'],
                  [0.234,'test'],[{},'test'],
                  [[],'test']]], 
     'value': [[['testArgument','hello'],['testArgument',123],
                ['testArgument',0.234],['testArgument',[]],
                ['testArgument',{}]],
               [['testArgument',None]]]},

  ('basefunctions','n/a','check_is_string'): \
    {'variable':[[['testArgument','hello'],['test','hello'],
                  ['1.0','hello']],
                 [[None,'hello'],['','hello'],[123,'hello'],
                  [0.234,'hello'],[{},'hello'],
                  [[],'hello']]], 
     'value': [[['testArgument','hello'],['testArgument',''],
                ['testArgument','123'],['testArgument','-1.23'],
                ['testArgument',"'!?!'"],['testArgument',"HELlo"],
                ['testArgument',"[..]"]],
               [['testArgument',None],['testArgument',123],
                ['testArgument',1.87],['testArgument',-75]]]},

  ('basefunctions','n/a','check_is_unicode_string'): \
    {'variable':[[['testArgument',u'hello'],['test',u'hello'],
                  ['1.0',u'hello']],
                 [[None,u'hello'],['',u'hello'],[123,u'hello'],
                  [0.234,u'hello'],[{},u'hello'],
                  [[],u'hello']]], 
     'value': [[['testArgument',u'hello'],['testArgument',u'text'],
                ['testArgument',u''],['testArgument',u'123']],
               [['testArgument',None],['testArgument',''],
                ['testArgument',-123],['testArgument',123],
                ['testArgument',1.87],['testArgument','ascii']]]},

  ('basefunctions','n/a','check_is_string_or_unicode_string'): \
    {'variable':[[['testArgument','hello'],['test',u'hello'],
                  ['1.0','hello2'],['1.0',u'hello']],
                 [[None,u'hello'],['','hello'],[123,u'hello'],
                  [0.234,'hello'],[{},u'hello'],
                  [[],u'hello']]], 
     'value': [[['testArgument',u'hello'],['testArgument','text'],
                ['testArgument',u''],['testArgument',u'123'],
                ['testArgument',''],['testArgument','123']],
               [['testArgument',None],['testArgument',123.45],
                ['testArgument',-123],['testArgument',-123.65],
                ['testArgument',{}],['testArgument',[]]]]},

  ('basefunctions','n/a','check_is_non_empty_string'): \
    {'variable':[[['testArgument','hello'],['test','hello'],
                  ['1.0','hello']],
                 [[None,'hello'],['','hello'],[123,'hello'],
                  [0.234,'hello'],[{},'hello'],
                  [[],'hello']]], 
     'value': [[['testArgument','hello'],['testArgument','123'],
                ['testArgument','-1.23'],['testArgument','HELlo'],
                ['testArgument',"'!?!'"],['testArgument',"[..]"]],
               [['testArgument',None],['testArgument',123],
                ['testArgument',1.87],['testArgument',-75],
                ['testArgument',''],['testArgument',[]],
                ['testArgument',{}]]]}, # , ['testArgument','hello']

  ('basefunctions','n/a','check_is_number'): \
    {'variable':[[['testArgument',123],['test',123],['1.0',123]],
                 [[None,123],['',123],[123,123],[0.234,123],
                  [{},123],[[],123]]], 
     'value': [[['testArgument',0],['testArgument',-0],
                ['testArgument',1.23],['testArgument',-24.41],
                ['testArgument',1289837],['testArgument',-973293]],
               [['testArgument',None],['testArgument','hello'],
                ['testArgument','123'],['testArgument','[]'],
                ['testArgument','-123.34'],['testArgument',''],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_positive'): \
    {'variable':[[['testArgument',1.0],['test',1.0],['1.0',1.0]],
                 [[None,1.0],['',1.0],[123,1.0],[0.234,1.0],
                  [{},1.0],[[],1.0]]], 
     'value': [[['testArgument',1.0],['testArgument',0.001],
                ['testArgument',0.0000001],['testArgument',1],
                ['testArgument',1.474],['testArgument',1236967],
                ['testArgument',17676.474]],
               [['testArgument',None],['testArgument',-1.23],
                ['testArgument',-123],['testArgument',-100000000],
                ['testArgument','hello'],['testArgument','123'],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_not_negative'): \
    {'variable':[[['testArgument',1.0],['test',1.0],['1.0',1.0]],
                 [[None,1.0],['',1.0],[123,1.0],[0.234,1.0],
                  [{},1.0],[[],1.0]]], 
     'value': [[['testArgument',0],['testArgument',-0],
                ['testArgument',1.0],['testArgument',0.00],
                ['testArgument',-0.000],['testArgument',1],
                ['testArgument',1.474],['testArgument',1236987],
                ['testArgument',17676.474]],
               [['testArgument',None],['testArgument',-1.23],
                ['testArgument',-123],['testArgument',-100000000],
                ['testArgument','hello'],['testArgument','123'],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_normalised'): \
    {'variable':[[['testArgument',1.0],['test',1.0],['1.0',1.0]],
                 [[None,1.0],['',1.0],[123,1.0],[0.234,1.0],
                  [{},1.0],[[],1.0]]], 
     'value': [[['testArgument',0],['testArgument',-0],
                ['testArgument',0.00],['testArgument',-0.0],
                ['testArgument',1],['testArgument',1.0],
                ['testArgument',0.0001],['testArgument',1.00000],
                ['testArgument',0.5],['testArgument',0.9999]],
               [['testArgument',None],['testArgument',-1.23],
                ['testArgument',-123],['testArgument',100],
                ['testArgument',1.0001],['testArgument',-1.0],
                ['testArgument','hello'],['testArgument','0.7'],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_percentage'): \
    {'variable':[[['testArgument',10.0],['test',10.0],['1.0',10.0]],
                 [[None,10.0],['',10.0],[123,10.0],[0.234,10.0],
                  [{},10.0],[[],10.0]]], 
     'value': [[['testArgument',0],['testArgument',-0],
                ['testArgument',0.00],['testArgument',-0.0],
                ['testArgument',1],['testArgument',1.0],
                ['testArgument',0.0001],['testArgument',99.000],
                ['testArgument',100],['testArgument',0.5],
                ['testArgument',50],['testArgument',50.001],
                ['testArgument',100.0],['testArgument',0.9999]],
               [['testArgument',None],['testArgument',-1.23],
                ['testArgument',-123],['testArgument',100.001],
                ['testArgument',-0.0001],['testArgument','hello'],
                ['testArgument','85'],['testArgument','45%'],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_integer'): \
    {'variable':[[['testArgument',10],['test',10],['1.0',10]],
                 [[None,10],['',10],[123,10],[0.234,10],
                  [{},10],[[],10]]], 
     'value': [[['testArgument',0],['testArgument',1],
                ['testArgument',10],['testArgument',1234],
                ['testArgument',-1],['testArgument',-96234],
                ['testArgument',-100],['testArgument',-0]],
               [['testArgument',None],['testArgument',-1.23],
                ['testArgument',1.23],['testArgument',-0.0001],
                ['testArgument',0.001],['testArgument','hello'],
                ['testArgument','85'],['testArgument',10000.0],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_float'): \
    {'variable':[[['testArgument',1.0],['test',1.0],['1.0',1.0]],
                 [[None,1.0],['',1.0],[123,1.0],[0.234,1.0],
                  [{},1.0],[[],1.0]]], 
     'value': [[['testArgument',0.0],['testArgument',-0.0],
                ['testArgument',0.123],['testArgument',-65.9203],
                ['testArgument',42.123],['testArgument',-10000.0]],
               [['testArgument',None],['testArgument',-123],
                ['testArgument',123],['testArgument',0],
                ['testArgument',100000],['testArgument','hello'],
                ['testArgument','8.5'],['testArgument',-0],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','check_is_dictionary'): \
    {'variable':[[['testArgument',{}],['test',{}],['1.0',{}]],
                 [[None,{}],['',{}],[123,{}],[0.234,{}],
                  [{},{}],[[],{}]]], 
     'value': [[['testArgument',{}],['testArgument',{1:2,6:0}],
                ['testArgument',{'a':4,'t':1,(1,4,6):'tr'}]],
               [['testArgument',None],['testArgument',"{1:2,3:4}"],
                ['testArgument',[]],['testArgument',set()]]]},

  ('basefunctions','n/a','check_is_list'): \
    {'variable':[[['testArgument',[]],['test',[]],['1.0',[]]],
                 [[None,[]],['',[]],[123,[]],[0.234,[]],
                  [{},[]],[[],[]]]], 
     'value': [[['testArgument',[]],['testArgument',[1,3,5]],
                ['testArgument',[-1,-3,-5]],
                ['testArgument',['a','56',1,{}]]],
               [['testArgument',None],['testArgument',"[1,2,3,4]"],
                ['testArgument',{}],['testArgument',set()]]]},

  ('basefunctions','n/a','check_is_set'): \
    {'variable':[[['testArgument',set()],['test',set()],['1.0',set()]],
                 [[None,set()],['',set()],[123,set()],[0.234,set()],
                  [{},set()],[[],set()]]], 
     'value': [[['testArgument',set()],['testArgument',set([1,2,3])],
                ['testArgument',set(['a','a'])],
                ['testArgument',set(['a','56',1,100.345])]],
               [['testArgument',None],['testArgument',"set([1,2,3])"],
                ['testArgument',[1,2,3,4]],['testArgument',{1:2,5:6}],
                ['testArgument',{}],['testArgument',[]]]]},

  ('basefunctions','n/a','check_is_tuple'): \
    {'variable':[[['testArgument',()],['test',()],['1.0',()]],
                 [[None,()],['',()],[123,()],[0.234,()],
                  [{},()],[[],()]]], 
     'value': [[['testArgument',()],['testArgument',('a','b')],
                ['testArgument',(42,'b')],['testArgument',(1,100)],
                ['testArgument',('a','b','c',1,2,3)]],
               [['testArgument',None],['testArgument',[1,2,3,4]],
                ['testArgument',{1:2,5:6}],['testArgument',set([1,2,3])],
                ['testArgument',"(1,2,3)"],['testArgument',[]],
                ['testArgument',{}],['testArgument',set()]]]},

  ('basefunctions','n/a','check_is_flag'): \
    {'variable':[[['testArgument',True],['test',True],['1.0',True]],
                 [[None,True],['',True],[123,True],[0.234,True],
                  [{},True],[[],True]]], 
     'value': [[['testArgument',True],['testArgument',False],
                ['testArgument',0],['testArgument',1],
                ['testArgument',0.0],['testArgument',1.0]],
               [['testArgument',None],['testArgument','True'],
                ['testArgument','False'],['testArgument',0.01],
                ['testArgument',1.01],['testArgument','1.0']]]},

  ('basefunctions','n/a','check_unicode_encoding_exists'): \
    {'unicode_encoding_string':[[["ascii"],["iso-8859-1"],["ASCII"]],
                 [[None],["asciii"],[123],['']]]},

  ('basefunctions','n/a','check_is_function_or_method'): \
    {'variable':[[['testArgument',f1],['test',f1],['1.0',f1]],
                 [[None,f1],['',f1],[123,f1],[0.234,f1],
                  [{},f1],[[],f1]]], 
     'value': [[['testArgument',f1],['testArgument',f2],
                ['testArgument',basefunctions.check_is_not_none],
                ['testArgument',basefunctions.check_is_function_or_method]],
               [['testArgument',None],['testArgument','f1'],
                ['testArgument','f2'],['testArgument',0.0],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','char_set_ascii'): \
    {'string_variable':[[["hello"],["1256783"],["hello1234test5678"],
                         ["hello 1234 test 5678"],[' 1 a 2 b ']],
                 [[None],[0.2345],[123],[[]],[{}],[-5434.6]]]},  

  ('basefunctions','n/a','check_is_valid_format_str'): \
    {'variable':[[['testArgument','int'],['test','int'],['1.0','int']],
                 [[None,'int'],['','int'],[123,'int'],[0.234,'int'],
                  [{},'int'],[[],'int']]], 			
     'value': [[['testArgument','int'],['testArgument','float1'],
                ['testArgument','float2'],['testArgument','float3'],
                ['testArgument','float4'],['testArgument','float5'],
                ['testArgument','float6'],['testArgument','float7'],
                ['testArgument','float8'],['testArgument','float9']],
               [['testArgument',None],['testArgument',''],
                ['testArgument','float10'],['testArgument','int1'],
                ['testArgument','floet1'],['testArgument',1],
                ['testArgument',[]],['testArgument',{}]]]},

  ('basefunctions','n/a','float_to_str'): \
    {'number_variable':[[[1234,'int'],[123.4,'int'],[1.0004,'int'],
                         [1000000000,'int'],[-12345.678,'int']],
                 [[None,'int'],['','int'],['123','int'],['456.98','int'],
                  [{},'int'],[[],'int']]], 			
     'format_string': [[[100,'int'],[100,'float1'],
                [100,'float2'],[100,'float3'],
                [100,'float4'],[100,'float5'],
                [100,'float6'],[100,'float7'],
                [100,'float8'],[100,'float9']],
               [[100,None],[100,''],
                [100,'float10'],[100,'int1'],
                [100,'floet1'],[100,1],
                [100,[]],[100,{}]]]},

  ('basefunctions','n/a','str2comma_separated_list'): \
    {'string_variable':[[[u"ab,cd,ef"],[u"12,567,83"],
                         [u"hello,1234,test,5678"],
                         [u"hello ,1234 ,test ,5678"],[u' 1 a, 2 b '],
                         [u'as$,bc#'],[u'abcdef'],[u' , ']],
                 [[None],[0.2345],[123],[''],[],{}]]},

  ('basefunctions','n/a','read_csv_file'): \
    {'file_name':[[['test1.csv',"ascii",False], # Assume these test files exist
                   ['test3.csv',"ascii",False],
                   ['test2.txt',"ascii",False]],                     
                  [[None,"ascii",False],['',"ascii",False], 
                   ['test3.csvv',"ascii",False],[234,"ascii",False],
                   [{},"ascii",False],[[],"ascii",False]]], 
     'encoding': [[['test1.csv',"ascii",False],
                   ['test1.csv',"iso-8859-1",False],
                   ['test1.csv',"ASCII",False],
                   ['test1.csv',None,False]],
                  [['test1.csv','',False],['test1.csv','asciii',False],
                   ['test1.csv','ascii encode',False],['test1.csv',123,False],
                   ['test1.csv',[],False],['test1.csv',{},False]]],
     'header_line': [[['test1.csv',"ascii",True],['test1.csv',"ascii",False],
                      ['test1.csv',"ascii",1.0],['test1.csv',"ascii",1],
                      ['test1.csv',"ascii",0],['test1.csv',"ascii",0.0]],
                     [['test1.csv',"ascii",None],['test1.csv',"ascii",'True'],
                      ['test1.csv',"ascii",'1.0'],['test1.csv',"ascii",1.01],
                      ['test1.csv',"ascii",0.01],['test1.csv',"ascii",'']]]},

  ('basefunctions','n/a','write_csv_file'): \
    {'file_name':[[['test.csv',"ascii",None,[]],['test.csv',"ascii",None,[]],
                   ['test.txt',"ascii",None,[]],
                   ['test.csv',"ascii",None,[]]],
                  [[None,"ascii",None,[]],['',"ascii",None,[]],
                   ['test-3/csvv',"ascii",None,[]],[234,"ascii",None,[]],
                   [{},"ascii",None,[]],[[],"ascii",None,[]]]], 
     'encoding': [[['test.csv',"ascii",None,[]],
                   ['test.csv',"iso-8859-1",None,[]],
                   ['test.csv',"ASCII",None,[]],
                   ['test.csv',None,None,[]]],
                 [['test.csv','',None,[]],['test.csv','asciii',None,[]],
                  ['test.csv','ascii encode',None,[]],['test.csv',123,None,[]],
                  ['test.csv',[],None,[]],['test.csv',{},None,[]]]],
     'header_list': [[['test.csv',"ascii",None,[]],
                      ['test.csv',"ascii",[],[]],
                      ['test.csv',"ascii",['attr1'],[]],
                      ['test.csv',"ascii",['attr1','attr2'],[]],
                      ['test.csv',"ascii",[' attr1 '],[]],
                      ['test.csv',"ascii",[''],[]]],
                     [['test.csv',"ascii",'',[]],
                      ['test.csv',"ascii",'attr1',[]],
                      ['test.csv',"ascii",'attr1,attr2',[]],
                      ['test.csv',"ascii",1,[]],
                      ['test.csv',"ascii",set(['attr1']),[]],
                      ['test.csv',"ascii",{1:'attr1'},[]]]],
     'file_data': [[['test.csv',"ascii",None,[]],
                    ['test.csv',"ascii",None,[['test']]],
                    ['test.csv',"ascii",None,[['1'],['2'],['3','4'],\
                                              ['5','6','7'],['8,9,10']]],
                    ['test.csv',"ascii",None,[['a','b'],['c','d','e']]],
                    ['test.csv',"ascii",None,[['a'],['1','2'],['b','$%'],
                                              ['','10.34']]],
                    ['test.csv',"ascii",None,[['']]]],
                   [['test.csv',"ascii",None,None],
                    ['test.csv',"ascii",None,'test'],
                    ['test.csv',"ascii",None,['test']],
                    ['test.csv',"ascii",None,[[1,2],[3,4]]],
                    ['test.csv',"ascii",None,{}],
                    ['test.csv',"ascii",None,set()],
                    ['test.csv',"ascii",None,'']]]}
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
       - Values are dictionaries where the keys are the names of the input
         argument that is being tested, and the values of these dictionaries
         are a list that contains two lists. The first list contains valid
         input arguments ('normal' argument tests) that should pass the test,
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
      test_method_name = test_method_names[2]
      print 'Testing arguments for method/function:', test_method_name

      for argument_name in test_method_data:
        print '  Testing input argument:', argument_name

        norm_test_data = test_method_data[argument_name][0]
        exce_test_data = test_method_data[argument_name][1]
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

          if (len(test_input) == 0):  # Method has no input argument
            try:
              getattr(basefunctions,test_method_name)()
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              getattr(basefunctions,test_method_name)(test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              getattr(basefunctions,test_method_name)(test_input[0],
                                                     test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              getattr(basefunctions,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              getattr(basefunctions,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2],
                                                     test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              getattr(basefunctions,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2],
                                                     test_input[3],
                                                     test_input[4])
            except:
              passed = False

          else:
            raise Exception, 'Illegal number of input arguments'

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

          if (len(test_input) == 0):  # Method has no input argument
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name))
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name),test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name),test_input[0],
                                                       test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2],
                                                       test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              self.assertRaises(Exception,
                getattr(basefunctions,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2],
                                                       test_input[3],
                                                       test_input[4])
            except:
              passed = False

          else:
            raise Exception, 'Illegal number of input arguments'

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

  def testFunct_char_set_ascii(self):
    """Test the functionality of 'char_set_ascii', making sure this function
       returns a correct string containing the set of corresponding characters.
    """

    print 'Testing functionality of "char_set_ascii"'

    num_passed = 0
    num_failed = 0
    num_tests = 0
    failed_tests_desc = ''

    test_cases = {
     '0123456789':['1','234','9746298136491', 
                   '99999999999999999999999999'],
     '0123456789 ':['1 2 3', ' 0 0 0 ', '   234'
                    '409324 12430 32578', '0000000 00000'],
     'abcdefghijklmnopqrstuvwxyz':['abc','aaaaaaaaaaaa','aaabbbccc',
                                   'cdhiofeakjbdakfhoweuar','ABC'],
     'abcdefghijklmnopqrstuvwxyz ':[' a b c ','aaaa aaaa  ','aaa bbb ccc',
                                    ' cdhiofeakjbdakfhoweuar','AB C'],
     'abcdefghijklmnopqrstuvwxyz0123456789':['1234sdfj12998', '12345678a',
                                             'afdadgf34kafh', '1a2b3c'],
     'abcdefghijklmnopqrstuvwxyz0123456789 ':['1234  sdfj 12998', ' 12345678a ',
                                              'afdadgf 34 kafh',
                                              ' 1 a 2 b 3 c ']}

    for char_set_type in test_cases:

      this_type_test_cases = test_cases[char_set_type]

      for test_case in this_type_test_cases:
        if basefunctions.char_set_ascii(test_case) == char_set_type:
          num_passed += 1
        else:
          num_failed += 1

          failed_tests_desc += "Failed with input string: '%s'; " % \
                               (test_case)
        num_tests += 1
        
    test_result_str = 'basefunctions,n/a,char_set_ascii,' + \
                      'n/a,funct,%d,' % (num_tests)

    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed,' % (num_failed)
      test_result_str += '"'+failed_tests_desc[:-2]+'"'

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_float_to_str(self):
    """Test the functionality of 'float_to_str', making sure this function
       returns a correct string of the number with the specified number of
       digits behind the comma.
    """

    print 'Testing functionality of "float_to_str"'

    num_passed = 0
    num_failed = 0
    num_tests =  0
    failed_tests_desc = ''

    test_cases = {
     'int':{1:'1',1.0:'1',123.0:'123',-123:'-123', 1000.0001:'1000', \
            56.7: '57'},
     'float1':{1:'1.0',1.0:'1.0',-123:'-123.0',1000.127:'1000.1',\
               56.78:'56.8'},
     'float2':{1:'1.00',1.0:'1.00',-123:'-123.00',1000.127:'1000.13',\
               56.78:'56.78'},
     'float3':{1:'1.000',-123:'-123.000',999.999:'999.999',\
               999.99999:'1000.000'},
     'float4':{1:'1.0000',-1.0:'-1.0000',4.56789:'4.5679', \
               999.99999:'1000.0000'},
     'float5':{1:'1.00000',-1.0:'-1.00000',4.456789:'4.45679', \
               999.999999:'1000.00000'},
     'float6':{1:'1.000000', -123:'-123.000000', 4.3456789:'4.345679', \
               123.12:'123.120000',999.9999999:'1000.000000'},
     'float7':{1:'1.0000000', -23.4:'-23.4000000', 4.23456789:'4.2345679',\
               123.12:'123.1200000',999.99999999:'1000.0000000'},
     'float8':{1:'1.00000000',-1.0:'-1.00000000',4.123456789: '4.12345679',\
               123.12: '123.12000000',999.999999999:'1000.00000000'},
     'float9':{1:'1.000000000',-1.0:'-1.000000000', \
               4.0123456789: '4.012345679',\
               999.9999999999:'1000.000000000'}}
                         
    for format in test_cases:

      this_format_test_cases = test_cases[format]

      for input_num in this_format_test_cases:
        if basefunctions.float_to_str(input_num,format) == \
                            this_format_test_cases[input_num]:
          num_passed += 1
        else:
          num_failed += 1
          failed_tests_desc += "Failed with input number: '%s'; " % \
                                (str(input_num))
        num_tests += 1


    test_result_str = 'basefunctions,n/a,float_to_str,' + \
                      'n/a,funct,%d,' % (num_tests)

    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed,' % (num_failed)
      test_result_str += '"'+failed_tests_desc[:-2]+'"'

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_str2comma_separated_list(self):
    """Test the functionality of 'str2comma_separated_list', making sure this
       function returns a correct list of values separated by the comma in the
       input string.
    """

    print 'Testing functionality of "str2comma_separated_list"'

    num_passed = 0
    num_failed = 0
    num_tests =  0

    failed_tests_desc = ''

    test_cases = {u'123,456,789':['123','456','789'],
                  u'abcd,efgh,ij':['abcd','efgh','ij'],
                  u"abcd,efgh,ij":['abcd','efgh','ij'],
                  u'123,abc,f23':['123','abc','f23'],
                  u'000,000,000':['000','000','000'],
                  u'#$%,^&*,@?>':['#$%','^&*','@?>'],
                  u'abcd,123 ':['abcd','123'],
                  u'123,45;6,7;89':['123','45;6','7;89'],
                  u'fd,g r,er,a w':['fd','g r','er','a w'],
                  u' fd,gr,er,aw ':['fd','gr','er','aw'],
                  u'123,456,':['123','456','']}

    for string_val in test_cases:

      if basefunctions.str2comma_separated_list(string_val) == \
         test_cases[string_val]:
        num_passed += 1
      else:
        num_failed += 1
        failed_tests_desc += "Failed when string input: '%s'; " % \
                              (str(string_val))
      num_tests += 1

    test_result_str = 'basefunctions,n/a,str2comma_separated_list,' + \
                      'n/a,funct,%d,' % (num_tests)

    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed,' % (num_failed)
      test_result_str += '"'+failed_tests_desc[:-2]+'"'

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_read_csv_file(self):
    """Test the functionality of 'read_csv_file', making sure this function
       reads a CSV file and returns the correct content of the file.

       This function assumes there are three small test file available:
       test1.csv, test2.txt, test3.csv

    """

    print 'Testing functionality of "read_csv_file"'

    num_passed = 0
    num_failed = 0
    num_tests =  0
    failed_tests_desc = ''

    # For the three test files, give file name, the expected number of records
    # (assuming there is no header line) and the expected number of attributes
    # in each record
    #
    test_cases = [('test1.csv',4,3),('test2.txt',5,4), ('test3.csv',0,1)]

    for test_case in test_cases:

      for header_flag in [True,False]:
        passed = True
        (header_list,file_data) = basefunctions.read_csv_file(test_case[0],
                                                              'ascii',
                                                              header_flag)
        if (header_flag == True):
          if (len(file_data) > 0):
            if (len(file_data) != test_case[1]-1):
              passed = False
          else:  # No records in file
            if (len(file_data) != 0):
              passed = False
          if (len(header_list) != test_case[2]):
            passed = False
        else:
          if (header_list != None):
            passed = False
          if (len(file_data) != test_case[1]):
            passed = False

        for rec in file_data:
          if len(rec) != test_case[2]:
            passed = False

        if (passed == True):
          num_passed += 1
        else:
          num_failed += 1
          failed_tests_desc += "Failed reading the file: '%s'; " % \
                                (test_case[0])
      num_tests += 1

    test_result_str = 'basefunctions,n/a,read_csv_file,' + \
                      'n/a,funct,%d,' % (num_tests)

    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed,' % (num_failed)
      test_result_str += '"'+failed_tests_desc[:-2]+'"'

    return [test_result_str,'']   

  # ---------------------------------------------------------------------------

  def testFunct_write_csv_file(self):
    """Test the functionality of 'write_csv_file', making sure this function
       correctly writes a list of values into a CSV file. To test this
       function we assume the read_csv_file() function is correct.
    """

    print 'Testing functionality of "write_csv_file"'

    num_passed = 0
    num_failed = 0
    num_tests =  0
    failed_tests_desc = ''

    test_cases = [[['test1'],['test2'],['test3']],
                  [['1'],['2'],['3']],
                  [['test 1'],['test 2'],['test 3']],
                  [['%^&'],['test $#%^'],['123 @#*(']],
                  [['1','2','3'],['4','5','6'],['7','8','9']],
                  [['1','2','3'],['4','5','6']],
                  [['1','2','3'],['4','5','6'],['7','8']],
                  [['id1','peter','lyneham'],['id2','miller','dickson'],\
                   ['id3','smith','hackett']]]

    header_lists = [None, ['attr1','attr2','attr3']]

    for test_case in test_cases:

      for header_list in header_lists:
        basefunctions.write_csv_file('test.csv','ascii',header_list,test_case)

        if (header_list != None):
          (read_header_list,read_file_data) = \
                          basefunctions.read_csv_file('test.csv','ascii',True)


        else:
          (read_header_list,read_file_data) = \
                          basefunctions.read_csv_file('test.csv','ascii',False)

      if (read_header_list == header_list) and (read_file_data == test_case):
        num_passed += 1
      else:
        num_failed += 1
        failed_tests_desc += "Failed writing the data: '%s'; " % \
                             (str(test_case))
      num_tests += 1

    test_result_str = 'basefunctions,n/a,write_csv_file,' + \
                      'n/a,funct,%d,' % (num_tests)

    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed,' % (num_failed)
      test_result_str += '"'+failed_tests_desc[:-2]+'"'

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
out_file_name = './logs/basefunctionsTest-%s.csv' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write("Test results generated by basefunctionsTest.py"  + os.linesep)

out_file.write("Test started: " + curr_time_str + os.linesep)

out_file.write(os.linesep)

out_file.write('Module name,Class name,Method name,Arguments,Test_type,' + \
               'Patterns tested,Summary,Failure description' + os.linesep)

out_file.write(os.linesep)

# Create instances for the testcase class that calls all tests
#
test_res_list = []
test_case_ins = TestCase('testArguments')
test_res_list += test_case_ins.testArguments(test_argument_data_dict)

test_case_ins = TestCase('testFunct_char_set_ascii')
test_res_list += \
  test_case_ins.testFunct_char_set_ascii()

test_case_ins = TestCase('testFunct_float_to_str')
test_res_list += \
  test_case_ins.testFunct_float_to_str()

test_case_ins = TestCase('testFunct_str2comma_separated_list')
test_res_list += \
  test_case_ins.testFunct_str2comma_separated_list()

test_case_ins = TestCase('testFunct_read_csv_file')
test_res_list += \
  test_case_ins.testFunct_read_csv_file()

test_case_ins = TestCase('testFunct_write_csv_file')
test_res_list += \
  test_case_ins.testFunct_write_csv_file()

# Write test output results into the log file
#
for line in test_res_list:
  out_file.write(line + os.linesep)

out_file.close()

print 'Test results are written to', out_file_name

for line in test_res_list:
  print line

# =============================================================================
