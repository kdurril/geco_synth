

# Import the necessary other modules of the data generator
#
import basefunctions  # Helper functions
import attrgenfunct   # Functions to generate independent attribute values
import contdepfunct   # Functions to generate dependent continuous attribute
                      # values
import generator      # Main classes to generate records and the data set
import corruptor      # Main classes to corrupt attribute values and records


import random
import csv
import json
import os
import StringIO
from collections import OrderedDict, namedtuple

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
num_org_rec = 4
num_dup_rec = 2

# Set the maximum number of duplicate records can be generated per original
# record.
#
max_duplicate_per_record = 1

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
num_modification_per_record = 2

# Check if the given the unicode encoding selected is valid.
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)


# -----------------------------------------------------------------------------

class AttrMeta(type):
    def __init__(self, *args):
        super(AttrMeta, self).__init__(*args)

        self.race_hispanic = \
            generator.GenerateFreqAlt(attribute_name = 'race-hispanic',
                    freq_file_name = os.path.abspath('lookup_files/race_w_hispanic_ascii.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
    
        self.sname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'surname',
                    freq_file_name = os.path.abspath('lookup_files/lastname.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.name_suffix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-suffix',
                   function = attrgenfunct.generate_name_suffix)

        self.sname_prev_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'previous-surname',
                    freq_file_name = os.path.abspath('lookup_files/lastname.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.nickname_attr = \
            generator.GenerateFuncAttribute(attribute_name = 'nickname',
                    function = attrgenfunct.generate_nickname)

        self.postcode_attr = \
            generator.GenerateFreqAttribute(attribute_name = 'postcode',
                      freq_file_name = os.path.abspath('lookup_files/postcode_ascii.csv'),
                      has_header_line = False,
                      unicode_encoding = unicode_encoding_used)
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

        #passport
        self.passport_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'passport-number',
                function = attrgenfunct.generate_passport_num)

        # Mother maiden name
        self.mother = \
    generator.GenerateFreqAttribute(attribute_name = 'mother-maiden-name',
                    freq_file_name = os.path.abspath('lookup_files/lastname.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.address_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'street-address',
                function = attrgenfunct.generate_address)
        
        self.city_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'city',
                function = attrgenfunct.generate_city)

        self.state_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'state',
                function = attrgenfunct.generate_state)

        self.primary_ID_attr = \
                generator.GenerateFuncAttribute(attribute_name = 'primary_key',
                function = attrgenfunct.generate_primary)



