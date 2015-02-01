# corrupter.py - Python module to corrupt (modify) generate synthetic data.
#
#                Part of a flexible data generation system.
#
# Peter Christen and Dinusha Vatsalan,  January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

"""Module containing several classes to corrupt synthetic data according to
   user specification.
"""

# -----------------------------------------------------------------------------
# Import necessary modules

import math
import random

import basefunctions

# =============================================================================
# Helper functions to randomly select a position for where to apply a
# modification

def position_mod_uniform(in_str):
  """Select any position in the given input string with uniform likelihood.

     Return 0 is the string is empty.
  """

  if (in_str == ''):  # Empty input string
    return 0

  max_pos = len(in_str)-1

  pos = random.randint(0, max_pos)  # String positions start at 0

  return pos

# -----------------------------------------------------------------------------

def position_mod_normal(in_str):
  """Select any position in the given input string with normally distributed
     likelihood where the average of the normal distribution is set to one
     character behind the middle of the string, and the standard deviation is
     set to 1/4 of the string length.

     This is based on studies on the distribution of errors in real text which
     showed that errors such as typographical mistakes are more likely to
     appear towards the middle and end of a string but not at the beginning.

     Return 0 is the string is empty.
  """

  if (in_str == ''):  # Empty input string
    return 0

  str_len = len(in_str)

  mid_pos = str_len / 2.0 + 1
  std_dev = str_len / 4.0
  max_pos = str_len - 1

  pos = int(round(random.gauss(mid_pos, std_dev)))
  while ((pos < 0) or (pos > max_pos)):
    pos = int(round(random.gauss(mid_pos, std_dev)))

  return pos

# =============================================================================
# Classes for corrupting a value in a single attribute (field) of the data set
# =============================================================================

class CorruptValue:
  """Base class for the definition of corruptor that is applied on a single
     attribute (field) in the data set.

     This class and all of its derived classes provide methods that allow the
     definition of how values in a single attribute are corrupted (modified)
     and the parameters necessary for the corruption process.

     The following variables need to be set when a CorruptValue instance is
     initialised (with further parameters listed in the derived classes):

     position_function  A function that (somehow) determines the location
                        within a string value of where a modification
                        (corruption) is to be applied. The input of this
                        function is assumed to be a string and its return value
                        an integer number in the range of the length of the
                        given input string.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, base_kwargs):
    """Constructor, set general attributes.
    """

    # General attributes for all attribute corruptors.
    #
    self.position_function = None

    # Process the keyword argument (all keywords specific to a certain data
    # generator type were processed in the derived class constructor)
    #
    for (keyword, value) in base_kwargs.items():

      if (keyword.startswith('position')):
        basefunctions.check_is_function_or_method('position_function', value)
        self.position_function = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    basefunctions.check_is_function_or_method('position_function',
                                              self.position_function)

    # Check if the position function does return an integer value
    #
    pos = self.position_function('test')
    if ((not isinstance(pos, int)) or (pos < 0) or (pos > 3)):
      raise Exception, 'Position function returns an illegal value (either' + \
                       'not an integer or and integer out of range: %s' % \
                       (str(pos))

  # ---------------------------------------------------------------------------

  def corrupt_value(self, str):
    """Method which corrupts the given input string and returns the modified
       string.
       See implementations in derived classes for details.
    """

    raise Exception, 'Override abstract method in derived class'

# =============================================================================

class CorruptMissingValue(CorruptValue):
  """A corruptor method which simply sets an attribute value to a missing
     value.

     The additional argument (besides the base class argument
     'position_function') that has to be set when this attribute type is
     initialised are:

     missing_val  The string which designates a missing value. Default value
                  is the empty string ''.

     Note that the 'position_function' is not required by this corruptor
     method.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.missing_val = ''
    self.name =        'Missing value'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('miss')):
        basefunctions.check_is_string('missing_val', value)
        self.missing_val = value

      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Simply return the missing value string.
    """

    return self.missing_val

# =============================================================================

class CorruptValueEdit(CorruptValue):
  """A simple corruptor which applies one edit operation on the given value.

     Depending upon the content of the value (letters, digits or mixed), if the
     edit operation is an insert or substitution a character from the same set
     (letters, digits or both) is selected.

     The additional arguments (besides the base class argument
     'position_function') that has to be set when this attribute type is
     initialised are:

     char_set_funct   A function which determines the set of characters that
                      can be inserted or used of substitution
     insert_prob      These for values set the likelihood of which edit
     delete_prob      operation will be selected.
     substitute_prob  All four probability values must be between 0 and 1, and
     transpose_prob   the sum of these four values must be 1.0
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.char_set_funct =  None
    self.insert_prob =     None
    self.delete_prob =     None
    self.substitute_prob = None
    self.transpose_prob =  None
    self.name =            'Edit operation'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('char')):
        basefunctions.check_is_function_or_method('char_set_funct', value)
        self.char_set_funct = value

      elif (keyword.startswith('ins')):
        basefunctions.check_is_normalised('insert_prob', value)
        self.insert_prob = value

      elif (keyword.startswith('del')):
        basefunctions.check_is_normalised('delete_prob', value)
        self.delete_prob = value

      elif (keyword.startswith('sub')):
        basefunctions.check_is_normalised('substitute_prob', value)
        self.substitute_prob = value

      elif (keyword.startswith('tran')):
        basefunctions.check_is_normalised('transpose_prob', value)
        self.transpose_prob = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_function_or_method('char_set_funct',
                                              self.char_set_funct)
    basefunctions.check_is_normalised('insert_prob',     self.insert_prob)
    basefunctions.check_is_normalised('delete_prob',     self.delete_prob)
    basefunctions.check_is_normalised('substitute_prob', self.substitute_prob)
    basefunctions.check_is_normalised('transpose_prob',  self.transpose_prob)

    # Check if the character set function returns a string
    #
    test_str = self.char_set_funct('test')   # This might become a problem
    basefunctions.check_is_string_or_unicode_string('test_str', test_str)

    if (abs((self.insert_prob + self.delete_prob + self.substitute_prob + \
         self.transpose_prob) - 1.0) > 0.0000001):
      raise Exception, 'The four edit probabilities do not sum to 1.0'

    # Calculate the probability ranges for the four edit operations
    #
    self.insert_range =     [0.0,self.insert_prob]
    self.delete_range =     [self.insert_range[1],
                             self.insert_range[1] + self.delete_prob]
    self.substitute_range = [self.delete_range[1],
                             self.delete_range[1] + self.substitute_prob]
    self.transpose_range =  [self.substitute_range[1],
                             self.substitute_range[1] + self.transpose_prob]
    assert self.transpose_range[1] == 1.0

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    # Randomly select an edit operation
    #
    r = random.random()

    if (r < self.insert_range[1]):
      edit_op = 'ins'
    elif ((r >= self.delete_range[0]) and (r < self.delete_range[1])):
      edit_op = 'del'
    elif ((r >= self.substitute_range[0]) and (r < self.substitute_range[1])):
      edit_op = 'sub'
    else:
      edit_op = 'tra'

    # Do some checks if only a valid edit operations was selected
    #
    if (edit_op == 'ins'):
      assert self.insert_prob > 0.0
    elif (edit_op == 'del'):
      assert self.delete_prob > 0.0
    elif (edit_op == 'sub'):
      assert self.substitute_prob > 0.0
    else:
      assert self.transpose_prob > 0.0

    # If the input string is empty only insert is possible
    #
    if ((len(in_str) == 0) and (edit_op != 'ins')):
      return in_str  # Return input string without modification

    # If the input string only has one character then transposition is not
    # possible
    #
    if ((len(in_str) == 1) and (edit_op == 'tra')):
      return in_str  # Return input string without modification

    # Position in string where to apply the modification
    #
    # For a transposition we cannot select the last position in the string
    # while for an insert we can specify the position after the last
    if (edit_op == 'tra'):
      len_in_str = in_str[:-1]
    elif (edit_op == 'ins'):
      len_in_str = in_str+'x'
    else:
      len_in_str = in_str
    mod_pos = self.position_function(len_in_str)

    # Get the set of possible characters that can be inserted or substituted
    #
    char_set = self.char_set_funct(in_str)

    if (char_set == ''):  # No possible value change
      return in_str

    if (edit_op == 'ins'):  # Insert a character
      ins_char = random.choice(char_set)
      new_str = in_str[:mod_pos] + ins_char + in_str[mod_pos:]

    elif (edit_op == 'del'):  # Delete a character
      new_str = in_str[:mod_pos] + in_str[mod_pos+1:]

    elif (edit_op == 'sub'):  # Substitute a character
      sub_char = random.choice(char_set)
      new_str = in_str[:mod_pos] + sub_char + in_str[mod_pos+1:]

    else:  # Transpose two characters
      char1 = in_str[mod_pos]
      char2 = in_str[mod_pos+1]
      new_str = in_str[:mod_pos]+char2+char1+in_str[mod_pos+2:]

    return new_str

