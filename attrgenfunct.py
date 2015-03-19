# Functions that can generate attribute values.
#
# These are functions that can be used in the GenerateFuncAttribute() class
# (see module generator.py). They generate values according to some internal
# functionality.
#
# The requirement of any such functions are:
# 1) that it must return a string
# 2) it can have been 0 and 5 parameters
# 
#
# Examples of such functions are:
# - Australian telephone numbers
# - Japanese telephone numbers
# - Credit card numbers
# - US social security numbers
# - Japanese social security numbers
# - Uniformly distributed age values between 0 and 100
# - Normally distributed age values between 0 and 110
# etc.

# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

import random

import basefunctions, generator

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
  number2 = random.randint(1,9999)

  oz_phone_str = str(area_code)+' '+str(number1).zfill(4)+' '+ \
                 str(number2).zfill(4)
  assert len(oz_phone_str) == 12
  assert oz_phone_str[0] == '0'

  return oz_phone_str

# -----------------------------------------------------------------------------
#
def generate_phone_number_american():
  """Randomly generate an American telephone number made of a three-digit area
     code and an seven-digit number made of two blocks, 3 and 4 digits (with a
     space between). For example: `202 234 5678'
     http://en.wikipedia.org/wiki/List_of_North_American_Numbering_Plan_area_codes
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

# -----------------------------------------------------------------------------
#
def generate_credit_card_number():
  """Randomly generate a credit card made of four four-digit numbers (with a
     space between each number group). For example: '1234 5678 9012 3456'

     For details see: http://en.wikipedia.org/wiki/Bank_card_number
  """

  number1 = random.randint(1,9999)
  assert number1 > 0

  number2 = random.randint(1,9999)
  assert number2 > 0

  number3 = random.randint(1,9999)
  assert number3 > 0

  number4 = random.randint(1,9999)
  assert number4 > 0

  cc_str = str(number1).zfill(4)+' '+str(number2).zfill(4)+' '+ \
           str(number3).zfill(4)+' '+str(number4).zfill(4)

  assert len(cc_str) == 19

  return cc_str

# -----------------------------------------------------------------------------
#
def generate_social_security_number():
  """Randomly generate a social security number. 
     For example: '234 78 9012'
     
     Update to reflect state, date of birth info
     consider: http://www.pnas.org/content/106/27/10975.full.pdf
  """

  number1 = random.randint(1,999)
  assert number1 > 0

  number2 = random.randint(1,99)
  assert number2 > 0

  number3 = random.randint(1,9999)
  assert number3 > 0

  ss_str = str(number1).zfill(3)+' '+str(number2).zfill(2)+' '+ \
           str(number3).zfill(4)

  assert len(ss_str) == 11

  return ss_str

# -----------------------------------------------------------------------------
#
def generate_drivers_license_num():
  # need revision
  # Based on dc format only

  """Randomly generate a drivers license number. 7-digit or 9-digit
     For example: '2512235' or '682019423'
     
     Update to reflect state infor
     consider: http://http://adr-inc.com/PDFs/State_DLFormats.pdf

     According to this paper, DOB info is encoded in drivers license
     We should take this into consideration for further update
     "http://www.highprogrammer.com/alan/numbers/index.html"

  """

  number1 = random.randint(1,9999999)
  assert number1 > 0

  number2 = random.randint(1,999999999)
  assert number2 > 0

  ss_str1 = str(number1).zfill(7)
  assert len(ss_str1) == 7
  
  ss_str2 = str(number2).zfill(9)
  assert len(ss_str1) == 9

  return random.choice([ss_str1, ss_str2])

# -----------------------------------------------------------------------------
#
def generate_passport_num():
  """Randomly generate a us passport number(9-digit number). 
     For example: '203941429'
  """

  number1 = random.randint(1,999999999)
  assert number1 > 0

  passport_str = str(number1).zfill(9)

  assert len(passport_str) == 9

  return passport_str

# -----------------------------------------------------------------------------
#
def generate_email_address(fname="Bohan", lname="Zhang"):
  """Randomly generate a email address
     Update middle name and nickname
     Update frequency table: http://www.ryansolutions.com/blog/2013/email-domains/
  """
  unicode_encoding_used = 'ascii'
  
  basefunctions.check_is_string('fname', fname)
  basefunctions.check_is_string('lname', lname)  

  domain_name = random.choice(["@gmail.com","@hotmail.com","@yahoo.com","@aol.com",
                               "@live.com","@msn.com", "@comcast.com"])
  
  add1 = fname[0] + "." + lname + domain_name
  add2 = fname + "." + lname + domain_name
  add3 = fname[0] + lname + domain_name
  add4 = fname + lname[0] + domain_name
  add5 = fname + domain_name
  
  add = random.choice([add1, add2, add3, add4, add5])
  
  return add


# -----------------------------------------------------------------------------
#
def generate_name_suffix():

  """Randomly generate a name suffix.  Assumes that 10% has a suffix'
  """

  #modify with look-up or full list
  rand = random.random()
  if rand <= 0.10:
    suffix = random.choice(['Jr.', 'Snr.', 'I', 'II', 'III'])
  else:
    suffix = "" 

  return suffix

# -----------------------------------------------------------------------------
#
def generate_gender():
  """Randomly generate a gender."""

  gender = random.choice(['Male', 'Female'])

  return gender

def gender(g):
  'gender'
  return g

# -----------------------------------------------------------------------------


def generate_firstname(gender = 'Female'):
  """randomly generate a name"""
  if gender == 'Female':
    gname = generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_female.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)
  if gender == 'Male':
    gname= generator.GenerateFreqAttribute(attribute_name = 'given-name',
                    freq_file_name = os.path.abspath('lookup_files/firstname_male.csv'),
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used)

    return gname


# -----------------------------------------------------------------------------
#
def generate_name_prefix_m():
  """Randomly generate a name prefix."""

  prefix = random.choice(['Mr', ""])

  return prefix

# -----------------------------------------------------------------------------
#
def generate_name_prefix_f():
  """Randomly generate a name prefix.  
  """
  prefix = random.choice(['Miss', 'Mrs', 'Ms', ""])

  return prefix


# -----------------------------------------------------------------------------
#
def generate_prefix_from_gender(gender):
  """Generate prefix using gender
  Jamie's Test code but not currently used in generate_data_english
  as of 2_8"""
  if gender == "Male":
    prefix = random.choice(['Mr', ""])
  if gender == "Female":
    prefix = random.choice(['Miss', 'Mrs', 'Ms', ""])
  return prefix
#
#-------------------------------------------------------------------------------
  
def generate_nickname():

  """Randomly generate a nickname.  Assumes that 5% has a nickname'
  """
  import random
  
  #modify with look-up or full list
  rand = random.random()
  if rand <= .05:
    nickname = random.choice(['A', 'B', 'C'])
  else:
    nickname = "" 

  return nickname

def race(r):
  'race'
  return r

def hispanic(h):
  'hispanic'
  return h


#-------------------------------------------------------------------------------

# Jamie to add new marital status from Census Bureau distribution

    
#-------------------------------------------------------------------------------
#""" Generate Fake DOB - Need to pass age which isn't working.  See comments below.
#For now I'm passing in a dummy age""" 

