

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
num_org_rec = 20
num_dup_rec = 5

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
class AttrSet(object):
    def __init__(self):
        self.name_prefix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-prefix',
                       function = attrgenfunct.generate_name_prefix_f)
        self.gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = 'lookup-files/givenname_f_freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.mname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'middle-name',
                    freq_file_name = 'lookup-files/givenname_f_freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.sname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'surname',
                    freq_file_name = 'lookup-files/surname-freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.name_suffix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-suffix',
                   function = attrgenfunct.generate_name_suffix)
        
        self.race_hispanic = \
    generator.GenerateFreqAlt(attribute_name = 'race-hispanic',
                    freq_file_name = 'lookup-files/race_w_hispanic_ascii.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.sname_prev_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'previous-surname',
                    freq_file_name = 'lookup-files/surname-freq.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.nickname_attr = \
            generator.GenerateFuncAttribute(attribute_name = 'nickname',
                    function = attrgenfunct.generate_nickname)


        self.postcode_attr = \
            generator.GenerateFreqAttribute(attribute_name = 'postcode',
                      freq_file_name = 'lookup-files/postcode_act_freq.csv',
                      has_header_line = False,
                      unicode_encoding = unicode_encoding_used)

        self.phone_num_attr = \
            generator.GenerateFuncAttribute(attribute_name = 'telephone-number',
                       function = attrgenfunct.generate_phone_number_australia)

        #Cell
        self.phone_num_cell_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'cell-number',
                           function = attrgenfunct.generate_phone_number_american)
        #Work
        self.phone_num_work_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'work-number',
                           function = attrgenfunct.generate_phone_number_american)
        #Home
        self.phone_num_home_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'home-number',
                           function = attrgenfunct.generate_phone_number_american)

        self.credit_card_attr =  \
                generator.GenerateFuncAttribute(attribute_name = 'credit-card-number',
                           function = attrgenfunct.generate_credit_card_number)

        self.social_security_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'social-security-number',
                          function = attrgenfunct.generate_social_security_number)

        self.age_uniform_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'age-uniform',
                           function = attrgenfunct.generate_uniform_age,
                           parameters = [0,120])

        self.income_normal_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'income-normal',
                           function = attrgenfunct.generate_normal_value,
                           parameters = [50000,20000, 0, 1000000, 'float2'])

        self.rating_normal_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'rating-normal',
                           function = attrgenfunct.generate_normal_value,
                           parameters = [0.0,1.0, None, None, 'float9'])

        #passport
        self.passport_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'passport-number',
                function = attrgenfunct.generate_passport_num)

            
        self.race_hispanic = \
                generator.GenerateFreqAlt(attribute_name = 'race-hispanic',
                                freq_file_name = 'lookup-files/race_w_hispanic_ascii.csv',
                                has_header_line = False,
                                unicode_encoding = unicode_encoding_used)

        # Calculating age off of frequency distribution of age.  Currently referencing female file
        # Male csv file also exists once we can get the age generated based on gender
        self.new_age_attr = \
              generator.GenerateFreqAlt(attribute_name = 'age-new',
                                freq_file_name = 'lookup-files/age_gender_ratio_female.csv',
                                has_header_line = False,
                                unicode_encoding = unicode_encoding_used) 

        # Calculating the DOB.  Requires the age to be passed
        self.DOB_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'DOB',
                                   function = attrgenfunct.generate_DOB)
        
        self.labels = ['given-name', 'middle-name', 'surname', 'name-suffix',
                       'race_hispanic', 'email'] 
        self.labels2 = ['postcode', 'city', 'previous-surname', 'nickname', 
                        'cell-number', 'work-number', 'home-number',  
                      'social-security-number', 'credit-card-number', 
                      'income-normal', 'age-uniform', 'income', 
                      'age', 'sex', 'blood-pressure', 'passport-number',
                      'email', 'race-hispanic', 'age-new', 'DOB']


    def output(self):
        'create synthetic output'
        #removed all compound attribute
        #single attr need create_attribute_values(), singular
        #compound attr need create_attribute_values(), plural!
        #must update compound context to USA
        primary = [self.gname_attr, self.mname_attr, 
                   self.sname_attr, self.name_suffix_attr]
        
        add_out = [self.name_prefix_attr, self.nickname_attr, self.postcode_attr, 
          self.phone_num_attr,
          self.phone_num_cell_attr, self.phone_num_work_attr, 
          self.phone_num_home_attr, self.social_security_attr, 
          self.credit_card_attr, self.age_uniform_attr, 
          self.income_normal_attr, self.passport_attr, 
          self.new_age_attr, self.DOB_attr]

        #primary.extend(add_out)
        
        out = [attr.create_attribute_value() for attr in primary]
        
        labels = [attr.attribute_name for attr in primary]

        self.race = self.race_hispanic.random_pick().split('..')[1]
        self.hispanic = self.race_hispanic.random_pick().split('..')[0]

        self.race_attr = generator.GenerateFuncAttribute(attribute_name='race',
          function = attrgenfunct.race,
          parameters = [str(self.race)])

        out.append(self.race_attr.create_attribute_value())
        labels.append(self.race_attr.attribute_name)
        
        self.hispanic_attr = generator.GenerateFuncAttribute(attribute_name='hispanic',
          function = attrgenfunct.hispanic,
          parameters=[str(self.hispanic)])
        
        out.append(self.hispanic_attr.create_attribute_value())
        labels.append(self.hispanic_attr.attribute_name)

        self.email_attr = generator.GenerateFuncAttribute(attribute_name = 'email',
          function = attrgenfunct.generate_email_address,
          parameters = [str(out[0]), str(out[2])])

        out.append(self.email_attr.create_attribute_value())
        labels.append(self.email_attr.attribute_name)

        return out

    def object_out(self):
        'create synthetic output'
        #removed all compound attribute
        #single attr need create_attribute_values(), singular
        #compound attr need create_attribute_values(), plural!
        #must update compound context to USA
        primary = [self.gname_attr, self.mname_attr, 
                   self.sname_attr, self.name_suffix_attr]
        
        add_out = [self.name_prefix_attr, self.nickname_attr, self.postcode_attr, 
          self.phone_num_attr,
          self.phone_num_cell_attr, self.phone_num_work_attr, 
          self.phone_num_home_attr, self.social_security_attr, 
          self.credit_card_attr, self.age_uniform_attr, 
          self.income_normal_attr, self.passport_attr, 
          self.new_age_attr, self.DOB_attr]

        #primary.extend(add_out)
        
        #out = [attr.create_attribute_value() for attr in primary]
        
        labels = [attr.attribute_name for attr in primary]
        race_hispanic = self.race_hispanic.random_pick()
        race_hispanic = race_hispanic.split('..')

        self.race_attr = generator.GenerateFuncAttribute(attribute_name='race',
          function = attrgenfunct.race,
          parameters = [str(race_hispanic[0])])

        primary.append(self.race_attr)
        
        self.hispanic_attr = generator.GenerateFuncAttribute(attribute_name='hispanic',
          function = attrgenfunct.hispanic,
          parameters=[str(race_hispanic[1])]
          )
        
        primary.append(self.hispanic_attr)
        email_out_0 = primary[0].create_attribute_value()
        email_out_2 = primary[2].create_attribute_value()

        self.email_attr = generator.GenerateFuncAttribute(attribute_name = 'email',
          function = attrgenfunct.generate_email_address,
          parameters = [str(email_out_0), str(email_out_2)]
          )

        primary.append(self.email_attr)

        return primary

