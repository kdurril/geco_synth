










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


# -----------------------------------------------------------------------------
class DependentFunc(object):

  __init__(self, **kwargs):
    self.gname = None
    self.sname = None
    self.dob = None
    self.nickname = None
    self.gender = None
    self.postcode = None
    self.city = None

    self.email = None
    
    self.prefix = None
    self.suffix = None
    self.drivers = None
    self.passport = None
    self.phone_home = None
    self.phone_cell = None
    self.phone_work = None
    self.ss = None
    self.credit_card = None

    self.race = None
    self.hispanic = None
    

  attr_name_list = ['gender', 'name-prefix', 'given-name', 'middle-name', 'surname', 'name-suffix', 'postcode', 'city',
                  'previous-surname', 'nickname', 'cell-number', 'work-number', 'home-number',  
                  'social-security-number', 'credit-card-number', 
                  'income-normal', 'age-uniform', 'income', 
                  'age', 'sex', 'blood-pressure', 'passport-number',
                  'email', 'race-hispanic', 'age-new', 'DOB']

  self.unicode_encoding_used = 'ascii'
  self.sname_attr = \
  generator.GenerateFreqAttribute(attribute_name = 'surname',
                          freq_file_name = 'lookup-files/surname-freq.csv',
                          has_header_line = False,
                          unicode_encoding = unicode_encoding_used)

  self.gname_attr = \
    generator.GenerateFreqAttribute(attribute_name = 'given-name',
                          freq_file_name = 'lookup-files/givenname_f_freq.csv',
                          has_header_line = False,
                          unicode_encoding = unicode_encoding_used)


  def generate_DOB(self, age=65):

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
                    freq_file_name = 'lookup-files/age_gender_ratio_female.csv',
                    has_header_line = False,
                    unicode_encoding = unicode_encoding_used) """

  from time import gmtime, strftime
  year_system = strftime ("%Y", gmtime())
  year_from_age = int(year_system) - age
  DOB = str(birth_month) +'/' + str(birth_day) + '/' + str(year_from_age)
  return DOB

  # -----------------------------------------------------------------------------
#
def generate_phone_number_american(self):
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
def generate_credit_card_number(self):
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
def generate_social_security_number(self):
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
def generate_drivers_license_num(self):
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
def generate_passport_num(self):
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
def generate_email_address(self, fname="Bohan", lname="Zhang"):
  """Randomly generate a email address
     Update middle name and nickname
     Update frequency table: http://www.ryansolutions.com/blog/2013/email-domains/
  """
  

  lname = str(sname_attr.create_attribute_value())
  fname = str(gname_attr.create_attribute_value())

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
def generate_name_suffix(self):

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
def generate_name_prefix_m(self, gender="M"):
	"""Randomly generate a name prefix.  
  """
  	prefix = random.choice(['Mr', ""])

  	return prefix

# -----------------------------------------------------------------------------
#
def generate_name_prefix_f(self, gender="F"):
	"""Randomly generate a name prefix.  
  """
  	prefix = random.choice(['Miss', 'Mrs', 'Ms', ""])

  	return prefix


# -----------------------------------------------------------------------------
#
def generate_prefix_from_gender(self, gender=None):
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
  
def generate_nickname(self, fname=None):

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