# =============================================================================

class CorruptValueKeyboard(CorruptValue):
  """Use a keyboard layout to simulate typing errors. They keyboard is
     hard-coded into this method, but can be changed easily for different
     keyboard layout.

     A character from the original input string will be randomly chosen using
     the position function, and then a character from either the same row or
     column in the keyboard will be selected.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     row_prob  The probability that a neighbouring character in the same row
               is selected.

     col_prob  The probability that a neighbouring character in the same
               column is selected.

     The sum of row_prob and col_prob must be 1.0.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.row_prob = None
    self.col_prob = None
    self.name =     'Keybord value'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('row')):
        basefunctions.check_is_normalised('row_prob', value)
        self.row_prob = value

      elif (keyword.startswith('col')):
        basefunctions.check_is_normalised('col_prob', value)
        self.col_prob = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_normalised('row_prob', self.row_prob)
    basefunctions.check_is_normalised('col_prob', self.col_prob)

    if (abs((self.row_prob + self.col_prob) - 1.0) > 0.0000001):
      raise Exception, 'Sum of row and column probablities does not sum ' + \
                       'to 1.0'

    # Keyboard substitutions gives two dictionaries with the neigbouring keys
    # for all leters both for rows and columns (based on ideas implemented by
    # Mauricio A. Hernandez in his dbgen).
    # This following data structures assume a QWERTY keyboard layout
    #
    self.rows = {'a':'s',  'b':'vn', 'c':'xv', 'd':'sf', 'e':'wr', 'f':'dg',
                 'g':'fh', 'h':'gj', 'i':'uo', 'j':'hk', 'k':'jl', 'l':'k',
                 'm':'n',  'n':'bm', 'o':'ip', 'p':'o',  'q':'w',  'r':'et',
                 's':'ad', 't':'ry', 'u':'yi', 'v':'cb', 'w':'qe', 'x':'zc',
                 'y':'tu', 'z':'x',
                 '1':'2',  '2':'13', '3':'24', '4':'35', '5':'46', '6':'57',
                 '7':'68', '8':'79', '9':'80', '0':'9'}

    self.cols = {'a':'qzw', 'b':'gh',  'c':'df', 'd':'erc','e':'ds34',
                 'f':'rvc', 'g':'tbv', 'h':'ybn', 'i':'k89',  'j':'umn',
                 'k':'im', 'l':'o', 'm':'jk',  'n':'hj',  'o':'l90', 'p':'0',
                 'q':'a12', 'r':'f45', 's':'wxz', 't':'g56',  'u':'j78',
                 'v':'fg', 'w':'s23',  'x':'sd', 'y':'h67',  'z':'as',
                 '1':'q',  '2':'qw', '3':'we', '4':'er', '5':'rt',  '6':'ty',
                 '7':'yu', '8':'ui', '9':'io', '0':'op'}

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by replacing a single
       character with a neighbouring character given the defined keyboard
       layout at a position randomly selected by the position function.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    max_try = 10  # Maximum number of tries to find a keyboard modification at
                  # a randomly selected position

    done_key_mod = False  # A flag, set to true once a modification is done
    try_num =      0

    mod_str = in_str[:]  # Make a copy of the string which will be modified

    while ((done_key_mod == False) and (try_num < max_try)):

      mod_pos =  self.position_function(mod_str)
      mod_char = mod_str[mod_pos]

      r = random.random()  # Create a random number between 0 and 1

      if (r <= self.row_prob):  # See if there is a row modification
        if (mod_char in self.rows):
          key_mod_chars = self.rows[mod_char]
          done_key_mod =  True

      else:  # See if there is a column modification
        if (mod_char in self.cols):
          key_mod_chars = self.cols[mod_char]
          done_key_mod =  True

      if (done_key_mod == False):
        try_num += 1

    # If a modification is possible do it
    #
    if (done_key_mod == True):

      # Randomly select one of the possible characters
      #
      new_char = random.choice(key_mod_chars)

      mod_str = mod_str[:mod_pos] + new_char + mod_str[mod_pos+1:]

    assert len(mod_str) == len(in_str)

    return mod_str

# =============================================================================

class CorruptValueOCR(CorruptValue):
  """Simulate OCR errors using a list of similar pairs of characters or strings
     that will be applied on the original string values.

     These pairs of characters will be loaded from a look-up file which is a
     CSV file with two columns, the first is a single character or character
     sequence, and the second column is also a single character or character
     sequence. It is assumed that the second value is an OCR modification of
     the first value, and the other way round. For example:

       5,S
       5,s
       2,Z
       2,z
       1,|
       6,G

     It is possible for an 'original' string value (first column) to have
     several variations (second column). In such a case one variation will be
     randomly selected during the value corruption (modification) process.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the OCR character
                       variations.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the look-up file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.lookup_file_name = None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.ocr_val_dict =     {}  # The dictionary to hold the OCR variations
    self.name =             'OCR value'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the OCR variations lookup file - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    # Process values from file and their frequencies
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) != 2):
        raise Exception, 'Illegal format in OCR variations lookup file ' + \
                         '%s: %s' % (self.lookup_file_name, str(rec_list))
      org_val = rec_list[0].strip()
      var_val = rec_list[1].strip()

      if (org_val == ''):
        raise Exception, 'Empty original OCR value in lookup file %s' % \
                         (self.lookup_file_name)
      if (var_val == ''):
        raise Exception, 'Empty OCR variation value in lookup file %s' % \
                         (self.lookup_file_name)
      if (org_val == var_val):
        raise Exception, 'OCR variation is the same as original value in ' + \
                         'lookup file %s' % (self.lookup_file_name)

      # Now insert the OCR original value and variation twice (with original
      # and variation both as key and value), i.e. swapped
      #
      this_org_val_list = self.ocr_val_dict.get(org_val, [])
      this_org_val_list.append(var_val)
      self.ocr_val_dict[org_val] = this_org_val_list

      this_org_val_list = self.ocr_val_dict.get(var_val, [])
      this_org_val_list.append(org_val)
      self.ocr_val_dict[var_val] = this_org_val_list

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by replacing a single
       character or a sequence of characters with an OCR variation at a
       position randomly selected by the position function.

       If there are several OCR variations then one will be randomly chosen.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    max_try = 10  # Maximum number of tries to find an OCR modification at a
                  # randomly selected position

    done_ocr_mod = False  # A flag, set to True once a modification is done
    try_num =      0

    mod_str = in_str[:]  # Make a copy of the string which will be modified

    while ((done_ocr_mod == False) and (try_num < max_try)):

      mod_pos = self.position_function(mod_str)

      # Try one to three characters at selected position
      #
      ocr_org_char_set = set([mod_str[mod_pos], mod_str[mod_pos:mod_pos+2], \
                              mod_str[mod_pos:mod_pos+3]])

      mod_options = []  # List of possible modifications that can be applied

      for ocr_org_char in ocr_org_char_set:
        if ocr_org_char in self.ocr_val_dict:
          ocr_var_list = self.ocr_val_dict[ocr_org_char]
          for mod_val in ocr_var_list:
            mod_options.append([ocr_org_char,len(ocr_org_char),mod_val])

      if (mod_options != []):  # Modifications are possible

        # Randomly select one of the possible modifications that can be applied
        #
        mod_to_apply = random.choice(mod_options)
        assert mod_to_apply[0] in self.ocr_val_dict.keys()
        assert mod_to_apply[2] in self.ocr_val_dict.keys()

        mod_str = in_str[:mod_pos] + mod_to_apply[2] + \
                  in_str[mod_pos+mod_to_apply[1]:]

        done_ocr_mod = True

      else:
        try_num += 1

    return mod_str

