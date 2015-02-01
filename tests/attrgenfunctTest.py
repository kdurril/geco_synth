# attrgenfunctTest.py - Test module that provides testing functions for the
#                       module attrgenfunct.py of the data generation system.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for attrgenfunct.py.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then system modules)

import os
import random
import sys
import time
import unittest
sys.path.append('..')

import attrgenfunct

random.seed(42)  # Set seed for random generator

# =============================================================================

# Define the number of tests to be done for the functionality tests
#
num_tests = 10000

# Define argument test cases here
#
test_argument_data_dict = {
  ('attrgenfunct','n/a','generate_uniform_value'): \
    {'min_val':[[[-10,10,'int'],[10,110,'float1'],[1110.0,11011.9,'float2'],
                 [-1110.0,-11.9,'float9'],[-51110,1247,'float7']],
                [['-10',10,'int'],[None,10,'float1'],[{},11011.9,'float2'],
                 ["-1110.0",-11.9,'float9'],['int',1247,'float7']]],
     'max_val':[[[-10,10,'int'],[10,110,'float1'],[1110.0,11011.9,'float2'],
                 [-1110.0,-11.9,'float9'],[-51110,1247,'float7']],
                [[-10,'10','int'],[10,None,'float1'],[1110.0,{},'float2'],
                 [-1110.0,"-11.9",'float9'],[-51110,'int','float7']]],
     'val_type':[[[-10,10,'int'],[10,110,'float1'],[1110.0,11011.9,'float2'],
                  [1.0,9.9,'float3'],[1.0,2.9,'float4'],[1.0,11.9,'float5'],
                  [1.0,9.9,'float6'],[1.0,2.9,'float7'],[1.0,11.9,'float8'],
                  [-1110.0,-11.9,'float9']],
                 [[-10,10,'int2'],[10,110,'float0'],[1110.0,11011.9,'float-'],
                  [1.0,9.9,'test'],[1.0,2.9,{}],[1.0,11.9,''],
                  [1.0,9.9,42],[1.0,2.9,-42.42],[1.0,11.9,[]]]]},
#
  ('attrgenfunct','n/a','generate_uniform_age'): \
    {'min_val':[[[0,120],[10,100],[25.0,76.9],[55,56],[55.0,57.9]],
                [[-1,120],[210,100],['25.0',76.9],[{},56],[-55.0,57.9]]],
     'max_val':[[[0,120],[10,100],[25.0,76.9],[55,56],[55.0,57.9]],
                [[0,140],[10,-100],[25.0,'76.9'],[55,{}],[55.0,-57.9]]]},
#
  ('attrgenfunct','n/a','generate_normal_value'): \
    {'mu':[[[1.0,1.0,-10,10,'int'],[-5, 25,-10,110,'float1'],
            [100.42,2000,-1110.0,11011.9,'float2'],
            [24.24,5.5,None,30.0,'float9'],[24.24,5.5,10.0,None,'float7']],
           [['1.0',1.0,-10,10,'int'],[-55, 25,-10,110,'float1'],
            [255, 25,-10,110,'float1'],[None,2000,-1110.0,11011.9,'float2'],
            [[],5.5,None,30.0,'float9'],[{},5.5,10.0,None,'float7']]],
     'sigma':[[[1.0,1.0,-10,10,'int'],[-5, 25,-10,110,'float1'],
               [100.42,2000,-1110.0,11011.9,'float2'],
               [24.24,5.5,None,30.0,'float9'],[24.24,5.5,10.0,None,'float7']],
              [[1.0,'1.0',-10,10,'int'],[-5,-25,-10,110,'float1'],
               [100.42,None,-1110.0,11011.9,'float2'],
               [24.24,{},None,30.0,'float9'],[24.24,[],10.0,None,'float7']]],
     'min_val':[[[1.0,1.0,-10,10,'int'],[-5, 25,-10,110,'float1'],
                 [100.42,2000,-1110.0,11011.9,'float2'],
                 [24.24,5.5,None,30.0,'float9'],[24.24,5.5,10.0,None,'float7']],
                [[1.0,1.0,'-10',10,'int'],[-5, 25,120,110,'float1'],
                 [100.42,2000,{},11011.9,'float2'],
                 [24.24,5.5,'None',30.0,'float9'],
                 [24.24,5.5,120.0,None,'float7']]],
     'max_val':[[[1.0,1.0,-10,10,'int'],[-5, 25,-10,110,'float1'],
                 [100.42,2000,-1110.0,11011.9,'float2'],
                 [24.24,5.5,None,30.0,'float9'],[24.24,5.5,10.0,None,'float7']],
                [[1.0,1.0,-10,'10','int'],[-5, 25,-10,-110,'float1'],
                 [100.42,2000,-1110.0,{},'float2'],
                 [24.24,5.5,None,-30.0,'float9'],[24.24,5.5,10.0,[],'float7']]],
     'val_type':[[[1.0,1.0,-10,10,'int'],[-5, 25,-10,110,'float1'],
                  [100.42,2000,-1110.0,11011.9,'float2'],
                  [24.24,5.5,None,30.0,'float9'],
                  [24.24,5.5,10.0,None,'float7']],
                 [[1.0,1.0,-10,10,'int2'],[-5, 25,-10,110,'float21'],
                  [100.42,2000,-1110.0,11011.9,None],
                  [24.24,5.5,None,30.0,42.42],
                  [24.24,5.5,10.0,None,{}]]]},
#
  ('attrgenfunct','n/a','generate_normal_age'): \
    {'mu':[[[51.0,1.0,0,110],[45,25,4,110],[50.42,50,5,77],
            [24.24,5.5,1,50.0],[24.24,5.5,10.0,99]],
           [['51.0',1.0,0,110],[-45,25,4,110],[223,25,4,110],[None,50,5,77],
            [30,20,40,110],[70,20,10,60],[{},5.5,1,50.0],['',5.5,10.0,99]]],
     'sigma':[[[51.0,1.0,0,110],[45,25,4,110],[50.42,50,5,77],
               [24.24,5.5,1,50.0],[24.24,5.5,10.0,99]],
              [[51.0,-1.0,0,110],[45,'25',4,110],[50.42,None,5,77],
               [24.24,{},1,50.0],[24.24,[],10.0,99]]],
     'min_val':[[[51.0,1.0,0,110],[45,25,4,110],[50.42,50,5,77],
                 [24.24,5.5,1,50.0],[24.24,5.5,10.0,99]],
                [[51.0,1.0,-10,110],[45,25,134,110],[50.42,50,'None',77],
                 [24.24,5.5,{},50.0],[24.24,5.5,[],99]]],
     'max_val':[[[51.0,1.0,0,110],[45,25,4,110],[50.42,50,5,77],
                 [24.24,5.5,1,50.0],[24.24,5.5,10.0,99]],
                [[51.0,1.0,0,'110'],[45,25,4,-110],[50.42,50,5,'None'],
                 [24.24,5.5,1,{}],[24.24,5.5,10.0,[]]]]},

# add tests for generate_normal_value, generate_normal_age
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
              getattr(attrgenfunct,test_method_name)()
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              getattr(attrgenfunct,test_method_name)(test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              getattr(attrgenfunct,test_method_name)(test_input[0],
                                                     test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              getattr(attrgenfunct,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              getattr(attrgenfunct,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2],
                                                     test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              getattr(attrgenfunct,test_method_name)(test_input[0],
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
                getattr(attrgenfunct,test_method_name))
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              self.assertRaises(Exception,
                getattr(attrgenfunct,test_method_name),test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              self.assertRaises(Exception,
                getattr(attrgenfunct,test_method_name),test_input[0],
                                                       test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              self.assertRaises(Exception,
                getattr(attrgenfunct,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              self.assertRaises(Exception,
                getattr(attrgenfunct,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2],
                                                       test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              self.assertRaises(Exception,
                getattr(attrgenfunct,test_method_name),test_input[0],
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

  def testFunct_generate_phone_number_australia(self, num_tests):
    """Test the functionality of 'generate_phone_number_australia', making
       sure this function returns strings of consisting only of digits, with
       the first digit being 0, and two whitespaces at specific positions.
    """

    print 'Testing functionality of "generate_phone_number_australia"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      oz_phone_num = attrgenfunct.generate_phone_number_australia()

      passed = True

      if (len(oz_phone_num) != 12):
        passed = False
      if (oz_phone_num[0] != '0'):
        passed = False
      if (oz_phone_num[2] != ' '):
        passed = False
      if (oz_phone_num[7] != ' '):
        passed = False
      oz_phone_num_no_space = oz_phone_num.replace(' ','')  # Remove spaces
      if (not oz_phone_num_no_space.isdigit()):
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'attrgenfunct,n/a,generate_phone_number_australia,' + \
                      'n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_generate_credit_card_number(self, num_tests):
    """Test the functionality of 'generate_credit_card_number', making sure
       this function returns strings of consisting only of four groups of
       digits, eac hwith 4 digits, and three whitespaces at specific positions.
    """

    print 'Testing functionality of "generate_credit_card_number"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      cc_num = attrgenfunct.generate_credit_card_number()

      passed = True

      if (len(cc_num) != 19):
        passed = False
      if (cc_num[4] != ' '):
        passed = False
      if (cc_num[9] != ' '):
        passed = False
      if (cc_num[14] != ' '):
        passed = False
      cc_num_no_space = cc_num.replace(' ','')  # Remove spaces
      if (not cc_num_no_space.isdigit()):
        passed = False

      if (passed == True):
        num_passed += 1
      else:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'attrgenfunct,n/a,generate_credit_card_number,' + \
                      'n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_generate_uniform_value(self, num_tests):
    """Test the functionality of 'generate_uniform_value', making sure
       this function returns a string according to the given value type in
       the range between the minimum and maximum value specified.
    """

    print 'Testing functionality of "generate_uniform_value"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      for val_type in ['int','float1','float2','float3','float4','float5', \
                       'float6','float7','float8','float9']:

        for min_val in [-100.0, -42, 0, 10, 100.0]:
          for max_val in [200.0, 242, 10000.01]:

            norm_val = attrgenfunct.generate_uniform_value(min_val, max_val, \
                                                           val_type)
            passed = True

            if (float(norm_val) < min_val):
              passed = False
            if (float(norm_val) > max_val):
              passed = False
            if (val_type == 'int') and ('.' in norm_val):
              passed = False
            if (val_type != 'int'):
              num_digit = int(val_type[-1])
              norm_val_list = norm_val.split('.')
              if (len(norm_val_list[1]) > num_digit):
                passed = False  # Only larger, because for example 100.0 will
                                # only return with 1 digit after comma

            if (passed == True):
              num_passed += 1
            else:
              num_failed += 1

    assert num_passed + num_failed == (15*10*num_tests)

    test_result_str = 'attrgenfunct,n/a,generate_uniform_value,' + \
                      'n/a,funct,%d,' % (15*10*num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_generate_uniform_age(self, num_tests):
    """Test the functionality of 'generate_uniform_age', making sure this
       function returns a string with an integer value between 0 and 130.
    """

    print 'Testing functionality of "generate_uniform_age"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      for (min_val, max_val) in [(0,10), (0,120), (0,45), (42,48), (40,120)]:

        age_val = attrgenfunct.generate_uniform_age(min_val, max_val)

        passed = True

        if (float(age_val) < min_val):
          passed = False
        if (float(age_val) > max_val):
          passed = False
        if ('.' in age_val):
          passed = False

        if (passed == True):
          num_passed += 1
        else:
          num_failed += 1

    assert num_passed + num_failed == num_tests*5

    test_result_str = 'attrgenfunct,n/a,generate_uniform_age,' + \
                      'n/a,funct,%d,' % (num_tests*5)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_generate_normal_value(self, num_tests):
    """Test the functionality of 'generate_normal_value', making sure this
       function returns a string according to the given value type in the
       range between the minimum and maximum value specified.
    """

    print 'Testing functionality of "generate_normal_value"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      for val_type in ['int','float1','float2','float3','float4','float5', \
                       'float6','float7','float8','float9']:

        for (mu, sigma, min_val, max_val) in \
          [(0,1,-10,10), (0,1,-1,1),(-100.5,123.45,-1010.7,-10.11),
           (12345.87,54875.1,-400532,96344),
           (0,1,None,10), (0,1,None,1),(-100.5,123.45,None,-10.11),
           (12345.87,54875.1,None,96344), 
           (0,1,-10,None), (0,1,-1,None),(-100.5,123.45,-1010.7,None),
           (12345.87,54875.1,-400532,None),
           (0,1,None,None), (0,1,None,None),(-100.5,123.45,None,None),
           (12345.87,54875.1,None,None)]:

          norm_val = attrgenfunct.generate_normal_value(mu, sigma, min_val, \
                                                        max_val, val_type)
          passed = True

          if (min_val != None) and (float(norm_val) < min_val):
            print '1:', norm_val, min_val
            passed = False
          if (max_val != None) and (float(norm_val) > max_val):
            print '2:', norm_val, max_val
            passed = False
          if (val_type == 'int') and ('.' in norm_val):
            print '3:', norm_val
            passed = False
          if (val_type != 'int'):
            num_digit = int(val_type[-1])
            norm_val_list = norm_val.split('.')

            if (len(norm_val_list[1]) > num_digit):
              print '4:', norm_val, val_type             
              passed = False  # Only larger, because for example 100.0 will
                              # only return with 1 digit after comma

          if (passed == True):
            num_passed += 1
          else:
            num_failed += 1

    assert num_passed + num_failed == (16*10*num_tests)

    test_result_str = 'attrgenfunct,n/a,generate_normal_value,' + \
                      'n/a,funct,%d,' % (16*10*num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_generate_normal_age(self, num_tests):
    """Test the functionality of 'generate_normal_age', making sure this
       function returns a string with an integer value between 0 and 130.
    """

    print 'Testing functionality of "generate_normal_age"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      for (mu, sigma, min_val, max_val) in \
         [(50,100,0,130), (25,20,5,55), (65,10,60,130), (85,20,0,95)]:

        age_val = attrgenfunct.generate_normal_age(mu, sigma, min_val, max_val)

        passed = True

        if (float(age_val) < min_val):
          passed = False
        if (float(age_val) > max_val):
          passed = False
        if ('.' in age_val):
          passed = False

        if (passed == True):
          num_passed += 1
        else:
          num_failed += 1

    assert num_passed + num_failed == num_tests*4

    test_result_str = 'attrgenfunct,n/a,generate_normal_age,' + \
                      'n/a,funct,%d,' % (num_tests*4)
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
out_file_name = './logs/attrgenfunctTest-%s.csv' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write('Test results generated by attrgenfunctTest.py'  + os.linesep)

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

test_case_ins = TestCase('testFunct_generate_phone_number_australia')
test_res_list += \
  test_case_ins.testFunct_generate_phone_number_australia(num_tests)

test_case_ins = TestCase('testFunct_generate_credit_card_number')
test_res_list += \
  test_case_ins.testFunct_generate_credit_card_number(num_tests)

test_case_ins = TestCase('testFunct_generate_uniform_value')
test_res_list += \
  test_case_ins.testFunct_generate_uniform_value(num_tests)

test_case_ins = TestCase('testFunct_generate_uniform_age')
test_res_list += \
  test_case_ins.testFunct_generate_uniform_age(num_tests)

test_case_ins = TestCase('testFunct_generate_normal_value')
test_res_list += \
  test_case_ins.testFunct_generate_normal_value(num_tests)

test_case_ins = TestCase('testFunct_generate_normal_age')
test_res_list += \
  test_case_ins.testFunct_generate_normal_age(num_tests)

# Write test output results into the log file
#
for line in test_res_list:
  out_file.write(line + os.linesep)

out_file.close()

print 'Test results are written to', out_file_name

for line in test_res_list:
  print line

# =============================================================================
