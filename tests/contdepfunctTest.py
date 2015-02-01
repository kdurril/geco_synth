# contdepfunctTest.py - Test module that provides testing functions for the
#                       module contdepfunct.py of the data generation system.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for contdepfunct.py.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then system modules)

import os
import random
import sys
import time
import unittest
sys.path.append('..')

import contdepfunct

random.seed(42)  # Set seed for random generator

# =============================================================================

# Define the number of tests to be done for the functionality tests
#
num_tests = 100000

# Define argument test cases here
#
test_argument_data_dict = {
  ('contdepfunct','n/a','blood_pressure_depending_on_age'): \
    {'age':[[[1],[2],[3],[77],[8],[9],[3.76],[99.9],[129.65],[42]],
            [[None],[''],['test'],[-65],[999],[-0.03],[130.01],
             [187.87],[{}],[[]]]]},
  ('contdepfunct','n/a','salary_depending_on_age'): \
    {'age':[[[1],[2],[3],[77],[8],[9],[3.76],[99.9],[129.65],[42]],
            [[None],[''],['test'],[-65],[999],[-0.03],[130.01],
             [187.87],[{}],[[]]]]}
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
              getattr(contdepfunct,test_method_name)()
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              getattr(contdepfunct,test_method_name)(test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              getattr(contdepfunct,test_method_name)(test_input[0],
                                                     test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              getattr(contdepfunct,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              getattr(contdepfunct,test_method_name)(test_input[0],
                                                     test_input[1],
                                                     test_input[2],
                                                     test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              getattr(contdepfunct,test_method_name)(test_input[0],
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
                getattr(contdepfunct,test_method_name))
            except:
              passed = False

          elif (len(test_input) == 1):  # Method has one input argument
            try:
              self.assertRaises(Exception,
                getattr(contdepfunct,test_method_name),test_input[0])
            except:
              passed = False

          elif (len(test_input) == 2):  # Method has two input arguments
            try:
              self.assertRaises(Exception,
                getattr(contdepfunct,test_method_name),test_input[0],
                                                       test_input[1])
            except:
              passed = False

          elif (len(test_input) == 3):  # Method has three input arguments
            try:
              self.assertRaises(Exception,
                getattr(contdepfunct,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2])
            except:
              passed = False

          elif (len(test_input) == 4):  # Method has four input arguments
            try:
              self.assertRaises(Exception,
                getattr(contdepfunct,test_method_name),test_input[0],
                                                       test_input[1],
                                                       test_input[2],
                                                       test_input[3])
            except:
              passed = False

          elif (len(test_input) == 5):  # Method has five input arguments
            try:
              self.assertRaises(Exception,
                getattr(contdepfunct,test_method_name),test_input[0],
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

  def testFunct_blood_pressure_depending_on_age(self, num_tests):
    """Test the functionality of 'blood_pressure_depending_on_age', making
       sure this function returns a positive floating point value.
    """

    print 'Testing functionality of "blood_pressure_depending_on_age"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      age = random.uniform(0.0, 120.0)

      try:
        assert (contdepfunct.blood_pressure_depending_on_age(age) >= 0.0)
        num_passed += 1
      except:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'contdepfunct,n/a,blood_pressure_depending_on_age,' + \
                      'n/a,funct,%d,' % (num_tests)
    if (num_failed == 0):
      test_result_str += 'all tests passed'
    else:
      test_result_str += '%d tests failed' % (num_failed)

    return [test_result_str,'']

  # ---------------------------------------------------------------------------

  def testFunct_salary_depending_on_age(self, num_tests):
    """Test the functionality of 'salary_depending_on_age', making sure
       this function returns a positive floating point value.
    """

    print 'Testing functionality of "salary_depending_on_age"'

    num_passed = 0
    num_failed = 0

    for i in range(num_tests):

      age = random.uniform(0.0, 120.0)

      try:
        assert (contdepfunct.salary_depending_on_age(age) >= 0.0)
        num_passed += 1
      except:
        num_failed += 1

    assert num_passed + num_failed == num_tests

    test_result_str = 'contdepfunct,n/a,salary_depending_on_age,' + \
                      'n/a,funct,%d,' % (num_tests)
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
out_file_name = './logs/contdepfunctTest-%s.csv' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write('Test results generated by contdepfunctTest.py'  + os.linesep)

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

test_case_ins = TestCase('testFunct_blood_pressure_depending_on_age')
test_res_list += \
  test_case_ins.testFunct_blood_pressure_depending_on_age(num_tests)

test_case_ins = TestCase('testFunct_salary_depending_on_age')
test_res_list += test_case_ins.testFunct_salary_depending_on_age(num_tests)

# Write test output results into the log file
#
for line in test_res_list:
  out_file.write(line + os.linesep)

out_file.close()

print 'Test results are written to', out_file_name

for line in test_res_list:
  print line

# =============================================================================