# =============================================================================

class CorruptValuePhonetic(CorruptValue):
  """Simulate phonetic errors using a list of phonetic rules which are stored
     in a CSV look-up file.

     Each line (row) in the CSV file must consist of seven columns that contain
     the following information:
     1) Where a phonetic modification can be applied. Possible values are:
        'ALL','START','END','MIDDLE'
     2) The original character sequence (i.e. the characters to be replaced)
     3) The new character sequence (which will replace the original sequence)
     4) Precondition: A condition that must occur before the original string
        character sequence in order for this rule to become applicable.
     5) Postcondition: Similarly, a condition that must occur after the
        original string character sequence in order for this rule to become
        applicable.
     6) Pattern existence condition: This condition requires that a certain
        given string character sequence does ('y' flag) or does not ('n' flag)
        occur in the input string.
     7) Start existence condition: Similarly, this condition requires that the
        input string starts with a certain string pattern ('y' flag) or not
        ('n' flag)

     A detailed description of this phonetic data generation is available in

       Accurate Synthetic Generation of Realistic Personal Information
       Peter Christen and Agus Pudjijono
       Proceedings of the Pacific-Asia Conference on Knowledge Discovery and
                          Data Mining (PAKDD), Bangkok, Thailand, April 2009. 

     For a given input string, one of the possible phonetic modifications will
     be randomly selected without the use of the position function.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the phonetic
                       modification patterns.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the look-up file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.

     Note that the 'position_function' is not required by this corruptor
     method.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.lookup_file_name = None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.replace_table =    []
    self.name =             'Phonetic value'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the misspelling lookup file - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    # Process values from file and misspellings
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) != 7):
        raise Exception, 'Illegal format in phonetic lookup file %s: %s' \
                         % (self.lookup_file_name, str(rec_list))
      val_tuple = ()
      for val in rec_list:
        if (val != ''):
          val = val.strip()
          val_tuple += val,
        else:
          raise Exception, 'Empty value in phonetic lookup file %s" %s' % \
                           (self.lookup_file_name, str(rec_list))
      self.replace_table.append(val_tuple)

  # ---------------------------------------------------------------------------

  def __apply_change__(self, in_str, ch):
    """Helper function which will apply the selected change to the input
       string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    work_str = in_str
    list_ch = ch.split('>')
    subs = list_ch[1]
    if (list_ch[1] == '@'): # @ is blank
      subs = ''
    tmp_str = work_str
    org_pat_length = len(list_ch[0])
    str_length =     len(work_str)

    if (list_ch[2] == 'end'):
      org_pat_start = work_str.find(list_ch[0], str_length-org_pat_length)
    elif (list_ch[2] == 'middle'):
      org_pat_start = work_str.find(list_ch[0],1)
    else: # Start and all 
      org_pat_start = work_str.find(list_ch[0],0)
 
    if (org_pat_start == 0):
      work_str = subs + work_str[org_pat_length:] 
    elif (org_pat_start > 0):
      work_str = work_str[:org_pat_start] + subs + \
                 work_str[org_pat_start+org_pat_length:]
 
    if (work_str == tmp_str):
      work_str = str_to_change

    return work_str

  # ---------------------------------------------------------------------------

  def __slavo_germanic__(self, in_str):
    """Helper function which determines if the inputstring could contain a
       Slavo or Germanic name.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if ((in_str.find('w') > -1) or (in_str.find('k') > -1) or \
        (in_str.find('cz') > -1) or (in_str.find('witz') > -1)):
      return 1
    else:
      return 0

  # ---------------------------------------------------------------------------

  def __collect_replacement__(self, s, where, orgpat, newpat, precond,
                              postcond, existcond, startcond):
    """Helper function which collects all the possible phonetic modification
       patterns that are possible on the given input string, and replaces a
       pattern in a string.

       The following arguments are needed:
       - where     Can be one of: 'ALL','START','END','MIDDLE'
       - precond   Pre-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant
       - postcond  Post-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant
 
       Developed by Agus Pudjijono, ANU, 2008.
    """

    vowels = 'aeiouy'   
    tmpstr = s
    changesstr = ''

    start_search = 0  # Position from where to start the search
    pat_len =      len(orgpat)
    stop =         False

    # As long as pattern is in string
    #
    while ((orgpat in tmpstr[start_search:]) and (stop == False)):

      pat_start = tmpstr.find(orgpat, start_search)
      str_len =   len(tmpstr)

      # Check conditions of previous and following character
      #
      OKpre  = False   # Previous character condition
      OKpre1 = False   # Previous character1 condition
      OKpre2 = False   # Previous character2 condition

      OKpost  = False  # Following character condition
      OKpost1 = False  # Following character1 condition
      OKpost2 = False  # Following character2 condition

      OKexist = False  # Existing pattern condition
      OKstart = False  # Existing start pattern condition

      index =  0

      if (precond == 'None'):
        OKpre = True

      elif (pat_start > 0):
        if (((precond == 'V') and (tmpstr[pat_start-1] in vowels)) or \
            ((precond == 'C') and (tmpstr[pat_start-1] not in vowels))):
          OKpre = True

        elif ((precond.find(';')) > -1):
          if (precond.find('|') > -1):    
            rls=precond.split('|')
            rl1=rls[0].split(';')             

            if (int(rl1[1]) < 0): 
              index =  pat_start+int(rl1[1])
            else:           
              index =  pat_start+(len(orgpat)-1)+int(rl1[1]) 

            i=2
            if (rl1[0] == 'n'):
              while (i < (len(rl1))):
                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                  OKpre1 = False
                  break
                else:
                  OKpre1 = True
                i+=1
            else:
              while (i < (len(rl1))):
                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                  OKpre1 = True 
                  break  
                i+=1

            rl2=rls[1].split(';')

            if (int(rl2[1]) < 0): 
              index =  pat_start+int(rl2[1])
            else:           
              index =  pat_start+(len(orgpat)-1)+int(rl2[1]) 

            i=2
            if (rl2[0] == 'n'):
              while (i < (len(rl2))):
                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                  OKpre2 = False
                  break
                else:
                  OKpre2 = True
                i+=1
            else:
              while (i < (len(rl2))):
                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                  OKpre2 = True 
                  break  
                i+=1

            OKpre=OKpre1 and OKpre2 

          else:          
            rl=precond.split(';')
            #-
            if (int(rl[1]) < 0): 
              index =  pat_start+int(rl[1])
            else:           
              index =  pat_start+(len(orgpat)-1)+int(rl[1]) 

            i=2
            if (rl[0] == 'n'):
              while (i < (len(rl))):  
                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                  OKpre = False  
                  break
                else:
                  OKpre = True
                i+=1
            else:
              while (i < (len(rl))):
                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                  OKpre = True 
                  break  
                i+=1

      if (postcond == 'None'):
        OKpost = True

      else:
        pat_end = pat_start+pat_len
          
        if (pat_end < str_len):
          if (((postcond == 'V') and (tmpstr[pat_end] in vowels)) or \
              ((postcond == 'C') and (tmpstr[pat_end] not in vowels))):
            OKpost = True
          elif ((postcond.find(';')) > -1):            
            if (postcond.find('|') > -1):    
              rls=postcond.split('|')

              rl1=rls[0].split(';')             

              if (int(rl1[1]) < 0): 
                index =  pat_start+int(rl1[1])
              else:           
                index =  pat_start+(len(orgpat)-1)+int(rl1[1]) 

              i=2
              if (rl1[0] == 'n'):
                while (i < (len(rl1))):
                  if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                    OKpost1 = False
                    break
                  else:
                    OKpost1 = True
                  i+=1
              else:
                while (i < (len(rl1))):
                  if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                    OKpost1 = True 
                    break  
                  i+=1
  
              rl2=rls[1].split(';')

              if (int(rl2[1]) < 0): 
                index =  pat_start+int(rl2[1])
              else:           
                index =  pat_start+(len(orgpat)-1)+int(rl2[1]) 

              i=2
              if (rl2[0] == 'n'):
                while (i < (len(rl2))):
                  if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                    OKpost2 = False
                    break
                  else:
                    OKpost2 = True
                  i+=1
              else:
                while (i < (len(rl2))):
                  if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                    OKpost2 = True 
                    break  
                  i+=1

              OKpost=OKpost1 and OKpost2  

            else:          
              rl=postcond.split(';')

              if (int(rl[1]) < 0): 
                index =  pat_start+int(rl[1])
              else:           
                index =  pat_start+(len(orgpat)-1)+int(rl[1]) 

              i=2
              if (rl[0] == 'n'):
                while (i < (len(rl))):  
                  if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                    OKpost = False
                    break
                  else:
                    OKpost = True
                  i+=1
              else:
                while (i < (len(rl))):
                  if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                    OKpost = True 
                    break  
                  i+=1

      if (existcond == 'None'):
        OKexist = True

      else:
        rl=existcond.split(';')
        if (rl[1] == 'slavo'):
          r=self.__slavo_germanic__(s)
          if (rl[0] == 'n'): 
            if (r == 0):
              OKexist=True
          else:
            if (r == 1):
              OKexist=True
        else:
          i=1
          if (rl[0] == 'n'):
            while (i < (len(rl))):
              if (s.find(rl[i]) > -1):
                OKexist = False
                break
              else:
                OKexist = True
              i+=i
          else:
            while (i < (len(rl))):
              if (s.find(rl[i]) > -1):
                OKexist = True 
                break  
              i+=i

      if (startcond == 'None'):
        OKstart = True

      else:
        rl=startcond.split(';')
        i=1  
        if (rl[0] == 'n'):
          while (i < (len(rl))):
            if (s.find(rl[i]) > -1):
              OKstart = False
              break
            else:
              OKstart = True
            i+=i
        else:
          while (i < (len(rl))):
            if (s.find(rl[i]) == 0):
              OKstart = True 
              break  
            i+=i

      # Replace pattern if conditions and position OK
      #
      if ((OKpre == True) and (OKpost == True) and (OKexist == True) and \
          (OKstart == True)) and (((where == 'START') and (pat_start == 0)) \
          or ((where == 'MIDDLE') and (pat_start > 0) and \
          (pat_start+pat_len < str_len)) or ((where == 'END') and \
          (pat_start+pat_len == str_len)) or (where == 'ALL')):
        tmpstr = tmpstr[:pat_start]+newpat+tmpstr[pat_start+pat_len:]
        changesstr += ',' +orgpat + '>' + newpat + '>' + where.lower()
        start_search = pat_start + len(newpat)

      else:
        start_search = pat_start+1

      if (start_search >= (len(tmpstr)-1)): 
        stop = True

    tmpstr += changesstr

    return tmpstr 

  # ---------------------------------------------------------------------------

  def __get_transformation__(self, in_str):
    """Helper function which generates the list of possible phonetic
       modifications for the given input string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if (in_str == ''):
      return in_str

    changesstr2 = ''

    workstr = in_str

    for rtpl in self.replace_table:  # Check all transformations in the table
      if (len(rtpl) == 3):
         rtpl += ('None','None','None','None')

      workstr = self.__collect_replacement__(in_str,rtpl[0],rtpl[1],rtpl[2],
                                             rtpl[3],rtpl[4],rtpl[5],rtpl[6])
      if (workstr.find(',') > -1):
        tmpstr = workstr.split(',')
        workstr = tmpstr[0]    
        if (changesstr2.find(tmpstr[1]) == -1): 
          changesstr2 += tmpstr[1]+';'
    workstr += ',' + changesstr2

    return workstr

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by applying a phonetic
       modification.

       If several such modifications are possible then one will be randomly
       selected.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    # Get the possible phonetic modifications for this input string
    #
    phonetic_changes = self.__get_transformation__(in_str)

    mod_str = in_str

    if (',' in phonetic_changes):  # Several modifications possible
      tmp_str = phonetic_changes.split(',')
      pc = tmp_str[1][:-1] # Remove the last ';'
      list_pc = pc.split(';')
      change_op = random.choice(list_pc)
      if (change_op != ''):
        mod_str = self.__apply_change__(in_str, change_op)
        #print in_str, mod_str, change_op

    return mod_str