class AttrSet(object):
    "the female gender class"
    
    __metaclass__ = AttrMeta

    def __init__(self, *args):

        self.gender_attr = generator.GenerateFuncAttribute(attribute_name='gender',
          function = attrgenfunct.gender,
          parameters=[str('Female')])

        self.name_prefix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-prefix',
                       function = attrgenfunct.generate_name_prefix_f)
        self.gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_female.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.mname_attr =\
    generator.GenerateFreqAttribute(attribute_name = 'middle-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_female.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.name_suffix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-suffix',
                   function = attrgenfunct.generate_name_suffix)

        # Calculating age off of frequency distribution of age.  Currently referencing female file
        # Male csv file also exists once we can get the age generated based on gender
        self.new_age_attr = \
              generator.GenerateFreqAlt(attribute_name = 'age-new',
                                freq_file_name = os.path.abspath('lookup_files/age_gender_ratio_female.csv'),
                                has_header_line = False,
                                unicode_encoding = unicode_encoding_used)
    
    AttrCheck = namedtuple('AttrCheck',['primary_ID','gname', 'mname','sname','name_suffix',\
                                  'name_prefix','sname_prev','nickname','new_age',\
                                  'gender','address','city','state','postcode',\
                                  'phone_num_cell','phone_num_work','phone_num_home',\
                                  'credit_card','social_security','passport','mother'])

    def output(self):
        'create synthetic output'
        #removed all compound attribute
        #single attr need create_attribute_values(), singular
        #compound attr need create_attribute_values(), plural!
        #must update compound context to USA
        primary = [self.primary_ID_attr, self.gname_attr, self.mname_attr, 
                  self.sname_attr, self.name_suffix_attr,
                  self.name_prefix_attr, 
                  self.sname_prev_attr, self.nickname_attr,
                  self.new_age_attr, self.gender_attr, self.address_attr,
                  self.city_attr, self.state_attr,
                  self.postcode_attr, self.phone_num_cell_attr,
                  self.phone_num_work_attr, self.phone_num_home_attr,
                  self.credit_card_attr, self.social_security_attr,
                  self.passport_attr, self.mother]
        
        #add_out = [self.name_prefix_attr, self.nickname_attr,
        #  self.phone_num_cell_attr, self.phone_num_work_attr, 
        #  self.phone_num_home_attr, self.social_security_attr, 
        #  self.credit_card_attr,
        #  self.passport_attr, 
        #  self.new_age_attr]

        #primary.extend(add_out)
        
        out = [attr.create_attribute_value() for attr in primary]
        
        labels = [attr.attribute_name for attr in primary]
        
        self.email_attr = generator.GenerateFuncAttribute(attribute_name = 'email',
          function = attrgenfunct.generate_email_address,
          parameters = [str(out[1]), str(out[3])]
          )

        out.append(self.email_attr.create_attribute_value())
        labels.append(self.email_attr.attribute_name)

        self.DOB_attr = generator.GenerateFuncAttribute(attribute_name = 'DOB',
           function = attrgenfunct.generate_DOB,
           parameters = [int(out[8])]
           )

        out.append(self.DOB_attr.create_attribute_value())
        labels.append(self.DOB_attr.attribute_name)

        r_h = self.race_hispanic.random_pick().split('..')
        self.race = r_h[1]
        self.hispanic = r_h[0]

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

        self.marriage_attr = generator.GenerateFuncAttribute(attribute_name='marital-status',
          function = attrgenfunct.marriage,
          parameters=[int(out[8])])
        
        out.append(self.marriage_attr.create_attribute_value())
        labels.append(self.marriage_attr.attribute_name)

        outputwork2 = OrderedDict(zip(labels,out))
        
        return outputwork2


    def output_alt(self, *args, **kwargs):
          'selective attribute output'

          required = [self.primary_ID_attr, self.gname_attr, self.mname_attr, 
                  self.sname_attr, self.name_suffix_attr,
                  self.name_prefix_attr, 
                  self.sname_prev_attr, self.nickname_attr,
                  self.new_age_attr, self.gender_attr, self.address_attr,
                  self.city_attr, self.state_attr,
                  self.postcode_attr]
          
          select_tup = self.AttrCheck(self.primary_ID_attr,
          self.gname_attr, 
          self.mname_attr, 
          self.sname_attr, 
          self.name_suffix_attr,
          self.name_prefix_attr, 
          self.sname_prev_attr, 
          self.nickname_attr,
          self.new_age_attr, 
          self.gender_attr, 
          self.address_attr,
          self.city_attr, 
          self.state_attr,
          self.postcode_attr, 
          self.phone_num_cell_attr,
          self.phone_num_work_attr, 
          self.phone_num_home_attr,
          self.credit_card_attr, 
          self.social_security_attr,
          self.passport_attr, 
          self.mother)

          #tick will be the true or false tuple
          #j will be the select_tup
          #tick = self.AttrCheck(*args)
          #select=(getattr(select_tup,x) for x in select_tup._fields if getattr(tick,x)==True)
          
          select = [select_tup._asdict()[y] for y in args]
          
          out = OrderedDict((attr.attribute_name, attr.create_attribute_value()) for attr in select)


          def attr_out_set(container, attr):
              container[attr.attribute_name] = attr.create_attribute_value() 

          self.email_attr = generator.GenerateFuncAttribute(attribute_name = 'email',
              function = attrgenfunct.generate_email_address,
              parameters = [str(out['given-name']), str(out['surname'])]
              )

          self.DOB_attr = generator.GenerateFuncAttribute(attribute_name = 'DOB',
           function = attrgenfunct.generate_DOB,
           parameters = [int(out['age-new'])]
           )

          r_h = self.race_hispanic.random_pick().split('..')
          self.race = r_h[1]
          self.hispanic = r_h[0]

          self.race_attr = generator.GenerateFuncAttribute(attribute_name='race',
              function = attrgenfunct.race,
              parameters = [str(self.race)])

          self.hispanic_attr = generator.GenerateFuncAttribute(attribute_name='hispanic',
          function = attrgenfunct.hispanic,
          parameters=[str(self.hispanic)])

          self.marriage_attr = generator.GenerateFuncAttribute(attribute_name='marital-status',
          function = attrgenfunct.marriage,
          parameters=[int(out['age-new'])])

          dependent = [self.email_attr, self.DOB_attr, self.race_attr,\
                    self.hispanic_attr, self.marriage_attr]

          for value in dependent:
              attr_out_set(out, value)

          return out



