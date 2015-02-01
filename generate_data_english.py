# generate-data-english.py - Python module to generate synthetic data based on
#                            English look-up and error tables.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

# Import the necessary other modules of the data generator
#
import basefunctions  # Helper functions
import attrgenfunct   # Functions to generate independent attribute values
import contdepfunct   # Functions to generate dependent continuous attribute
                      # values
import generator      # Main classes to generate records and the data set
import corruptor      # Main classes to corrupt attribute values and records

import random
random.seed(42)  # Set seed for random generator, so data generation can be
                 # repeated

# Set the Unicode encoding for this data generation project. This needs to be
# changed to another encoding for different Unicode character sets.
# Valid encoding strings are listed here:
# http://docs.python.org/library/codecs.html#standard-encodings
#
unicode_encoding_used = 'ascii'

# The name of the record identifier attribute (unique value for each record).
# This name cannot be given as name to any other attribute that is generated.
#
rec_id_attr_name = 'rec-id'

# Set the file name of the data set to be generated (this will be a comma
# separated values, CSV, file).
#
out_file_name = 'example-data-english.csv'

# Set how many original and how many duplicate records are to be generated.
#
num_org_rec = 10000
num_dup_rec = 10000

# Set the maximum number of duplicate records can be generated per original
# record.
#
max_duplicate_per_record = 3

# Set the probability distribution used to create the duplicate records for one
# original record (possible values are: 'uniform', 'poisson', 'zipf').
#
num_duplicates_distribution = 'zipf'

# Set the maximum number of modification that can be applied to a single
# attribute (field).
#
max_modification_per_attr = 1

# Set the number of modification that are to be applied to a record.
#
num_modification_per_record = 5

# Check if the given the unicode encoding selected is valid.
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

# -----------------------------------------------------------------------------
# Define the attributes to be generated (using methods from the generator.py
# module).
#
gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'given-name',
                          freq_file_name = 'lookup-files/givenname_f_freq.csv',
                          has_header_line = False,
                          unicode_encoding = unicode_encoding_used)

sname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'surname',
                          freq_file_name = 'lookup-files/surname-freq.csv',
                          has_header_line = False,
                          unicode_encoding = unicode_encoding_used)

postcode_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'postcode',
                          freq_file_name = 'lookup-files/postcode_act_freq.csv',
                          has_header_line = False,
                          unicode_encoding = unicode_encoding_used)

phone_num_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'telephone-number',
                       function = attrgenfunct.generate_phone_number_australia)

credit_card_attr =  \
    generator.GenerateFuncAttribute(attribute_name = 'credit-card-number',
                       function = attrgenfunct.generate_credit_card_number)

age_uniform_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'age-uniform',
                       function = attrgenfunct.generate_uniform_age,
                       parameters = [0,120])

income_normal_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'income-normal',
                       function = attrgenfunct.generate_normal_value,
                       parameters = [50000,20000, 0, 1000000, 'float2'])

rating_normal_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'rating-normal',
                       function = attrgenfunct.generate_normal_value,
                       parameters = [0.0,1.0, None, None, 'float9'])

gender_city_comp_attr = \
    generator.GenerateCateCateCompoundAttribute(\
          categorical1_attribute_name = 'gender',
          categorical2_attribute_name = 'city',
          lookup_file_name = 'lookup-files/gender-city.csv',
          has_header_line = True,
          unicode_encoding = 'ascii')

sex_income_comp_attr = \
    generator.GenerateCateContCompoundAttribute(\
          categorical_attribute_name = 'sex',
          continuous_attribute_name = 'income',
          continuous_value_type = 'float1',
          lookup_file_name = 'lookup-files/gender-income.csv',
          has_header_line = False,
          unicode_encoding = 'ascii')

