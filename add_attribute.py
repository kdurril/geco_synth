#usr/bin/python
# -*- coding: utf-8 -*-
#build for python 2.7

#How to add attributes to GECO


#git pull to update your local files
#test changes locally before pushing to git
#comment when you push to indicate which attributes you've added

#on attrgenfunct.py 
#start by creating a generating function
#make function names descriptive
#update document strings, describe functionality
#add a "modify" comment such as "modify with look-up or full list"
#if the function will need additional revision 

#on generate_data_english.py
#add an attribute variable to 
#add attribute_name to list attr_name_list
#add variable to attr_data_list
#check to see if you have updated variable names if copying
#if corrupting: add attribute_name to attr_mod_prob_dictionary
#if corrupting: add attribute_name to attr_mod_data_dictionary

#test from command line  with import generate_data_english
#I use iPython or iPython notebook for quick review 

#Simple attribute

#Create a generating function in attrgenfunct.py
#Compare generate_phone_number_australia
#                  to
#        generate_phone_number_american
# -----------------------------------------------------------------------------
#
def generate_phone_number_australia():
  """Randomly generate an Australian telephone number made of a two-digit area
     code and an eight-digit number made of two blocks of four digits (with a
     space between). For example: `02 1234 5678'

     For details see: http://en.wikipedia.org/wiki/ \
                      Telephone_numbers_in_Australia#Personal_numbers_.2805.29
  """
  
  area_code = random.choice(['02', '03', '04', '07', '08'])

  number1 = random.randint(1,9999)
  number2 = random.randint(1,999)

  oz_phone_str = str(area_code)+' '+str(number1).zfill(4)+' '+ \
                 str(number2).zfill(3)
  assert len(oz_phone_str) == 11
  assert oz_phone_str[0] == '0'

  return oz_phone_str


# -----------------------------------------------------------------------------
#
def generate_phone_number_american():
  """Randomly generate an American telephone number made of a three-digit area
     code and an seven-digit number made of two blocks, 3 and 4 digits (with a
     space between). For example: `202 234 5678'
  """
  #modify with look-up or full list
  area_code = random.choice(['202', '212', '215', '412', '812'])
  number1 = random.randint(1,999)
  number2 = random.randint(1,9999)
  
  #.zfill will pad zeros to the left of digits, 1 become 001 w/ zfill(3)
  us_phone_str = str(area_code)+' '+str(number1).zfill(3)+' '+ \
                 str(number2).zfill(4)
  assert len(us_phone_str) == 12
  

  return us_phone_str

#The following is from generate_data_english.py
#Cell
phone_num_cell_attr = \
    generator.GenerateFuncAttribute(attribute_name = 'cell-number',
                       function = attrgenfunct.generate_phone_number_american)

#Update attr_name_list & attr_data_list
#add attribute_name
#Generating attr_name_list by calling attribribute name on the object
# is prefered to manually creating the attr_name_list 
#after creating attr_data_list
# create attr_name_list = [attr.attribute_name for attr in attr_data_list]
# or 
# use a dict comprehension with 
# attr_dict = dict((attr.attribute_name, attr.create_attribute_value()) for attr in attr_data_list)
# or 
# use a OrderedDict to preserve order for human readability
attr_name_list = ['gender', 'given-name', 'surname', 'postcode', 'city',
                  'cell-number', 'work-number', 'home-number', 
                  'social-security', 'credit-card-number', 
                  'income-normal', 'age-uniform', 
                  'income', 'age', 'sex']

#variable name such as phone_num_cell_attr
attr_data_list = [gname_attr, sname_attr, postcode_attr, 
                  phone_num_cell_attr, phone_num_work_attr,
                  phone_num_home_attr, social_security_attr,
                  credit_card_attr, age_uniform_attr, income_normal_attr,
                  gender_city_comp_attr, sex_income_comp_attr,
                  gender_town_salary_comp_attr, 
                  age_salary_comp_attr, age_blood_pressure_comp_attr]


#if corrupting
#Update attr_mod_prob_dictionary
#       attr_mod_data_dictionary
attr_mod_prob_dictionary = {'gender':0.1, 'given-name':0.2,'surname':0.2,
                            'postcode':0.1,'city':0.1, 'cell-number':0.15,
                            'credit-card-number':0.1,'age':0.05}

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
                            'cell-number':[(1.0, missing_val_corruptor)],
                            'credit-card-number':[(1.0, edit_corruptor)]}

#Look-up table attribute

#