# =============================================================================

class CorruptCategoricalValue(CorruptValue):
  """Replace a categorical value with another categorical value from the same
     look-up file.

     This corruptor can be used to modify attribute values with known
     misspellings.

     The look-up file is a CSV file with two columns, the first is a
     categorical value that is expected to be in an attribute in an original
     record, and the second is a variation of this categorical value.

     It is possible for an 'original' categorical value (first column) to have
     several misspelling variations (second column). In such a case one
     misspelling will be randomly selected.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the categorical values
                       and their misspellings.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the look-up file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.

     Note that the 'position_function' is not required by this corruptor
     method.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.lookup_file_name = None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.misspell_dict =    {}  # The dictionary to hold the misspellings
    self.name =             'Categorial value'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the misspelling lookup file - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    # Process values from file and misspellings
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) != 2):
        raise Exception, 'Illegal format in misspellings lookup file %s: %s' \
                         % (self.lookup_file_name, str(rec_list))

      org_val =  rec_list[0].strip()
      if (org_val == ''):
        raise Exception, 'Empty original attribute value in lookup file %s' % \
                         (self.lookup_file_name)
      misspell_val = rec_list[1].strip()
      if (misspell_val == ''):
        raise Exception, 'Empty misspelled attribute value in lookup ' + \
                         'file %s' % (self.lookup_file_name)
      if (org_val == misspell_val):
        raise Exception, 'Misspelled value is the same as original value' + \
                         ' in lookup file %s' % (self.lookup_file_name)

      this_org_val_list = self.misspell_dict.get(org_val, [])
      this_org_val_list.append(misspell_val)
      self.misspell_dict[org_val] = this_org_val_list

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and replaces it with a
       misspelling, if there is a known misspelling for the given original
       value.

       If there are several known misspellings for the given original value
       then one will be randomly selected.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    if (in_str not in self.misspell_dict):  # No misspelling for this value
      return in_str

    misspell_list = self.misspell_dict[in_str]

    return random.choice(misspell_list)


# =============================================================================

class CorruptDataSet:
  """Class which provides methods to corrupt the original records generated by
     one of the classes derived from the GenerateDataSet base class.

     The following arguments need to be set when a GenerateDataSet instance is
     initialised:

     number_of_mod_records  The number of modified (corrupted) records that are
                            to be generated. This will correspond to the number
                            of 'duplicate' records that are generated.

     number_of_org_records  The number of original records that were generated
                            by the GenerateDataSet class.
                          
     attribute_name_list    The list of attributes (fields) that have been
                            generated for each record.

     max_num_dup_per_rec    The maximum number of modified (corrupted) records
                            that can be generated for a single original record.

     num_dup_dist           The probability distribution used to create the
                            duplicate records for one original record (possible
                            distributions are: 'uniform', 'poisson', 'zipf')

     max_num_mod_per_attr   The maximum number of modifications are to be
                            applied on a single attribute.

     num_mod_per_rec        The number of modification that are to be applied
                            to a record

     attr_mod_prob_dict     This dictionary contains probabilities that
                            determine how likely an attribute is selected for
                            random modification (corruption).
                            Keys are attribute names and values are probability
                            values. The sum of the given probabilities must sum
                            to 1.0.
                            Not all attributes need to be listed in this
                            dictionary, only the ones onto which modifications
                            are to be applied.
                            An example of such a dictionary is given below.

     attr_mod_data_dict     A dictionary which contains for each attribute that
                            is to be modified a list which contains as pairs of
                            probabilities and corruptor objects (i.e. objects
                            based on any of the classes derived from base class
                            CorruptValue).
                            For each attribute listed, the sum of probabilities
                            given in its list must sum to 1.0.
                            An example of such a dictionary is given below.

     Example for 'attr_mod_prob_dict':

     attr_mod_prob_dict = {'surname':0.4, 'address':0.6}

     In this example, the surname attribute will be selected for modification
     with a 40% likelihood and the address attribute with a 60% likelihood.

     Example for 'attr_mod_data_dict':

     attr_mod_data_dict = {'surname':[(0.25,corrupt_ocr), (0.50:corrupt_edit),
                                      (0.25:corrupt_keyboard)],
                           'address':[(0.50:corrupt_ocr), (0.20:missing_value),
                                      (0.25:corrupt_keyboard)]}

     In this example, if the 'surname' is selected for modification, with a
     25% likelihood an OCR modification will be applied, with 50% likelihood a
     character edit modification will be applied, and with 25% likelihood a
     keyboard typing error modification will be applied.
     If the 'address' attribute is selected, then with 50% likelihood an OCR
     modification will be applied, with 20% likelihood a value will be set to
     a missing value, and with 25% likelihood a keyboard typing error
     modification will be applied.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor, set attributes.
    """

    self.number_of_mod_records = None
    self.number_of_org_records = None
    self.attribute_name_list =   None
    self.max_num_dup_per_rec =   None
    self.num_dup_dist =          None
    self.num_mod_per_rec =       None
    self.max_num_mod_per_attr =  None
    self.attr_mod_prob_dict =    None
    self.attr_mod_data_dict =    None

    # Process the keyword arguments
    #
    for (keyword, value) in kwargs.items():

      if (keyword.startswith('number_of_m')):
        basefunctions.check_is_integer('number_of_mod_records', value)
        basefunctions.check_is_positive('number_of_mod_records', value)
        self.number_of_mod_records = value

      elif (keyword.startswith('number_of_o')):
        basefunctions.check_is_integer('number_of_org_records', value)
        basefunctions.check_is_positive('number_of_org_records', value)
        self.number_of_org_records = value

      elif (keyword.startswith('attribute')):
        basefunctions.check_is_list('attribute_name_list', value)
        self.attribute_name_list = value

      elif (keyword.startswith('max_num_dup')):
        basefunctions.check_is_integer('max_num_dup_per_rec', value)
        basefunctions.check_is_positive('max_num_dup_per_rec', value)
        self.max_num_dup_per_rec = value

      elif (keyword.startswith('num_dup_')):
        if (value not in ['uniform', 'poisson', 'zipf']):
          raise Exception, 'Illegal value given for "num_dup_dist": %s' % \
                           (str(value))
        self.num_dup_dist = value

      elif (keyword.startswith('num_mod_per_r')):
        basefunctions.check_is_integer('num_mod_per_rec', value)
        basefunctions.check_is_positive('num_mod_per_rec', value)
        self.num_mod_per_rec = value

      elif (keyword.startswith('max_num_mod_per_a')):
        basefunctions.check_is_integer('max_num_mod_per_attr', value)
        basefunctions.check_is_positive('max_num_mod_per_attr', value)
        self.max_num_mod_per_attr = value

      elif (keyword.startswith('attr_mod_p')):
        basefunctions.check_is_dictionary('attr_mod_prob_dict', value)
        self.attr_mod_prob_dict = value

      elif (keyword.startswith('attr_mod_d')):
        basefunctions.check_is_dictionary('attr_mod_data_dict', value)
        self.attr_mod_data_dict = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_integer('number_of_mod_records',
                                   self.number_of_mod_records)
    basefunctions.check_is_positive('number_of_mod_records',
                                   self.number_of_mod_records)
    basefunctions.check_is_integer('number_of_org_records',
                                   self.number_of_org_records)
    basefunctions.check_is_positive('number_of_org_records',
                                   self.number_of_org_records)
    basefunctions.check_is_list('attribute_name_list',
                                self.attribute_name_list)
    basefunctions.check_is_integer('max_num_dup_per_rec',
                                   self.max_num_dup_per_rec)
    basefunctions.check_is_positive('max_num_dup_per_rec',
                                    self.max_num_dup_per_rec)
    basefunctions.check_is_string('num_dup_dist', self.num_dup_dist)
    basefunctions.check_is_integer('num_mod_per_rec',
                                   self.num_mod_per_rec)
    basefunctions.check_is_positive('num_mod_per_rec',
                                   self.num_mod_per_rec)
    basefunctions.check_is_integer('max_num_mod_per_attr',
                                   self.max_num_mod_per_attr)
    basefunctions.check_is_positive('max_num_mod_per_attr',
                                   self.max_num_mod_per_attr)
    if (self.max_num_mod_per_attr > self.num_mod_per_rec):
      raise Exception, 'Number of modifications per record must be larger' + \
                       ' than maximum number of modifications per attribute'
    basefunctions.check_is_dictionary('attr_mod_prob_dict',
                                self.attr_mod_prob_dict)
    basefunctions.check_is_dictionary('attr_mod_data_dict',
                                      self.attr_mod_data_dict)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Check if it is possible to generate the desired number of modified
    # (duplicate) corrupted records
    #
    if (self.number_of_mod_records > self.number_of_org_records * \
                                     self.max_num_dup_per_rec):
      raise Exception, 'Desired number of duplicates cannot be generated ' + \
                       'with given number of original records and maximum' + \
                       ' number of duplicates per original record'

    # Check if there are enough attributes given for modifications - - - - - -
    #
    if (len(self.attr_mod_prob_dict) < self.num_mod_per_rec):
      raise Exception, 'Not enough attribute modifications given to obtain' + \
                       ' the desired number of modifications per record'

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Create a distribution for the number of duplicates for an original record
    #
    num_dup =  1
    prob_sum = 0.0
    self.prob_dist_list = [(num_dup, prob_sum)]

    if (self.num_dup_dist == 'uniform'):
      uniform_val = 1.0 / float(self.max_num_dup_per_rec)

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    uniform_val+self.prob_dist_list[-1][1]))

    elif (self.num_dup_dist == 'poisson'):

      def fac(n):  # Factorial of an integer number (recursive calculation)
        if (n > 1.0):
          return n*fac(n - 1.0)
        else:
          return 1.0

      poisson_num = []   # A list of poisson numbers
      poisson_sum = 0.0  # The sum of all poisson number

      # The mean (lambda) for the poisson numbers
      #
      mean = 1.0 + (float(self.number_of_mod_records) / \
                    float(self.number_of_org_records))

      for i in range(self.max_num_dup_per_rec):
        poisson_num.append((math.exp(-mean) * (mean ** i)) / fac(i))
        poisson_sum += poisson_num[-1]

      for i in range(self.max_num_dup_per_rec):  # Scale so they sum up to 1.0
        poisson_num[i] = poisson_num[i] / poisson_sum

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    poisson_num[i]+self.prob_dist_list[-1][1]))

    elif (self.num_dup_dist == 'zipf'):
      zipf_theta = 0.5

      denom = 0.0
      for i in range(self.number_of_org_records):
        denom += (1.0 / (i+1) ** (1.0 - zipf_theta))

      zipf_c = 1.0 / denom
      zipf_num = []  # A list of Zipf numbers
      zipf_sum = 0.0  # The sum of all Zipf number

      for i in range(self.max_num_dup_per_rec):
        zipf_num.append(zipf_c / ((i+1) ** (1.0 - zipf_theta)))
        zipf_sum += zipf_num[-1]

      for i in range(self.max_num_dup_per_rec):  # Scale so they sum up to 1.0
        zipf_num[i] = zipf_num[i] / zipf_sum

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    zipf_num[i]+self.prob_dist_list[-1][1]))

    print 'Probability distribution for number of duplicates per record:'
    print self.prob_dist_list

    # Check probability list for attributes and dictionary for attributes - - -
    # if they sum to 1.0
    #
    attr_prob_sum = sum(self.attr_mod_prob_dict.values())
    if (abs(attr_prob_sum - 1.0) > 0.0000001):
      raise Exception, 'Attribute modification probabilities do not sum ' + \
                       'to 1.0: %f' % (attr_prob_sum)
    for attr_name in self.attr_mod_prob_dict:
      assert self.attr_mod_prob_dict[attr_name] >= 0.0, \
             'Negative probability given in "attr_mod_prob_dict"'
      if attr_name not in self.attribute_name_list:
        raise Exception, 'Attribute name "%s" in "attr_mod_prob_dict" not ' % \
                         (attr_name) + 'listed in "attribute_name_list"'

    # Check details of attribute modification data dictionary
    #
    for (attr_name, attr_mod_data_list) in self.attr_mod_data_dict.items():
      if attr_name not in self.attribute_name_list:
        raise Exception, 'Attribute name "%s" in "attr_mod_data_dict" not ' % \
                         (attr_name) + 'listed in "attribute_name_list"'
      basefunctions.check_is_list('attr_mod_data_dict entry',
                                  attr_mod_data_list)
      prob_sum = 0.0
      for list_elem in attr_mod_data_list:
        basefunctions.check_is_tuple('attr_mod_data_dict list element',
                                     list_elem)
        assert len(list_elem) == 2, 'attr_mod_data_dict list element does ' + \
                                    'not consist of two elements'
        basefunctions.check_is_normalised('attr_mod_data_dict list probability',
                                          list_elem[0])
        prob_sum += list_elem[0]
      if (abs(prob_sum - 1.0) > 0.0000001):
        raise Exception, 'Probability sum is no 1.0 for attribute "%s"' % \
                         (attr_name)

    # Generate a list with attribute probabilities summed for easy selection
    #
    self.attr_mod_prob_list = []
    prob_sum = 0
    for (attr_name, attr_prob) in self.attr_mod_prob_dict.items():
      prob_sum += attr_prob
      self.attr_mod_prob_list.append([prob_sum, attr_name])
    #print self.attr_mod_prob_list

  # ---------------------------------------------------------------------------

  def corrupt_records(self, rec_dict):
    """Method to corrupt modify the records in the given record dictionary
       according to the settings of the data set corruptor.
    """

    # Check if number of records given is what is expected
    #
    assert self.number_of_org_records == len(rec_dict), \
           'Illegal number of records to modify given'

    # First generate for each original record the number of duplicates that are
    # to be generated for it.
    #
    dup_rec_num_dict = {}  # Keys are the record identifiers of the original
                           # records, value their number of duplicates
    total_num_dups = 0     # Total number of duplicates generated

    org_rec_id_list = rec_dict.keys()
    random.shuffle(org_rec_id_list)

    org_rec_i = 0  # Loop counter over which record to assign duplicates to

    while ((org_rec_i < self.number_of_org_records) and \
           (total_num_dups < self.number_of_mod_records)):

      # Randomly choose how many duplicates to create for this original record
      #
      r = random.random()  # Random number between 0.0 and 1.0
      ind = -1
      while (self.prob_dist_list[ind][1] > r):
        ind -= 1
      num_dups = self.prob_dist_list[ind][0]

      assert (num_dups > 0) and (num_dups <= self.max_num_dup_per_rec)

      # Check if there are still 'enough' duplicates to generate
      #
      if (num_dups <= (self.number_of_mod_records-total_num_dups)):

        # Select next record for which to generate duplicates
        #
        org_rec_id = org_rec_id_list[org_rec_i]
        org_rec_i += 1
        dup_rec_num_dict[org_rec_id] = num_dups
        total_num_dups += num_dups

    assert total_num_dups == sum(dup_rec_num_dict.values())

    # Deal with the case where every original record has a number of duplicates
    # but not enough duplicates are generated in total
    #
    org_rec_id_list = rec_dict.keys()
    random.shuffle(org_rec_id_list)

    while (total_num_dups < self.number_of_mod_records):
      org_rec_id = random.choice(org_rec_id_list)

      # If possible, increase number of duplicates for this record by 1
      #
      if (dup_rec_num_dict[org_rec_id] < self.max_num_dup_per_rec):
        dup_rec_num_dict[org_rec_id] = dup_rec_num_dict[org_rec_id]+1
        total_num_dups += 1

    assert sum(dup_rec_num_dict.values()) == self.number_of_mod_records

    # Generate a histogram of number of duplicates per record
    #
    dup_histo = {}
    for (org_rec_id_to_mod, num_dups) in dup_rec_num_dict.iteritems():
      dup_count = dup_histo.get(num_dups, 0) + 1
      dup_histo[num_dups] = dup_count
    print 'Distribution of number of original records with certain number ' + \
          'of duplicates:'
    dup_histo_keys = dup_histo.keys()
    dup_histo_keys.sort()
    for num_dups in dup_histo_keys:
      print ' Number of records with %d duplicates: %d' % \
            (num_dups, dup_histo[num_dups])
    print

    num_dup_rec_created = 0  # Count how many duplicate records have been
                             # generated

    # Main loop over all original records for which to generate duplicates - -
    #
    for (org_rec_id_to_mod, num_dups) in dup_rec_num_dict.iteritems():
      assert (num_dups > 0) and (num_dups <= self.max_num_dup_per_rec)

      print
      print 'Generating %d modified (duplicate) records for record "%s"' % \
            (num_dups, org_rec_id_to_mod)

      rec_to_mod_list = rec_dict[org_rec_id_to_mod]

      d = 0  # Loop counter for duplicates for this record

      this_dup_rec_list = []  # A list of all duplicates for this record

      # Loop to create duplicate records - - - - - - - - - - - - - - - - - - - -
      #
      while (d < num_dups):

        # Create a duplicate of the original record
        #
        dup_rec_list = rec_to_mod_list[:] # Make copy of original record

        org_rec_num = org_rec_id_to_mod.split('-')[1]
        dup_rec_id = 'rec-%s-dup-%d' % (org_rec_num, d)
        print '  Generate identifier for duplicate record based on "%s": %s' \
              % (org_rec_id_to_mod, dup_rec_id)

        # Count the number of modifications in this record (counted as the
        # number of modified attributes)
        #
        num_mod_in_record = 0

        # Set the attribute modification counters to zero for all attributes
        # that can be modified
        #
        attr_mod_count_dict = {}
        for attr_name in self.attr_mod_prob_dict.keys():
          attr_mod_count_dict[attr_name] = 0

        # Abort generating modifications after a larger number of tries to
        # prevent an endless loop
        #
        max_num_tries = self.num_mod_per_rec*10
        num_tries =     0

        # Now apply desired number of modifications to this record
        #
        while ((num_mod_in_record < self.num_mod_per_rec) and
               (num_tries < max_num_tries)):

          # Randomly modify an attribute value
          #
          r = random.random()  # Random value between 0.0 and 1.0
          i = 0
          while (self.attr_mod_prob_list[i][0] < r):
            i += 1
          mod_attr_name = self.attr_mod_prob_list[i][1]

          if (attr_mod_count_dict[mod_attr_name] < self.max_num_mod_per_attr):
            mod_attr_name_index = self.attribute_name_list.index(mod_attr_name)
            mod_attr_val = dup_rec_list[mod_attr_name_index]

            # Select an attribute to modify according to probability
            # distribution of corruption methods
            #
            attr_mod_data_list = self.attr_mod_data_dict[mod_attr_name]

            r = random.random()  # Random value between 0.0 and 1.0
            p_sum = attr_mod_data_list[0][0]
            i = 0
            while (r >= p_sum):
              i += 1
              p_sum += attr_mod_data_list[i][0]
            corruptor_method = attr_mod_data_list[i][1]

            # Modify the value from the selected attribute
            #
            new_attr_val = corruptor_method.corrupt_value(mod_attr_val)

            org_attr_val = rec_to_mod_list[mod_attr_name_index]

            # If the modified value is different insert it back into modified
            # record
            #
            if (new_attr_val != org_attr_val):
              print '  Selected attribute for modification:', mod_attr_name
              print '    Selected corruptor:', corruptor_method.name

              # The following weird string printing construct is to overcome
              # problems with printing non-ASCII characters
              #              
              print '      Original attribute value:', str([org_attr_val])[1:-1]
              print '      Modified attribute value:', str([new_attr_val])[1:-1]

              dup_rec_list[mod_attr_name_index] = new_attr_val

              # One more modification for this attribute
              #
              attr_mod_count_dict[mod_attr_name] += 1

              # The number of modifications in a record corresponds to the
              # number of modified attributes
              #
              num_mod_in_record = 0

              for num_attr_mods in attr_mod_count_dict.values():
                if (num_attr_mods > 0):
                  num_mod_in_record += 1  # One more modification
              assert num_mod_in_record <= self.num_mod_per_rec

            num_tries += 1  # One more try to modify record

        # Check if this duplicate is different from all others for this original
        # record
        #
        is_diff = True  # Flag to check if the latest duplicate is different

        if (this_dup_rec_list == []):  # No duplicate so far
          this_dup_rec_list.append(dup_rec_list)
        else:
          for check_dup_rec in this_dup_rec_list:
            if (check_dup_rec == dup_rec_list):  # Same as a previous duplicate
              is_diff = False
              print 'Same duplicate:', check_dup_rec
              print '               ', dup_rec_list

        if (is_diff == True):  # Only keep duplicate records that are different

          # Safe the record into the overall record dictionary
          #
          rec_dict[dup_rec_id] = dup_rec_list

          d += 1
          num_dup_rec_created += 1

          print 'Original record:'
          print ' ', rec_to_mod_list
          print 'Record with %d modified attributes' % (num_mod_in_record),
          attr_mod_str = '('
          for a in self.attribute_name_list:
            if (attr_mod_count_dict.get(a,0) > 0):
              attr_mod_str += '%d in %s, ' % (attr_mod_count_dict[a],a)
          attr_mod_str = attr_mod_str[:-1]+'):'
          print attr_mod_str
          print ' ', dup_rec_list
          print '%d of %d duplicate records generated so far' % \
                (num_dup_rec_created, self.number_of_mod_records)
          print

    return rec_dict

# =============================================================================