class AttrSetM(AttrSet):
    "the male gender class"
    def __init__(self):

        self.gender_attr = generator.GenerateFuncAttribute(attribute_name='gender',
          function = attrgenfunct.gender,
          parameters=[str('Male')])

        self.gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_male.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
        self.mname_attr =\
    generator.GenerateFreqAttribute(attribute_name = 'middle-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_male.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.name_suffix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-suffix',
                   function = attrgenfunct.generate_name_suffix)

        self.sname_prev_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'previous-surname',
                   function = attrgenfunct.generate_surname_m)

        self.name_prefix_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'name-prefix',
                       function = attrgenfunct.generate_name_prefix_m)
        
        self.sname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'surname',
                    freq_file_name = os.path.abspath('lookup_files/lastname.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

        self.new_age_attr = \
              generator.GenerateFreqAlt(attribute_name = 'age-new',
                                freq_file_name = os.path.abspath('lookup_files/age_gender_ratio_male.csv'),
                                has_header_line = False,
                                unicode_encoding = unicode_encoding_used)


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
          lookup_file_name = 'lookup_files/surname-misspell.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

ocr_corruptor = corruptor.CorruptValueOCR(\
          position_function = corruptor.position_mod_normal,
          lookup_file_name = 'lookup_files/ocr-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(\
          position_function = corruptor.position_mod_normal,
          row_prob = 0.5,
          col_prob = 0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(\
          lookup_file_name = 'lookup_files/phonetic-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

missing_val_corruptor = corruptor.CorruptMissingValue()

postcode_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_val='missing')

given_name_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_value='unknown')

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
'''
# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#
attr_mod_prob_dictionary = {'given-name':0.05, 'middle-name':0.05, 'gender':0.05, 'surname':0.05,'postcode':0.05,
              'cell-number':0.05, 'work-number':0.05,
              'home-number':0.05, 'social-security-number':0.05, 'passport-number':0.05, 
              'credit-card-number':0.05, 'name-suffix': .01, 'name-prefix': 0.01, 'previous-surname':0.05,
              'mother-maiden-name':0.05, 'street-address':0.05, 'email':0.05, 'race':0.01, 
              'hispanic':0.01, 'city':0.01, 'state':0.05, 'age-new':0.05, 'DOB':0.05, 'marital-status':0.05}
                            

# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {'surname':[(0.15, surname_misspell_corruptor),
                                       (0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.15, edit_corruptor2),
                                       (0.1, missing_val_corruptor)],
                            'given-name':[(0.15, given_name_missing_val_corruptor), 
                                         (0.15, ocr_corruptor),
                                     (0.15, keyboard_corruptor),
                                         (0.15, phonetic_corruptor),
                                         (0.15, edit_corruptor),
                                         (0.15, edit_corruptor2),
                                         (0.1, missing_val_corruptor)],
                            'middle-name':[(0.15, given_name_missing_val_corruptor), 
                                         (0.15, ocr_corruptor),
                                     (0.15, keyboard_corruptor),
                                         (0.15, phonetic_corruptor),
                                         (0.15, edit_corruptor),
                                         (0.15, edit_corruptor2),
                                         (0.1, missing_val_corruptor)],
                            'gender':[(0.25, keyboard_corruptor),
                                       (0.25, edit_corruptor),
                                       (0.25, edit_corruptor2),
                                       (0.25, missing_val_corruptor)],
                            'postcode':[(0.3, keyboard_corruptor),
                                       (0.2, postcode_missing_val_corruptor),
                                       (0.5, missing_val_corruptor)],
                            'cell-number':[(0.1, edit_corruptor),
                                    (0.1, edit_corruptor2),
                                    (0.8, missing_val_corruptor)],
                            'work-number':[(0.1, edit_corruptor),
                                    (0.1, edit_corruptor2),
                                    (0.8, missing_val_corruptor)],
                            'home-number':[(0.1, edit_corruptor),
                                    (0.1, edit_corruptor2),
                                    (0.8, missing_val_corruptor)],
                            'social-security-number':[(0.2, edit_corruptor),
                                    (0.2, edit_corruptor2),
                                    (0.6, missing_val_corruptor)],
                            'credit-card-number':[(0.25, edit_corruptor),
                                    (0.25, edit_corruptor2),
                                    (0.5, missing_val_corruptor)],
                            'name-suffix':[(1.0, missing_val_corruptor)],
                            'name-prefix':[(1.0, missing_val_corruptor)],
                            'previous-surname':[(0.15, surname_misspell_corruptor),
                                       (0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.15, edit_corruptor2),
                                       (0.1, missing_val_corruptor)],
                            'passport-number':[(0.25, edit_corruptor),
                                    (0.25, edit_corruptor2),
                                    (0.5, missing_val_corruptor)],  
                            'mother-maiden-name':[(0.15, surname_misspell_corruptor),
                                       (0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.15, edit_corruptor2),
                                       (0.1, missing_val_corruptor)],
                            'street-address':[(0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.2, edit_corruptor2),
                                       (0.2, missing_val_corruptor)],
                            'email':[(0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.2, edit_corruptor2),
                                       (0.2, missing_val_corruptor)],
                            'race':[(0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.2, edit_corruptor2),
                                       (0.2, missing_val_corruptor)],
                            'hispanic':[(0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.2, edit_corruptor2),
                                       (0.2, missing_val_corruptor)],
                            'city':[(0.15, ocr_corruptor),
                                       (0.15, keyboard_corruptor),
                                       (0.15, phonetic_corruptor),
                                       (0.15, edit_corruptor),
                                       (0.2, edit_corruptor2),
                                       (0.2, missing_val_corruptor)], 
                            'state':[(0.25, keyboard_corruptor),
                                       (0.25, edit_corruptor),
                                       (0.25, edit_corruptor2),
                                       (0.25, missing_val_corruptor)],
                            'age-new':[(0.25, edit_corruptor),
                                    (0.25, edit_corruptor2),
                                    (0.5, missing_val_corruptor)], 
                            'DOB':[(0.25, edit_corruptor),
                                    (0.25, edit_corruptor2),
                                    (0.5, missing_val_corruptor)],
                            'marital-status':[(0.25, edit_corruptor),
                                    (0.25, edit_corruptor2),
                                    (0.5, missing_val_corruptor)]}
                                       
                            #'city':[(0.1, edit_corruptor),
                            #        (0.1, missing_val_corruptor),
                            #        (0.4, keyboard_corruptor),
                            #        (0.4, phonetic_corruptor)],
                            #'age':[(1.0, edit_corruptor2)],
                          

def row_synth(genfunct, row_count):
    'genfunct is an AttrSet object, row_count is int'
    return (genfunct.output() for x in xrange(row_count))

def row_synth_alt(genfunct, row_count):
    'genfunct is an AttrSet object, row_count is int'
    return (genfunct.output_alt() for x in xrange(row_count))

def row_keys(genfunct):
    'get keys for output labels'
    return genfunct.output().keys()

def to_corruptor(genfunct, row_count):
    'create output structured on GenerateDataSet generate()'
    return dict(('rec-'+str(y)+'-org', genfunct.output().values()) for y in range(row_count))

def to_corruptor_gf(genfunct_input):
    'input is already generated'
    g_list = list(genfunct_input)
    g_len = len(g_list)
    counter = ['rec-'+str(y)+'-org' for y in range(g_len)]
    value_list = [x.values() for x in g_list]
    return dict(zip(counter,value_list))

def to_corruptor_csv(genfunct, row_count):
    'this has no header, flattens and retains id from to_corruptor'
    corrupt_out = to_corruptor(genfunct, row_count)
    corrupt_out = test_data_corruptor.corrupt_records(corrupt_out)
    return (([k]+v) for k,v in corrupt_out.iteritems())

def from_tdc(tdc_in):
    'use input from test_data_corruptor.corrupt_records()'
    return (([k]+v) for k,v in tdc_in.iteritems())

def to_corruptor_write(corruptor_csv, file_name='English_corrupt_output.csv'):
    'write corruptor data with id row'
    
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow()
        writer.writerows(corruptor_csv)

    return file_name

def to_csv(genfunct_input, fieldnames,file_name='English_output.csv'):
    'genfucnt_input is the output from row_synth'
    
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(genfunct_input)
    return file_name

# Code to output to IO string vs CSV
def to_string(genfunct_input, fieldnames):
  'writing to an io string'
  output = StringIO.StringIO()
  writer = csv.DictWriter(output, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(genfunct_input)
  contents = output.getvalue()
  #print output.getvalue()
  return contents

# Code to output to IO string vs CSV
def to_corruptor_write_io_string(corruptor_csv):
    'write corruptor to an io string'
    output = StringIO.StringIO()
    writer = csv.writer(output)
    writer.writerows(corruptor_csv)
    corrupt_contents = output.getvalue()
    #print corrupt_contents
    return corrupt_contents

def to_json(genfunct_input, file_name='English_output.json'):
    'genfucnt_input is the output from row_synth'
    with open(file_name, 'a') as jsonfile:
        jsonfile.write(json.dumps(str(list(genfunct_input))))



def original_output(base_output, a):
    to_csv(base_output,a.output().keys())
    
def corrupt_output(a_output):
    to_corruptor_write(from_tdc(test_data_corruptor.corrupt_records(\
                                to_corruptor_gf(a_output))))

# Code to output to IO string vs CSV (next two functions)
def original_output2(base_output, a):
    to_string(base_output,a.output().keys())

def corrupt_output2(base_output):
  to_corruptor_write(from_tdc(test_data_corruptor.corrupt_records(\
                                to_corruptor_gf(base_output)))) 

attr_name_list = row_keys(AttrSet())

#attr_data_list = AttrSet().output().values()

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

'''
# =============================================================================
# No need to change anything below here

# Start the data generation process
#
#rec_dict = test_data_generator.generate()

rec_dict = to_corruptor(b, num_org_rec)

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
if __name__ == '__main__':
    b = AttrSet()
    c = AttrSetM()

    base_output_b = list(row_synth(b, num_org_rec/2 ))
    base_output_c = list(row_synth(c, num_org_rec/2 ))
    
    #Extend female engender list
    base_output_b.extend(base_output_c)
   
    #Shuffle the list
    #random.shuffle(base_output_b)

    #Creating the list to replace the primary key list

    i = 0
    y = 1
    while i < len(base_output_b):
      for x in base_output_b:
        x['primary_key'] = (i+1)
        i = i+1
    
    original_output(base_output_b, b)
    corrupt_output(base_output_b)

    # Code to output to IO string vs CSV  
    original_output2(base_output_b, b)
    # Code to output to IO string vs CSV  
    out_io = to_corruptor_write_io_string(\
             from_tdc(\
             test_data_corruptor.corrupt_records(\
             to_corruptor_gf(base_output_b))))