def generate_DOB(age=65):

  """Randomly generate a month & date for DOB """
  
  import random
  birth_month = random.randint(1,12)
  if birth_month == "1" or "3" or "5" or "7" or "8" or "10" or "12":
    birth_day = random.randint(1,31)
  if birth_month == "2":
    birth_day = random.randint(1,28)
  else:
    birth_day = random.randint(1,30)
  
  """Can not use the age generator function here for some reason but this code
  worked on generate_data_english.py.  For now, passing dummy age into the function
  to make it work for the time being.  I did input reference to import generator in
  the beginning of the program but got stuck on 'unicode_encoding' 
  
  age = generator.GenerateFreqAlt(attribute_name = 'agejy',
                    freq_file_name = 'lookup_files/age_gender_ratio_female.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used) """

  from time import gmtime, strftime
  year_system = strftime ("%Y", gmtime())
  year_from_age = int(year_system) - age
  DOB = str(birth_month) +'/' + str(birth_day) + '/' + str(year_from_age)
  return DOB
  

# -----------------------------------------------------------------------------

def generate_uniform_value(min_val, max_val, val_type):
  """Randomly generate a numerical value according to a uniform distribution
     between the minimum and maximum values given.

     The value type can be set as 'int', so a string formatted as an integer
     value is returned; or as 'float1' to 'float9', in which case a string
     formatted as floating-point value with the specified number of digits
     behind the comma is returned.

     Note that for certain situations and string formats a value outside the
     set range might be returned. For example, if min_val=100.25 and
     val_type='float1' the rounding can result in a string value '100.2' to
     be returned.

     Suitable minimum and maximum values need to be selected to prevent such a
     situation.
  """

  basefunctions.check_is_number('min_val', min_val)
  basefunctions.check_is_number('max_val', max_val)
  assert min_val < max_val

  r = random.uniform(min_val, max_val)

  return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------