gender_town_salary_comp_attr = \
    generator.GenerateCateCateContCompoundAttribute(\
          categorical1_attribute_name = 'alternative-gender',
          categorical2_attribute_name = 'town',
          continuous_attribute_name = 'salary',
          continuous_value_type = 'float4',
          lookup_file_name = 'lookup-files/gender-city-income.csv',
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

age_salary_comp_attr = \
    generator.GenerateContContCompoundAttribute(\
          continuous1_attribute_name = 'age2',
          continuous2_attribute_name = 'salary2',
          continuous1_funct_name =     'normal',
          continuous1_funct_param =    [45,20,15,130],
          continuous2_function = contdepfunct.salary_depending_on_age,
          continuous1_value_type = 'int',
          continuous2_value_type = 'float1')

# -----------------------------------------------------------------------------
# Define how the generated records are to be corrupted (using methods from
# the corruptor.py module).

# For a value edit corruptor, the sum or the four probabilities given must
# be 1.0.
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
          lookup_file_name = 'lookup-files/surname-misspell.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

ocr_corruptor = corruptor.CorruptValueOCR(\
          position_function = corruptor.position_mod_normal,
          lookup_file_name = 'lookup-files/ocr-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(\
          position_function = corruptor.position_mod_normal,
          row_prob = 0.5,
          col_prob = 0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(\
          lookup_file_name = 'lookup-files/phonetic-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

missing_val_corruptor = corruptor.CorruptMissingValue()

postcode_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_val='missing')

given_name_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_value='unknown')

# -----------------------------------------------------------------------------
# Define the attributes to be generated for this data set, and the data set
# itself.
#
attr_name_list = ['gender', 'given-name', 'surname', 'postcode', 'city',
                  'telephone-number', 'credit-card-number', 'income-normal',
                  'age-uniform', 'income', 'age', 'sex', 'blood-pressure']

attr_data_list = [gname_attr, sname_attr, postcode_attr, phone_num_attr,
                  credit_card_attr, age_uniform_attr, income_normal_attr,
                  gender_city_comp_attr, sex_income_comp_attr,
                  gender_town_salary_comp_attr, age_blood_pressure_comp_attr,
                  age_salary_comp_attr]

# Nothing to change here - set-up the data set generation object.
#
test_data_generator = generator.GenerateDataSet(output_file_name = \
                                          out_file_name,
                                          write_header_line = True,
                                          rec_id_attr_name = rec_id_attr_name,
                                          number_of_records = num_org_rec,
                                          attribute_name_list = attr_name_list,
                                          attribute_data_list = attr_data_list,
                                          unicode_encoding = \
                                                         unicode_encoding_used)

# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#
attr_mod_prob_dictionary = {'gender':0.1, 'given-name':0.2,'surname':0.2,
                            'postcode':0.1,'city':0.1, 'telephone-number':0.15,
                            'credit-card-number':0.1,'age':0.05}

# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {'gender':[(1.0, missing_val_corruptor)],
                            'surname':[(0.1, surname_misspell_corruptor),
                                       (0.1, ocr_corruptor),
                                       (0.1, keyboard_corruptor),
                                       (0.7, phonetic_corruptor)],
                            'given-name':[(0.1, edit_corruptor2),
                                          (0.1, ocr_corruptor),
                                          (0.1, keyboard_corruptor),
                                          (0.7, phonetic_corruptor)],
                            'postcode':[(0.8, keyboard_corruptor),
                                        (0.2, postcode_missing_val_corruptor)],
                            'city':[(0.1, edit_corruptor),
                                    (0.1, missing_val_corruptor),
                                    (0.4, keyboard_corruptor),
                                    (0.4, phonetic_corruptor)],
                            'age':[(1.0, edit_corruptor2)],
                            'telephone-number':[(1.0, missing_val_corruptor)],
                            'credit-card-number':[(1.0, edit_corruptor)]}

# Nothing to change here - set-up the data set corruption object
#
test_data_corruptor = corruptor.CorruptDataSet(number_of_org_records = \
                                          num_org_rec,
                                          number_of_mod_records = num_dup_rec,
                                          attribute_name_list = attr_name_list,
                                          max_num_dup_per_rec = \
                                                 max_duplicate_per_record,
                                          num_dup_dist = \
                                                 num_duplicates_distribution,
                                          max_num_mod_per_attr = \
                                                 max_modification_per_attr,
                                          num_mod_per_rec = \
                                                 num_modification_per_record,
                                          attr_mod_prob_dict = \
                                                 attr_mod_prob_dictionary,
                                          attr_mod_data_dict = \
                                                 attr_mod_data_dictionary)

# =============================================================================
# No need to change anything below here

# Start the data generation process
#
rec_dict = test_data_generator.generate()

assert len(rec_dict) == num_org_rec  # Check the number of generated records

# Corrupt (modify) the original records into duplicate records
#
rec_dict = test_data_corruptor.corrupt_records(rec_dict)

assert len(rec_dict) == num_org_rec+num_dup_rec # Check total number of records

# Write generate data into a file
#
test_data_generator.write()

# End.
# =============================================================================