attr_name_list = ['given-name', 'middle-name', 'surname', 'name-suffix',
                   'race', 'hispanic', 'email'] 

attr_data_list = AttrSet().object_out()               

labels = ['gender', 'name-prefix', 'given-name', 'middle-name', 'surname', 'name-suffix', 'postcode', 'city',
                  'previous-surname', 'nickname', 'cell-number', 'work-number', 'home-number',  
                  'social-security-number', 'credit-card-number', 
                  'income-normal', 'age-uniform', 'income', 
                  'age', 'sex', 'blood-pressure', 'passport-number',
                  'email', 'race-hispanic', 'age-new', 'DOB']
'''
attr_list = [age_uniform_attr,
 credit_card_attr,
 email_attr,
 gname_attr,
 income_normal_attr,
 mname_attr,
 name_prefix_attr,
 name_suffix_attr,
 new_age_attr,
 nickname_attr,
 output,
 passport_attr,
 phone_num_attr,
 phone_num_cell_attr,
 phone_num_home_attr,
 phone_num_work_attr,
 postcode_attr,
 race_hispanic,
 rating_normal_attr,
 sname_attr,
 sname_prev_attr,
 social_security_attr]
'''

# Nothing to change here - set-up the data set generation object.
#
'''test_data_generator = generator.GenerateDataSet(output_file_name = \
                                          out_file_name,
                                          write_header_line = True,
                                          rec_id_attr_name = rec_id_attr_name,
                                          number_of_records = num_org_rec,
                                          attribute_name_list = attr_name_list,
                                          attribute_data_list = attr_data_list,
                                          unicode_encoding = unicode_encoding_used)

# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#
attr_mod_prob_dictionary = {'given-name':0.2,'surname':0.2}
                            #'gender':0.1,
                            #'postcode':0.1,'city':0.1, 'cell-number':0.15,
                            #'credit-card-number':0.1,'age':0.05

# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {'surname':[(0.1, surname_misspell_corruptor),
                                       (0.1, ocr_corruptor),
                                       (0.1, keyboard_corruptor),
                                       (0.7, phonetic_corruptor)],
                            'given-name':[(0.1, edit_corruptor2),
                                          (0.1, ocr_corruptor),
                                          (0.1, keyboard_corruptor),
                                          (0.7, phonetic_corruptor)]}
                            #'gender':[(1.0, missing_val_corruptor)],
                            #'postcode':[(0.8, keyboard_corruptor),
                            #            (0.2, postcode_missing_val_corruptor)],
                            #'city':[(0.1, edit_corruptor),
                            #        (0.1, missing_val_corruptor),
                            #        (0.4, keyboard_corruptor),
                            #        (0.4, phonetic_corruptor)],
                            #'age':[(1.0, edit_corruptor2)],
                            #'cell-number':[(1.0, missing_val_corruptor)],
                            #'credit-card-number':[(1.0, edit_corruptor)]

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
'''