#
def generate_uniform_age(min_val, max_val):
  """Randomly generate an age value (returned as integer) according to a
     uniform distribution between the minimum and maximum values given.

     This function is simple a shorthand for:

       generate_uniform_value(min_val, max_val, 'int')
  """

  assert min_val >= 0
  assert max_val <= 130

  return generate_uniform_value(min_val, max_val, 'int')

# -----------------------------------------------------------------------------

def generate_normal_value(mu, sigma, min_val, max_val, val_type):
  """Randomly generate a numerical value according to a normal distribution
     with the mean (mu) and standard deviation (sigma) given.

     A minimum and maximum allowed value can given as additional parameters,
     if set to None then no minimum and/or maximum limit is set.

     The value type can be set as 'int', so a string formatted as an integer
     value is returned; or as 'float1' to 'float9', in which case a string
     formatted as floating-point value with the specified number of digits
     behind the comma is returned.
  """

  basefunctions.check_is_number('mu', mu)
  basefunctions.check_is_number('sigma', sigma)
  assert sigma > 0.0

  if (min_val != None):
    basefunctions.check_is_number('min_val', min_val)
    assert min_val <= mu

  if (max_val != None):
    basefunctions.check_is_number('max_val', max_val)
    assert max_val >= mu

  if ((min_val != None) and (max_val != None)):
    assert min_val < max_val

  if (min_val != None) or (max_val != None):
    in_range = False  # For testing if the random value is with the range
  else:
    in_range = True

  r = random.normalvariate(mu, sigma)

  while (in_range == False):
    if ((min_val == None) or ((min_val != None) and (r >= min_val))):
      in_range = True

    if ((max_val != None) and (r > max_val)):
      in_range = False

    if (in_range == True):
      r_str = basefunctions.float_to_str(r, val_type)
      r_test = float(r_str)
      if (min_val != None) and (r_test < min_val):
        in_range = False
      if (max_val != None) and (r_test > max_val):
        in_range = False

    if (in_range == False):
      r = random.normalvariate(mu, sigma)

  if (min_val != None):
    assert r >= min_val
  if (max_val != None):
    assert r <= max_val

  return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------
#
def generate_normal_age(mu, sigma, min_val, max_val):
  """Randomly generate an age value (returned as integer) according to a
     normal distribution following the mean and standard deviation values
     given, and limited to age values between (including) the minimum and
     maximum values given.

     This function is simple a shorthand for:

       generate_normal_value(mu, sigma, min_val, max_val, 'int')
  """

  assert min_val >= 0
  assert max_val <= 130

  age = generate_normal_value(mu, sigma, min_val, max_val, 'int')

  while ((int(age) < min_val) or (int(age) > max_val)):
    age = generate_normal_value(mu, sigma, min_val, max_val, 'int')

  return age

