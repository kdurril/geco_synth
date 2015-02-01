# mainTest.py - Test module that provides stress testing for the overall
#               flexible data generation system by generating with a large
#               variety of parameter settings and checking the generated data
#               is within the paramter settings.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Test module for the overall flexible data generator system.
"""

do_large_tests = False  # Set to True to run tests to generate large
                        # datasets - warning is time consuming
import os
import sys
import time
import unittest
sys.path.append('..')

# Import data generator modules required
#
import attrgenfunct
import contdepfunct
import basefunctions
import generator
import corruptor

import random

random.seed(42)  # Set seed for random generator

# =============================================================================

# Define test cases, each being a list containing the main parameters required
# for generating a data set:
# 1) rec_id_attr_name
# 2) num_org_rec
# 3) num_dup_rec
# 4) max_duplicate_per_record
# 5) num_duplicates_distribution ('uniform', 'poisson', 'zipf')
# 6) max_modification_per_attr
# 7) num_modification_per_record
#
test_cases = [['rec_id',    100,    100, 1, 'uniform', 1, 1],
              ['rec_id',    100,    100, 1, 'poisson', 1, 1],
              ['rec_id',    100,    100, 1, 'zipf',    1, 1],
              ['rec_id',  10000,  10000, 1, 'uniform', 1, 1],
              ['rec_id',  10000,  10000, 1, 'poisson', 1, 1],
              ['rec_id',  10000,  10000, 1, 'zipf',    1, 1]]
if (do_large_tests == True):
  test_cases += [['rec_id', 100000, 100000, 1, 'uniform', 1, 1],
                 ['rec_id', 100000, 100000, 1, 'poisson', 1, 1],
                 ['rec_id', 100000, 100000, 1, 'zipf',    1, 1]]
#
test_cases += [['rec_id',    100,    20, 1, 'uniform', 1, 1],
               ['rec_id',    100,    20, 1, 'poisson', 1, 1],
               ['rec_id',    100,    20, 1, 'zipf',    1, 1],
               ['rec_id',  10000,  2000, 1, 'uniform', 1, 1],
               ['rec_id',  10000,  2000, 1, 'poisson', 1, 1],
               ['rec_id',  10000,  2000, 1, 'zipf',    1, 1]]
if (do_large_tests == True):
  test_cases += [['rec_id', 100000, 20000, 1, 'uniform', 1, 1],
                 ['rec_id', 100000, 20000, 1, 'poisson', 1, 1],
                 ['rec_id', 100000, 20000, 1, 'zipf',    1, 1]]
#
test_cases += [['rec_num',    123,    321, 5, 'uniform', 1, 3],
               ['rec_num',    123,    321, 5, 'poisson', 1, 3],
               ['rec_num',    123,    321, 5, 'zipf',    1, 3],
               ['rec_num',  12345,  14321, 5, 'uniform', 1, 3],
               ['rec_num',  12345,  14321, 5, 'poisson', 1, 3],
               ['rec_num',  12345,  14321, 5, 'zipf',    1, 3]]
if (do_large_tests == True):
  test_cases += [['rec_num', 123456, 154321, 5, 'uniform', 1, 3],
                 ['rec_num', 123456, 154321, 5, 'poisson', 1, 3],
                 ['rec_num', 123456, 154321, 5, 'zipf',    1, 3]]
#
test_cases += [['rec_num',    123,    321, 3, 'uniform', 3, 9],
               ['rec_num',    123,    321, 3, 'poisson', 3, 9],
               ['rec_num',    123,    321, 3, 'zipf',    3, 9],
               ['rec_num',  12345,  14321, 3, 'uniform', 3, 9],
               ['rec_num',  12345,  14321, 3, 'poisson', 3, 9],
               ['rec_num',  12345,  14321, 3, 'zipf',    3, 9]]
if (do_large_tests == True):
  test_cases += [['rec_num', 123456, 154321, 3, 'uniform', 3, 9],
                 ['rec_num', 123456, 154321, 3, 'poisson', 3, 9],
                 ['rec_num', 123456, 154321, 3, 'zipf',    3, 9]]
#
test_cases += [['rec_num',    321,    123, 11, 'uniform', 2, 7],
               ['rec_num',    321,    123, 11, 'poisson', 2, 7],
               ['rec_num',    321,    123, 11, 'zipf',    2, 7],
               ['rec_num',  43210,  14321, 11, 'uniform', 2, 7],
               ['rec_num',  43210,  14321, 11, 'poisson', 2, 7],
               ['rec_num',  43210,  14321, 11, 'zipf',    2, 7]]
if (do_large_tests == True):
  test_cases += [['rec_num', 654321, 123456, 11, 'uniform', 2, 7],
                 ['rec_num', 654321, 123456, 11, 'poisson', 2, 7],
                 ['rec_num', 654321, 123456, 11, 'zipf',    2, 7]]

# Set the Unicode encoding for all test data generation
#
unicode_encoding_used = 'ascii'

# Check the unicode encoding selected is valid
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

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

  def testDataGeneration(self, test_case):
    """Test the overall generation of a data set according to the parameters
       given by checking if the generated data sets follows the parameter
       specification given.
    """

    rec_id_attr_name =            test_case[0]
    num_org_rec =                 test_case[1]
    num_dup_rec =                 test_case[2]
    max_duplicate_per_record =    test_case[3]
    num_duplicates_distribution = test_case[4]
    max_modification_per_attr =   test_case[5]
    num_modification_per_record = test_case[6]

    test_res_list = ['', 'Test case parameters:']
    test_res_list.append('  rec_id_attr_name = %s' % (rec_id_attr_name))
    test_res_list.append('  num_org_rec = %s' % (num_org_rec))
    test_res_list.append('  num_dup_rec = %s' % (num_dup_rec))
    test_res_list.append('  max_duplicate_per_record = %s' % \
                         (max_duplicate_per_record))
    test_res_list.append('  num_duplicates_distribution = %s' % \
                         (num_duplicates_distribution))
    test_res_list.append('  max_modification_per_attr = %s' % \
                         (max_modification_per_attr))
    test_res_list.append('  num_modification_per_record = %s' % \
                         (num_modification_per_record))
    test_res_list.append('')

    # Define the attributes to be generated (based on methods from - - - - -
    # the generator.py module)

    # Individual attributes
    #
    given_name_attr = \
      generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = '../lookup-files/givenname_freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

    surnname_attr = \
      generator.GenerateFreqAttribute(attribute_name = 'surname',
                    freq_file_name = '../lookup-files/surname-freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

    postcode_attr = \
      generator.GenerateFreqAttribute(attribute_name = 'postcode',
                    freq_file_name = '../lookup-files/postcode_act_freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

    oz_phone_num_attr = \
      generator.GenerateFuncAttribute(attribute_name = 'oz-phone-number',
                   function = attrgenfunct.generate_phone_number_australia)

    credit_card_attr =  \
     generator.GenerateFuncAttribute(attribute_name = 'credit-card-number',
                   function = attrgenfunct.generate_credit_card_number)

    age_uniform_attr = \
      generator.GenerateFuncAttribute(attribute_name = 'age-uniform',
                   function = attrgenfunct.generate_uniform_age,
                   parameters = [0,120])

    age_death_normal_attr = \
      generator.GenerateFuncAttribute(attribute_name = 'age-death-normal',
                   function = attrgenfunct.generate_normal_age,
                   parameters = [80,20,0,120])

    income_normal_attr = \
      generator.GenerateFuncAttribute(attribute_name = 'income-normal',
                   function = attrgenfunct.generate_normal_value,
                   parameters = [75000, 20000, 0, 1000000, 'float2'])

    rating_normal_attr = \
      generator.GenerateFuncAttribute(attribute_name = 'rating-normal',
                   function = attrgenfunct.generate_normal_value,
                   parameters = [2.5, 1.0, 0.0, 5.0, 'int'])

    # Compund (dependent) attributes
    #
    gender_city_comp_attr = \
      generator.GenerateCateCateCompoundAttribute(\
                   categorical1_attribute_name = 'gender',
                   categorical2_attribute_name = 'city',
                   lookup_file_name = '../lookup-files/gender-city.csv',
                   has_header_line = True,
                   unicode_encoding = unicode_encoding_used)

    gender_income_comp_attr = \
      generator.GenerateCateContCompoundAttribute(\
                   categorical_attribute_name = 'alt-gender',
                   continuous_attribute_name = 'income',
                   continuous_value_type = 'float1',
                   lookup_file_name = '../lookup-files/gender-income.csv',
                   has_header_line = False,
                   unicode_encoding = unicode_encoding_used)

    gender_city_salary_comp_attr = \
      generator.GenerateCateCateContCompoundAttribute(\
                   categorical1_attribute_name = 'alt-gender-2',
                   categorical2_attribute_name = 'town',
                   continuous_attribute_name = 'salary',
                   continuous_value_type = 'float4',
                   lookup_file_name = \
                     '../lookup-files/gender-city-income.csv',
                   has_header_line = False,
                   unicode_encoding = unicode_encoding_used)

    age_blood_pressure_comp_attr = \
      generator.GenerateContContCompoundAttribute(\
                   continuous1_attribute_name = 'medical-age',
                   continuous2_attribute_name = 'blood-pressure',
                   continuous1_funct_name =     'uniform',
                   continuous1_funct_param =    [10,110],
                   continuous2_function = \
                     contdepfunct.blood_pressure_depending_on_age,
                   continuous1_value_type = 'int',
                   continuous2_value_type = 'float3')

    age_salary_comp_attr = \
      generator.GenerateContContCompoundAttribute(\
                   continuous1_attribute_name = 'medical-age-2',
                   continuous2_attribute_name = 'medical-salary',
                   continuous1_funct_name =     'normal',
                   continuous1_funct_param =    [45,20,25,130],
                   continuous2_function = \
                     contdepfunct.salary_depending_on_age,
                   continuous1_value_type = 'int',
                   continuous2_value_type = 'float1')

    # Define how attribute values are to be modified (corrupted) - - - - - -
    # (based on methods from the corruptor.py module)
    #
    average_edit_corruptor = \
      corruptor.CorruptValueEdit(\
                   position_function = corruptor.position_mod_normal,
                   char_set_funct = basefunctions.char_set_ascii,
                   insert_prob = 0.25,
                   delete_prob = 0.25,
                   substitute_prob = 0.25,
                   transpose_prob = 0.25)

    sub_tra_edit_corruptor = \
      corruptor.CorruptValueEdit(\
                   position_function = corruptor.position_mod_uniform,
                   char_set_funct = basefunctions.char_set_ascii,
                   insert_prob = 0.0,
                   delete_prob = 0.0,
                   substitute_prob = 0.5,
                   transpose_prob = 0.5)

    ins_del_edit_corruptor = \
      corruptor.CorruptValueEdit(\
                   position_function = corruptor.position_mod_normal,
                   char_set_funct = basefunctions.char_set_ascii,
                   insert_prob = 0.5,
                   delete_prob = 0.5,
                   substitute_prob = 0.0,
                   transpose_prob = 0.0)

    surname_misspell_corruptor = \
      corruptor.CorruptCategoricalValue(\
                   lookup_file_name = '../lookup-files/surname-misspell.csv',
                   has_header_line = False,
                   unicode_encoding = unicode_encoding_used)

    ocr_corruptor = corruptor.CorruptValueOCR(\
                   position_function = corruptor.position_mod_uniform,
                   lookup_file_name = '../lookup-files/ocr-variations.csv',
                   has_header_line = False,
                   unicode_encoding = unicode_encoding_used)

    keyboard_corruptor = corruptor.CorruptValueKeyboard(\
                   position_function = corruptor.position_mod_normal,
                   row_prob = 0.5,
                   col_prob = 0.5)

    phonetic_corruptor = corruptor.CorruptValuePhonetic(\
                   position_function = corruptor.position_mod_uniform,
                   lookup_file_name = \
                     '../lookup-files/phonetic-variations.csv',
                   has_header_line = False,
                   unicode_encoding = unicode_encoding_used)

    missing_val_empty_corruptor = corruptor.CorruptMissingValue()
    missing_val_miss_corruptor = corruptor.CorruptMissingValue(\
      missing_value='miss')
    missing_val_unkown_corruptor = corruptor.CorruptMissingValue(\
      missing_value='unknown')

    # Define the attributes to be generated for this data set, and the data
    # set itself
    #
    attr_name_list = ['given-name', 'surname', 'city', 'postcode',
                      'oz-phone-number', 'credit-card-number', 'age-uniform',
                      'age-death-normal', 'income-normal', 'rating-normal',
                      'gender', 'alt-gender', 'alt-gender-2', 'town',
                      'income', 'salary', 'medical-age', 'blood-pressure',
                      'medical-age-2', 'medical-salary']

    attr_data_list = [given_name_attr, surnname_attr, postcode_attr,
                      oz_phone_num_attr, credit_card_attr, age_uniform_attr,
                      age_death_normal_attr, income_normal_attr,
                      rating_normal_attr, gender_city_comp_attr,
                      gender_income_comp_attr, gender_city_salary_comp_attr,
                      age_blood_pressure_comp_attr, age_salary_comp_attr]

    # Initialise the main data generator
    #
    test_data_generator = generator.GenerateDataSet(\
                            output_file_name = 'no-file-name',
                            write_header_line = True,
                            rec_id_attr_name = rec_id_attr_name,
                            number_of_records = num_org_rec,
                            attribute_name_list = attr_name_list,
                            attribute_data_list = attr_data_list,
                            unicode_encoding = unicode_encoding_used)

    # Define distribution of how likely an attribute will be selected for
    # modification (sum of probabilities must be 1.0)
    #
    attr_mod_prob_dictionary = {'given-name':0.1, 'surname':0.1,
                                'city':0.1, 'postcode':0.1,
                                'oz-phone-number':0.1,
                                'age-death-normal':0.1,
                                'income-normal':0.1,'gender':0.1, 'town':0.1,
                                'income':0.1}

    # For each attribute, a distribution of which corruptors to apply needs
    # to be given, with the sum ofprobabilities to be 1.0 for each attribute
    #
    attr_mod_data_dictionary = \
      {'given-name':[(0.25, average_edit_corruptor),
                     (0.25, ocr_corruptor),
                     (0.25, phonetic_corruptor),
                     (0.25, missing_val_miss_corruptor)],
       'surname':[(0.5, surname_misspell_corruptor),
                  (0.5, average_edit_corruptor)],
       'city':[(0.5, keyboard_corruptor),
               (0.5, missing_val_empty_corruptor)],
       'postcode':[(0.3, missing_val_unkown_corruptor),
                   (0.7, sub_tra_edit_corruptor)],
       'oz-phone-number':[(0.2, missing_val_empty_corruptor),
                          (0.4, sub_tra_edit_corruptor),
                          (0.4, keyboard_corruptor)],
       'age-death-normal':[(1.0, missing_val_unkown_corruptor)],
       'income-normal':[(0.3, keyboard_corruptor),
                        (0.3, ocr_corruptor),
                        (0.4, missing_val_empty_corruptor)],
       'gender':[(0.5, sub_tra_edit_corruptor),
                 (0.5, ocr_corruptor)],
       'town':[(0.2, average_edit_corruptor),
               (0.3, ocr_corruptor),
               (0.2, keyboard_corruptor),
               (0.3, phonetic_corruptor)],
       'income':[(1.0, missing_val_miss_corruptor)]}

    # Initialise the main data corruptor
    #
    test_data_corruptor = corruptor.CorruptDataSet(\
                            number_of_org_records = num_org_rec,
                            number_of_mod_records = num_dup_rec,
                            attribute_name_list = attr_name_list,
                            max_num_dup_per_rec = max_duplicate_per_record,
                            num_dup_dist = num_duplicates_distribution,
                            max_num_mod_per_attr = max_modification_per_attr,
                            num_mod_per_rec = num_modification_per_record,
                            attr_mod_prob_dict = attr_mod_prob_dictionary,
                            attr_mod_data_dict = attr_mod_data_dictionary)

    passed = True  # Assume the test will pass :-)

    # Start the generation process
    #
    try:
      rec_dict = test_data_generator.generate()

    except Exception as exce_value:  # Something bad happened
      test_res_list.append('  generator.generate() raised Exception: "%s"' % \
                           (str(exce_value)))
      return test_res_list  # Abandon test

    num_org_rec_gen = len(rec_dict)

    if (num_org_rec_gen != num_org_rec):
      passed = False
      test_res_list.append('  Wrong number of original records generated:' + \
                           ' %d, expected %d' % (num_org_rec_gen,num_org_rec))

    # Corrupt (modify) the original records into duplicate records
    #
    try:
      rec_dict = test_data_corruptor.corrupt_records(rec_dict)
    except Exception as exce_value:  # Something bad happened
      test_res_list.append('  corruptor.corrupt_records() raised ' + \
                           'Exception: "%s"' % (str(exce_value)))
      return test_res_list  # Abandon test

    num_dup_rec_gen = len(rec_dict)-num_org_rec_gen

    if (num_dup_rec_gen != num_dup_rec):
      passed = False
      test_res_list.append('  Wrong number of duplicate records generated:' + \
                           ' %d, expected %d' % (num_dup_rec_gen,num_dup_rec))

    num_dup_counts = {}  # Count how many records have a certain number of
                         # duplicates

    # Do tests on all generated records
    #
    for (rec_id,rec_list) in rec_dict.iteritems():
      if (len(rec_list) != len(attr_name_list)):
        passed = False
        test_res_list.append('  Record with identifier "%s" contains wrong' % \
                             (rec_id) + ' number of attributes: ' + \
                             ' %d, expected %d' % (len(rec_list),
                             len(attr_name_list)))

      if ('org' in rec_id):  # An original record

        # Check the number of duplicates for this record is what is expected
        #
        num_dups = 0
        rec_num = rec_id.split('-')[1]

        for d in range(max_duplicate_per_record*2):
          tmp_rec_id = 'rec-%s-dup-%d' % (rec_num,d)
          if tmp_rec_id in rec_dict:
            num_dups += 1
        if (num_dups > max_duplicate_per_record):
          passed = False
          test_res_list.append('  Too many duplicate records for original' + \
                               ' record "%s": %d' % (rec_id), num_dups)

        d_count = num_dup_counts.get(num_dups, 0) + 1
        num_dup_counts[num_dups] = d_count

        # Check no duplicate number is outside expected range
        #
        for d in range(max_duplicate_per_record,max_duplicate_per_record*2):
          tmp_rec_id = 'rec-%s-dup-%d' % (rec_num,d)
          if (tmp_rec_id in rec_dict):
            passed = False
            test_res_list.append('  Illegal duplicate number: %s' % \
                                 (tmp_rec_id)+' (larger than max. number ' + \
                                 'of duplicates per record %sd' % \
                                 (max_duplicate_per_record))

        # Check values in certain attributes only contain letters
        #
        for i in [0,1,2,10,11,12,13]:
          test_val = rec_list[i].replace(' ','')
          test_val = test_val.replace('-','')
          test_val = test_val.replace("'",'')
          if (test_val.isalpha() == False):
            passed = False
            test_res_list.append('  Value in attribute "%s" is not only ' % \
                                 (attr_name_list[i]) + 'letters:')
            test_res_list.append('    Org: %s' % (str(rec_list)))

        # Check values in certain attributes only contain digits
        #
        for i in [3,4,5,6,7,8,9,14,15,16,17,18,19]:
          test_val = rec_list[i].replace(' ','')
          test_val = test_val.replace('.','')
          if (test_val.isdigit() == False):
            passed = False
            test_res_list.append('  Value in attribute "%s" is not only ' % \
                                 (attr_name_list[i]) + 'digits:')
            test_res_list.append('    Org: %s' % (str(rec_list)))

        # Check age values are in range
        #
        for i in [6,7,16]:
          test_val = int(rec_list[i].strip())
          if ((test_val < 0) or (test_val > 130)):
            passed = False
            test_res_list.append('  Age value in attribute "%s" is out of' % \
                                 (attr_name_list[i]) + ' range:')
            test_res_list.append('    Org: %s' % (str(rec_list)))

        # Check length of postcode, telephone and credit card numbers
        #
        if (len(rec_list[3]) != 4):
          passed = False
          test_res_list.append('  Postcode has not 4 digits:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

        if ((len(rec_list[4]) != 12) or (rec_list[4][0] != '0')):
          passed = False
          test_res_list.append('  Australian phone number has wrong format:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

        # Check 'rating' is between 0 and 5
        #
        test_val = int(rec_list[9].strip())
        if ((test_val < 0) or (test_val > 5)):
          passed = False
          test_res_list.append('  "rating-normal" value is out of range:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

        # Check gender values
        #
        test_val = rec_list[10]
        if (test_val not in ['male','female']):
          passed = False
          test_res_list.append('  "gender" value is out of range:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

        test_val = rec_list[11]
        if (test_val not in ['m','f','na']):
          passed = False
          test_res_list.append('  "alt-gender" value is out of range:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

        test_val = rec_list[12]
        if (test_val not in ['male','female']):
          passed = False
          test_res_list.append('  "alt-gender-2" value is out of range:')
          test_res_list.append('    Org: %s' % (str(rec_list)))

      if ('dup' in rec_id):  # A duplicate record

        # Get the corresponding original record
        #
        org_rec_id = 'rec-%s-org' % (rec_id.split('-')[1])
        org_rec_list = rec_dict[org_rec_id]

        # Check the duplicate number
        #
        dup_num = int(rec_id.split('-')[-1])
        if ((dup_num < 0) or (dup_num > max_duplicate_per_record-1)):
          passed = False
          test_res_list.append('  Duplicate record with identifier "%s" ' % \
                               (rec_id) + ' has an illegal duplicate number:' \
                               + ' %d' % (dup_num))
          test_res_list.append('    Org: %s' % (str(org_rec_list)))
          test_res_list.append('    Dup: %s' % (str(rec_list)))

        # Check that a duplicate record contains the expected - - - - - - - - -
        # number of modifications

        num_diff_val = 0  # Count how many values are different

        for i in range(len(rec_list)):  # Check all attribute values
          if (rec_list[i] != org_rec_list[i]):
            num_diff_val += 1

        if (num_diff_val == 0):  # No differences between org and dup record
          passed = False
          test_res_list.append('  Duplicate record with identifier "%s" ' % \
                               (rec_id) + 'is the same as it original record')
          test_res_list.append('    Org: %s' % (str(org_rec_list)))
          test_res_list.append('    Dup: %s' % (str(rec_list)))

        if (num_diff_val < num_modification_per_record):
          passed = False
          test_res_list.append('  Duplicate record with identifier "%s" ' % \
                               (rec_id) + 'contains less modifications ' + \
                               'than expected (%d instead of %d)' % \
                               (num_diff_val, num_modification_per_record))
          test_res_list.append('    Org: %s' % (str(org_rec_list)))
          test_res_list.append('    Dup: %s' % (str(rec_list)))

        # Check that certain attributes have not been modified
        #
        for i in [5,6,9,11,12,15,16,17,18,19]:
          if (rec_list[i] != org_rec_list[i]):
            passed = False
            test_res_list.append('  Duplicate record with identifier "%s" ' % \
                                 (rec_id) + 'contains modified attribute ' + \
                                 'values that should not be modified')
            test_res_list.append('    Org: %s' % (str(org_rec_list)))
            test_res_list.append('    Dup: %s' % (str(rec_list)))

        # Check the content of certain attribute values, and how they
        # differ between original and duplicate records
        #
        # Due to the possibility thatmultiple modifications are applied on the
        # same attribute these tests are limited

        test_org_val = org_rec_list[2]  # City
        test_dup_val = rec_list[2]
        if (test_dup_val != ''):
          if (len(test_org_val) != len(test_dup_val)):
            passed = False
            test_res_list.append('  "city" values have different length:')
            test_res_list.append('    Org: %s' % (str(org_rec_list)))
            test_res_list.append('    Dup: %s' % (str(rec_list)))

        test_org_val = org_rec_list[4]  # Australian phone number
        test_dup_val = rec_list[4]
        if (test_dup_val != ''):
          if (len(test_org_val) != len(test_dup_val)):
            passed = False
            test_res_list.append('  "oz-phone-number" values have different' + \
                                 ' length:')
            test_res_list.append('    Org: %s' % (str(org_rec_list)))
            test_res_list.append('    Dup: %s' % (str(rec_list)))

        test_org_val = org_rec_list[7]  # Age-death-normal
        test_dup_val = rec_list[7]
        if (test_dup_val != 'unknown'):
          if (test_org_val != test_dup_val):
            passed = False
            test_res_list.append('  Wrong value for "age-death-normal":')
            test_res_list.append('    Org: %s' % (str(org_rec_list)))
            test_res_list.append('    Dup: %s' % (str(rec_list)))

        test_org_val = org_rec_list[14]  # Income
        test_dup_val = rec_list[14]
        if (test_dup_val != 'miss'):
          if (test_org_val != test_dup_val):
            passed = False
            test_res_list.append('  Wrong value for "income":')
            test_res_list.append('    Org: %s' % (str(org_rec_list)))
            test_res_list.append('    Dup: %s' % (str(rec_list)))

    test_res_list.append('  Distribution of duplicates: ("%s" expected)' % \
                         num_duplicates_distribution)
    dup_keys = num_dup_counts.keys()
    dup_keys.sort()
    for d in dup_keys:
      test_res_list.append('    %d: %d records' % (d, num_dup_counts[d]))
    test_res_list.append('')

    if (passed == True):
      test_res_list.append('  All tests passed')
    test_res_list.append('')

    return test_res_list

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
out_file_name = './logs/mainTest-%s.txt' % (curr_time_str)

out_file = open(out_file_name, 'w')

out_file.write('Test results generated by mainTest.py'  + os.linesep)

out_file.write('Test started: ' + curr_time_str + os.linesep)

out_file.write(os.linesep)

for test_case in test_cases:

  # Create instances for the testcase class that calls all tests
  #
  test_case_ins = TestCase('testDataGeneration')
  test_res_list = test_case_ins.testDataGeneration(test_case)

  # Write test output results into the log file
  #
  for line in test_res_list:
    out_file.write(line + os.linesep)

  for line in test_res_list:
    print line

out_file.close()

print 'Test results are written to', out_file_name


# =============================================================================