def attrgenfunct_log(num_test=10):
  'log for attrgenfunct'

  with open('attrgenfunct_log.txt', 'w') as output:

    output.write( 'Generate %d Australian telephone numbers:' % (num_test))
    for i in range(num_test):
      output.write(' ' + generate_phone_number_australia()+',')
    output.write('\n')

    output.write( 'Generate %d credit card numbers:' % (num_test))
    for i in range(num_test):
      output.write(' '+generate_credit_card_number()+',')
    output.write('\n')

    output.write( 'Generate %d uniformly distributed integer numbers between -100' % \
          (num_test) + ' and -5:')
    for i in range(num_test):
      output.write( ' ' + generate_uniform_value(-100, -5, 'int'),)
    output.write('\n')

    output.write( 'Generate %d uniformly distributed floating-point numbers with ' % \
          (num_test) + '3 digits between -55 and 55:')
    for i in range(num_test):
      output.write( ' ' + generate_uniform_value(-55, 55, 'float3'))
    output.write('\n')

    output.write( 'Generate %d uniformly distributed floating-point numbers with ' % \
          (num_test) + '7 digits between 147 and 9843:')
    for i in range(num_test):
      output.write( ' ' + generate_uniform_value(147, 9843, 'float7'))
    output.write('\n')

    output.write( 'Generate %d uniformly distributed age values between 0 and 120:' % \
          (num_test))
    for i in range(num_test):
      output.write( ' ' + generate_uniform_age(0, 120))
    output.write('\n')

    output.write( 'Generate %d uniformly distributed age values between 18 and 65:' % \
          (num_test))
    for i in range(num_test):
      output.write( ' ' + generate_uniform_age(18, 65))
    output.write('\n')

    output.write( 'Generate %d normally distributed integer numbers between -200' % \
          (num_test) + ' and -3 with mean -50 and standard deviation 44:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_value(-50, 44, -200, -3, 'int'))
    output.write('\n')

    output.write( 'Generate %d normally distributed floating-point numbers with ' % \
          (num_test) + '5 digits between -100 and 100 and with mean 22 and ' + \
          'standard deviation 74:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_value(22, 74, -100, 100, 'float5'))
    output.write('\n')

    output.write( 'Generate %d normally distributed floating-point numbers with ' % \
          (num_test) + '9 digits with mean 22 and standard deviation 74:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_value(22, 74, min_val=None, max_val= None,
                                       val_type='float9'))
    output.write('\n')

    output.write( 'Generate %d normally distributed floating-point numbers with ' % \
          (num_test) + '2 digits with mean 22 and standard deviation 24 that' + \
          ' are larger than 10:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_value(22, 74, min_val=10, max_val=None,
                                       val_type='float2'))
    output.write('\n')

    output.write( 'Generate %d normally distributed floating-point numbers with ' % \
          (num_test) + '4 digits with mean 22 and standard deviation 24 that' + \
          ' are smaller than 30:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_value(22, 74, min_val=None, max_val=40,
                                       val_type='float4'))
    output.write('\n')

    output.write( 'Generate %d normally distributed age values between 0 and 120' % \
          (num_test) + ' with mean 45 and standard deviation 22:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_age(45, 22, 0, 120))
    output.write('\n')

    output.write( 'Generate %d normally distributed age values between 18 and 65' % \
          (num_test) + ' with mean 30 and standard deviation 10:')
    for i in range(num_test):
      output.write( ' ' + generate_normal_age(30, 10, 18, 65))
    

# =============================================================================

# If called from command line perform some examples: Generate values
#
if (__name__ == '__main__'):
    attrgenfunct_log()