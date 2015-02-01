# generator.py - Python module to generate synthetic data.
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

"""Module containing several classes to generate synthetic data according to
   user specification.
"""

# -----------------------------------------------------------------------------
# Import necessary modules

import random

import basefunctions

# =============================================================================
# Classes for generating a single attribute (field) of the data set
# =============================================================================

class GenerateAttribute:
  """Base class for the definition of a single attribute (field) to be
     generated.

     This class and all of its derived classes provide methods that allow the
     definition of a single attribute and the parameters necessary for its
     generation.

     The following variables need to be set when a GenerateAttribute instance
     is initialised (with further parameters listed in the derived classes):

     attribute_name  The name of this attribute, which will be used in the
                     header line to be written into the output file.

                     Ideally, this attribute name should be short, not contain
                     spaces and it must not contain any quote or punctuation
                     characters.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, base_kwargs):
    """Constructor, set general attributes.
    """

    # General attributes for all attribute generators
    #
    self.attribute_name = None

    # Process the keyword argument (all keywords specific to a certain data
    # generator type were processed in the derived class constructor)
    #
    for (keyword, value) in base_kwargs.items():

      if (keyword.startswith('attribute')):
        basefunctions.check_is_non_empty_string('attribute_name', value)
        self.attribute_name = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    basefunctions.check_is_non_empty_string('attribute_name',
                                            self.attribute_name)

    # Check the content of the attribute name string for certain characters
    # that would pose problems when generating comma separated values (CSV)
    # files.
    #
    if (("'" in self.attribute_name) or ('"' in self.attribute_name) or \
        ("`" in self.attribute_name) or (',' in self.attribute_name) or \
        (";" in self.attribute_name) or ('\t' in self.attribute_name)):
      raise Exception, 'Illegal character (such as comma, semi-colon or' + \
                       'quote in attribute name'

  # ---------------------------------------------------------------------------

  def create_attribute_value(self):
    """Method which creates and returns one attribute value.
       See implementations in derived classes for details.
    """

    raise Exception, 'Override abstract method in derived class'

# =============================================================================

class GenerateFreqAttribute(GenerateAttribute):
  """Generate an attribute where values are retrieved from a lookup table that
     contains categorical attribute values and their frequencies.

     The additional argument (besides the base class argument 'attribute_name')
     that has to be set when this attribute type is initialised are:

     freq_file_name    The name of the file which contains the attribute values
                       and their frequencies.

                       This file must be in comma separated values (CSV) format
                       with the first column being the attribute values and the
                       second column their counts (positive integer numbers).

                       Each attribute value must only occur once in the
                       frequency file.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the frequency file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.attribute_type =   'Frequency'
    self.freq_file_name =   None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.attr_value_list =  []  # The list of attribute values to be loaded

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('freq')):
        basefunctions.check_is_non_empty_string('freq_file_name', value)
        self.freq_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        base_kwargs[keyword] = value

    GenerateAttribute.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('freq_file_name',
                                            self.freq_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the frequency file - - - - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, freq_file_data = \
                     basefunctions.read_csv_file(self.freq_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    val_dict = {}   # The attribute values to be loaded from file and their
                    # counts or frequencies

    # Process values from file and their frequencies
    #
    for rec_list in freq_file_data:
      if (len(rec_list) != 2):
        raise Exception, 'Illegal format in frequency file %s: %s' % \
                         (self.freq_file_name, line)
      line_val =  rec_list[0].strip()
      try:
        line_count = int(rec_list[1])
      except:
        raise Exception, 'Value count given is not an integer number: %s' % \
                         (rec_list[1])

      if (line_val == ''):
        raise Exception, 'Empty attribute value in frequency file %s' % \
                         (self.freq_file_name)
      basefunctions.check_is_positive('line_count', line_count)

      if (line_val in val_dict):
        raise Exception, 'Attribute values "%s" occurs twice in ' % \
                         (line_val) + 'frequency file %s' % \
                         (self.freq_file_name)

      val_dict[line_val] = line_count

    val_list = []  # The list of attribute values, with values repeated
                   # according to their frequencies

    # Generate a list of values according to their counts
    #
    for (attr_val, val_count) in val_dict.iteritems():

      # Append value as many times as given in their counts
      #
      new_list = [attr_val]* val_count
      val_list += new_list

    random.shuffle(val_list)  # Randomly shuffle the list of values

    self.attr_value_list = val_list

  # ---------------------------------------------------------------------------

  def create_attribute_value(self):
    """Method which creates and returns one attribute value randomly selected
       from the attribute value lookup table.
    """

    assert self.attr_value_list != []

    return random.choice(self.attr_value_list)

# =============================================================================

class GenerateFuncAttribute(GenerateAttribute):
  """Generate an attribute where values are retrieved from a function that
     creates values according to some specification.

     Such functions include creating telephone numbers or social security
     numbers with a certain structure, or numerical values normally or
     uniformly distributed according to some parameter setting.

     The additional argument (besides the base class argument 'attribute_name')
     that has to be set when this attribute type is initialised are:

     function    A Python function that, when called, has to return a string
                 value that is created according to some specification.

     parameters  A list of one or more parameters (maximum 5) passed to the
                 function when it is called.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.attribute_type = 'Function'
    self.function =       None
    self.parameters =     None

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('funct')):
        basefunctions.check_is_function_or_method('function', value)
        self.function = value

      elif (keyword.startswith('para')):
        basefunctions.check_is_list('parameters', value)
        if (len(value) > 5):
          raise Exception, 'Maximum five parameters allowed for function call'
        self.parameters = value

      else:
        base_kwargs[keyword] = value

    GenerateAttribute.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_function_or_method('function', self.function)

    # Check if the function does return a string (five different possibilities,
    # depending upon number of parameters)
    #
    if (self.parameters == None) or (len(self.parameters) == 0):
      funct_ret = self.function()
    elif (len(self.parameters) == 1):
      funct_ret = self.function(self.parameters[0])
    elif (len(self.parameters) == 2):
      funct_ret = self.function(self.parameters[0], self.parameters[1])
    elif (len(self.parameters) == 3):
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2])
    elif (len(self.parameters) == 4):
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2], self.parameters[3])
    else:
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2], self.parameters[3],
                                self.parameters[4])

    if (not isinstance(funct_ret, str)):
      raise Exception, ('Function provided does not return a string value:',
                        self.function, type(funct_ret))

  # ---------------------------------------------------------------------------

  def create_attribute_value(self):
    """Method which creates and returns one attribute value generated by the
       function provided.
    """

    if (self.parameters == None):
      funct_ret = self.function()
    elif (len(self.parameters) == 1):
      funct_ret = self.function(self.parameters[0])
    elif (len(self.parameters) == 2):
      funct_ret = self.function(self.parameters[0], self.parameters[1])
    elif (len(self.parameters) == 3):
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2])
    elif (len(self.parameters) == 4):
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2], self.parameters[3])
    else:
      funct_ret = self.function(self.parameters[0], self.parameters[1],
                                self.parameters[2], self.parameters[3],
                                self.parameters[4])
    return funct_ret

# =============================================================================
# Classes for generating compound attributes (fields) of the data set
# =============================================================================

class GenerateCompoundAttribute:
  """Base class for the definition of compound attributes (fields) to be
     generated.

     This class and all of its derived classes provide methods that allow the
     definition of several (are least two) attributes and the parameters
     necessary for their generation.

     This base class does not have any generic variables that need to be set.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, base_kwargs):
    """Constructor. See implementations in derived classes for details.
    """

    raise Exception, 'Override abstract method in derived class'

  # ---------------------------------------------------------------------------

  def create_attribute_value(self):
    """Method which creates and returns several (compound) attribute values.
       See implementations in derived classes for details.
    """

    raise Exception, 'Override abstract method in derived class'

# =============================================================================

class GenerateCateCateCompoundAttribute(GenerateCompoundAttribute):
  """Generate two attributes, both containing categorical values, where the
     values of the second attribute depend upon the values in the first
     attribute.

     This for example allows the modelling of:
     - city location values that depend upon gender values, or
     - medication name values that depend upon gender values.

     The arguments that have to be set when this attribute type is initialised
     are:

     categorical1_attribute_name  The name of the first categorical attribute
                                  that will be generated. This name will be
                                  used in the header line to be written into
                                  the output file.

     categorical2_attribute_name  The name of the second categorical attribute
                                  that will be generated. This name will be
                                  used in the header line to be written into
                                  the output file.

     lookup_file_name             Name of the file which contains the values of
                                  the first categorical attribute, and for each
                                  of these values the names of the categories
                                  and their counts of the second categorical
                                  attribute. This file format is further
                                  explained below.

     has_header_line              A flag, set to True or False, that has to be
                                  set according to if the look-up file starts
                                  with a header line or not.

     unicode_encoding             The Unicode encoding (a string name) of the
                                  file.

     The format of the look-up file is:

     # Comment lines start with the # character
     cate_attr1_val,count,cate_attr2_val1,count1,cate_attr2_val2,count2, \
     cate_attr2_val3,count3,cate_attr2_val4,count4, ...

     The look-up file is a comma separated values (CSV) file which contains
     two types of rows:
     A) The first type of row contains the following columns:
        1) A categorical value. For all possible values of the first
           categorical attribute, one row must be specified in this look-up
           file.
        2) Count of this categorical value (a positive integer number). This
           determines the likelihood of how often a certain categorical value
           will be chosen. This count must be a positive integer number.
        3) The first categorical value of the second attribute.
        4) The count (positive integer number) of this first categorical
           value.
        5) The second categorical value of the second attribute.
        6) The count of this second categorical value.

        ...

        X) A '\' character, which indicates that the following line (row)
           contains further categorical values and their counts from the
           second attribute.

     B) The second type of row contains the following columns:
        1) A categorical value of the second attribute.
        2) The count of this categorical value.
        3) Another categorical value of the second attribute.
        4) The count of this categorical value.

        ...

     Example:
       male,60,canberra,7, \
       sydney,30,melbourne,45, \
       perth,18
       female,40,canberra,10,sydney,40, \
       melbourne,20,brisbane,30,hobart,5,\
       perth,20
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    # General attributes for all data set generators
    #
    self.number_of_atttributes = 2
    self.attribute_type =        'Compound-Categorical-Categorical'

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('categorical1')):
        basefunctions.check_is_non_empty_string('categorical1_attribute_name',
                                                value)
        self.categorical1_attribute_name = value

      elif (keyword.startswith('categorical2')):
        basefunctions.check_is_non_empty_string('categorical2_attribute_name',
                                                value)
        self.categorical2_attribute_name = value

      elif (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('categorical1_attribute_name',
                                            self.categorical1_attribute_name)
    basefunctions.check_is_non_empty_string('categorical2_attribute_name',
                                            self.categorical2_attribute_name)
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    if (self.categorical1_attribute_name == self.categorical2_attribute_name):
      raise Exception, 'Both attribute names are the same'

    # Load the lookup file - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    cate_val1_dict = {}  # The categorical values from attribute 1 to be loaded
                         # from file and their counts.

    cate_val2_dict = {}  # The categorical values from attribute 1 to be loaded
                         # as keys and lists of categorical values (according
                         # to their counts) from attribute 2 as values.

    # Process attribute values from file and their details
    #
    i = 0  # Line counter in file data

    while i < len(lookup_file_data):
      rec_list = lookup_file_data[i]

      # First line must contain categorical value of the first attribute
      #
      if (len(rec_list) < 2):  # Need at least two values in each line
        raise Exception, 'Illegal format in lookup file %s: %s' % \
                         (self.freq_file_name, str(rec_list))
      cate_attr1_val =  rec_list[0].strip()
      try:
        cate_attr1_count = int(rec_list[1])
      except:
        raise Exception, 'Value count given for attribute 1 is not an ' + \
                         'integer number: %s' % (rec_list[1])

      if (cate_attr1_val == ''):
        raise Exception, 'Empty categorical attribute 1 value in lookup ' + \
                         'file %s' % (self.lookup_file_name)
      basefunctions.check_is_positive('cate_attr1_count', cate_attr1_count)

      if (cate_attr1_val in cate_val1_dict):
        raise Exception, 'Attribute 1 value "%s" occurs twice in ' % \
                         (cate_attr1_val) + 'lookup file %s' % \
                         (self.lookup_file_name)

      cate_val1_dict[cate_attr1_val] = cate_attr1_count

      # Process values for second categorical attribute in this line
      #
      cate_attr2_data = rec_list[2:]  # All values and counts of attribute 2

      this_cate_val2_dict = {}  # Values in second categorical attribute for
                                # this categorical value from first attribute

      while (cate_attr2_data != []):
        if (len(cate_attr2_data) == 1):
          if (cate_attr2_data[0] != '\\'):
            raise Exception, 'Line in categorical look-up file has illegal' + \
                             'format.'
          # Get the next record from file data with a continuation of the
          # categorical values from the second attribute
          #
          i += 1
          cate_attr2_data = lookup_file_data[i]
          if (len(cate_attr2_data) < 2):
            raise Exception, 'Illegal format in lookup file %s: %s' % \
                             (self.freq_file_name, str(cate_attr2_data))

        cate_attr2_val =   cate_attr2_data[0]
        try:
          cate_attr2_count = int(cate_attr2_data[1])
        except:
          raise Exception, 'Value count given for attribute 2 is not an ' + \
                           'integer number: %s' % (cate_attr2_data[1])

        if (cate_attr2_val == ''):
          raise Exception, 'Empty categorical attribute 2 value in lookup' \
                           + ' file %s' % (self.lookup_file_name)
        basefunctions.check_is_positive('cate_attr2_count', cate_attr2_count)

        if (cate_attr2_val in cate_val2_dict):
          raise Exception, 'Attribute 2 value "%s" occurs twice in ' % \
                           (cate_attr2_val) + 'lookup file %s' % \
                           (self.lookup_file_name)

        this_cate_val2_dict[cate_attr2_val] = cate_attr2_count

        cate_attr2_data = cate_attr2_data[2:]

      # Generate a list of values according to their counts
      #
      cate_attr2_val_list = []

      for (cate_attr2_val, val2_count) in this_cate_val2_dict.iteritems():

        # Append value as many times as given in their counts
        #
        new_list = [cate_attr2_val]* val2_count
        cate_attr2_val_list += new_list

      random.shuffle(cate_attr2_val_list) # Randomly shuffle the list of values

      cate_val2_dict[cate_attr1_val] = cate_attr2_val_list

      # Go to next line in file data
      #
      i += 1

    # Generate a list of values according to their counts
    #
    cate_attr1_val_list = []

    for (cate_attr1_val, val1_count) in cate_val1_dict.iteritems():

      # Append value as many times as given in their counts
      #
      new_list = [cate_attr1_val]* val1_count
      cate_attr1_val_list += new_list

    random.shuffle(cate_attr1_val_list)  # Randomly shuffle the list of values

    self.cate_attr1_val_list = cate_attr1_val_list
    self.cate_val2_dict =      cate_val2_dict

  # ---------------------------------------------------------------------------

  def create_attribute_values(self):
    """Method which creates and returns two categorical attribute values, where
       the second value depends upon the first value. Both categorical values
       are randomly selected according to the provided frequency distributions.
    """

    assert self.cate_attr1_val_list != []
    assert self.cate_val2_dict != {}

    cate_attr1_val = random.choice(self.cate_attr1_val_list)

    cate_attr2_list = self.cate_val2_dict[cate_attr1_val]

    cate_attr2_val = random.choice(cate_attr2_list)
 
    return cate_attr1_val, cate_attr2_val

# =============================================================================

class GenerateCateContCompoundAttribute(GenerateCompoundAttribute):
  """Generate two attributes, one containing categorical values and the other
     continuous values, where the continuous values depend upon the categorical
     values.

     This for example allows the modelling of:
     - salary values that depend upon gender values, or
     - blood pressure values that depend upon age values.

     The arguments that have to be set when this attribute type is initialised
     are:

     categorical_attribute_name  The name of the categorical attribute that
                                 will be generated. This name will be used in
                                 the header line to be written into the output
                                 file.

     continuous_attribute_name   The name of the continuous attribute that will
                                 be generated. This name will be used in the
                                 header line to be written into the output
                                 file.

     lookup_file_name            Name of the file which contains the values of
                                 the continuous attribute, and for each of these
                                 values the name of a function (and its
                                 parameters) that is used to generate the
                                 continuous values. This file format is further
                                 explained below.

     has_header_line             A flag, set to True or False, that has to be
                                 set according to if the look-up file starts
                                 with a header line or not.

     unicode_encoding            The Unicode encoding (a string name) of the
                                 file.

     continuous_value_type       The format of how continuous values are
                                 returned when they are generated. Possible
                                 values are 'int', so integer values are
                                 returned; or 'float1', 'float2', to 'float9',
                                 in which case floating-point values with the
                                 specified number of digits behind the comma
                                 are returned.

     The format of the look-up file is:

     # Comment lines start with the # character
     cate_val,count,funct_name,funct_param_1,...,funct_param_N

     The look-up file is a comma separated values (CSV) file with the following
     columns:
     1) A categorical value. For all possible categorical values of an
        attribute, one row must be specified in this look-up file.

     2) Count of this categorical value (a positive integer number). This
        determines the likelihood of how often a certain categorical value will
        be chosen.

     3) A function which generates the continuous value for this categorical
        value. Implemented functions currently are:
        - uniform
        - normal

     4) The parameters required for the function that generates the continuous
        values. They are:
        - uniform:  min_val, max_val
        - normal:   mu, sigma, min_val, max_val
                    (min_val and max_val can be set to None in which case no
                    minimum or maximum is enforced)

     Example:
       male,60,uniform,20000,100000  
       female,40,normal,35000,100000,10000,None
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    # General attributes for all data set generators
    #
    self.number_of_atttributes = 2
    self.attribute_type =        'Compound-Categorical-Continuous'

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('cate')):
        basefunctions.check_is_non_empty_string('categorical_attribute_name',
                                                value)
        self.categorical_attribute_name = value

      elif (keyword.startswith('continuous_a')):
        basefunctions.check_is_non_empty_string('continuous_attribute_name',
                                                value)
        self.continuous_attribute_name = value

      elif (keyword.startswith('continuous_v')):
        basefunctions.check_is_non_empty_string('continuous_value_type',
                                                value)
        basefunctions.check_is_valid_format_str('continuous_value_type',
                                                value)
        self.continuous_value_type = value

      elif (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('categorical_attribute_name',
                                            self.categorical_attribute_name)
    basefunctions.check_is_non_empty_string('continuous_attribute_name',
                                            self.continuous_attribute_name)
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    if (self.categorical_attribute_name == self.continuous_attribute_name):
      raise Exception, 'Both attribute names are the same'

    basefunctions.check_is_valid_format_str('continuous_value_type',
                                            self.continuous_value_type)

    # Load the lookup file - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    cate_val_dict = {}    # The categorical attribute values to be loaded from
                          # file and their counts.
    cont_funct_dict = {}  # For each categorical attribute value the details of
                          # the function used for the continuous attribute.

    # Process attribute values from file and their details
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) not in [5,7]):
        raise Exception, 'Illegal format in lookup file %s: %s' % \
                         (self.lookup_file_name, str(rec_list))
      cate_attr_val =  rec_list[0].strip()
      try:
        cate_attr_count = int(rec_list[1])
      except:
        raise Exception, 'Value count given for categorical attribute is ' + \
                         'not an integer number: %s' % (rec_list[1])
      cont_attr_funct = rec_list[2].strip()

      if (cate_attr_val == ''):
        raise Exception, 'Empty categorical attribute value in lookup file %s'\
                         % (self.lookup_file_name)
      if (cate_attr_count <= 0):
        raise Exception, 'Count given for categorical attribute is not ' + \
                         'positive for value "%s" in lookup ' % \
                         (cate_attr_val) + 'file %s' % (self.lookup_file_name)

      if (cate_attr_val in cate_val_dict):
        raise Exception, 'Attribute values "%s" occurs twice in ' % \
                         (cate_attr_val) + 'lookup file %s' % \
                         (self.lookup_file_name)

      if (cont_attr_funct not in ['uniform','normal']):
        raise Exception, 'Illegal continuous attribute function given: "%s"' % \
                         (cont_attr_funct) + ' in lookup file %s' % \
                         (self.lookup_file_name)

      cate_val_dict[cate_attr_val] = cate_attr_count

      # Get function parameters from file data
      #
      if (cont_attr_funct == 'uniform'):
        cont_attr_funct_min_val = float(rec_list[3])
        basefunctions.check_is_number('cont_attr_funct_min_val',
                                      cont_attr_funct_min_val)

        cont_attr_funct_max_val = float(rec_list[4])
        basefunctions.check_is_number('cont_attr_funct_max_val',
                                      cont_attr_funct_max_val)

        cont_funct_dict[cate_attr_val] = [cont_attr_funct,
                                          cont_attr_funct_min_val,
                                          cont_attr_funct_max_val]

      elif (cont_attr_funct == 'normal'):
        cont_attr_funct_mu =    float(rec_list[3])
        basefunctions.check_is_number('cont_attr_funct_mu',
                                      cont_attr_funct_mu)

        cont_attr_funct_sigma = float(rec_list[4])
        basefunctions.check_is_number('cont_attr_funct_sigma',
                                      cont_attr_funct_sigma)
        try:
          cont_attr_funct_min_val = float(rec_list[5])
        except:
          cont_attr_funct_min_val = None
        if (cont_attr_funct_min_val != None):
          basefunctions.check_is_number('cont_attr_funct_min_val',
                                        cont_attr_funct_min_val)
        try:
          cont_attr_funct_max_val = float(rec_list[6])
        except:
          cont_attr_funct_max_val = None
        if (cont_attr_funct_max_val != None):
          basefunctions.check_is_number('cont_attr_funct_max_val',
                                        cont_attr_funct_max_val)

        cont_funct_dict[cate_attr_val] = [cont_attr_funct,
                                          cont_attr_funct_mu,
                                          cont_attr_funct_sigma,
                                          cont_attr_funct_min_val,
                                          cont_attr_funct_max_val]

    # Generate a list of values according to their counts
    #
    cate_attr_val_list = []

    for (cate_attr_val, val_count) in cate_val_dict.iteritems():

      # Append value as many times as given in their counts
      #
      new_list = [cate_attr_val]* val_count
      cate_attr_val_list += new_list

    random.shuffle(cate_attr_val_list)  # Randomly shuffle the list of values

    self.cate_attr_val_list = cate_attr_val_list
    self.cont_funct_dict =    cont_funct_dict

  # ---------------------------------------------------------------------------

  def create_attribute_values(self):
    """Method which creates and returns two attribute values, one categorical
       and one continuous, with the categorical value randomly selected
       according to the provided frequency distribution, and the continuous
       value according to the selected function and its parameters.
    """

    assert self.cate_attr_val_list != []

    cate_attr_val = random.choice(self.cate_attr_val_list)

    # Get the details of the function and generate the continuous value
    #
    funct_details = self.cont_funct_dict[cate_attr_val]
    funct_name = funct_details[0]

    if (funct_name == 'uniform'):
      cont_attr_val = random.uniform(funct_details[1], funct_details[2])

    elif (funct_name == 'normal'):
      mu =      funct_details[1]
      sigma =   funct_details[2]
      min_val = funct_details[3]
      max_val = funct_details[4]
      in_range = False

      cont_attr_val = random.normalvariate(mu, sigma)

      while (in_range == False):
        if (((min_val != None) and (cont_attr_val < min_val)) or
            ((max_val != None) and (cont_attr_val > max_val))):
          in_range = False
          cont_attr_val = random.normalvariate(mu, sigma)
        else:
          in_range = True

      if (min_val != None):
        assert cont_attr_val >= min_val
      if (max_val != None):
        assert cont_attr_val <= max_val

    else:
      raise Exception, ('Illegal continuous function given:', funct_name)

    cont_attr_val_str = basefunctions.float_to_str(cont_attr_val,
                                                   self.continuous_value_type)

    return cate_attr_val, cont_attr_val_str

# =============================================================================

class GenerateCateCateContCompoundAttribute(GenerateCompoundAttribute):
  """Generate three attributes, thefirst two containing categorical values and
     the third containing continuous values, where the values of the second
     attribute depend upon the values in the first attribute, and the values
     of the third attribute depend upon both the values of the first and second
     attribute.

     This for example allows the modelling of:
     - blood pressure depending upon gender and city of residence values, or
     - salary depending upon gender and profession values.

     The arguments that have to be set when this attribute type is initialised
     are:

     categorical1_attribute_name  The name of the first categorical attribute
                                  that will be generated. This name will be
                                  used in the header line to be written into
                                  the output file.

     categorical2_attribute_name  The name of the second categorical attribute
                                  that will be generated. This name will be
                                  used in the header line to be written into
                                  the output file.

     continuous_attribute_name    The name of the continuous attribute that
                                  will be generated. This name will be used in
                                  the header line to be written into the output
                                  file.

     lookup_file_name              Name of the file which contains the values
                                   of the first categorical attribute, and for
                                   each of these values the names of the
                                   categories and their counts of the second
                                   categorical attribute, and for each of these
                                   values the name of a function (and its
                                   parameters) that is used to generate the
                                   continuous values. This file format is
                                   further explained below.

     has_header_line               A flag, set to True or False, that has to be
                                   set according to if the look-up file starts
                                   with a header line or not.

     unicode_encoding              The Unicode encoding (a string name) of the
                                   file.

     continuous_value_type         The format of how continuous values are
                                   returned when they are generated. Possible
                                   values are 'int', so integer values are
                                   returned; or 'float1', 'float2', to
                                   'float9', in which case floating-point
                                   values with the specified number of digits
                                   behind the comma are returned.

     The format of the look-up file is:

     # Comment lines start with the # character
     cate_attr1_val1,count
     cate_attr2_val1,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr2_val2,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr2_val3,count,funct_name,funct_param_1,...,funct_param_N
     ...
     cate_attr2_valX,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr1_val2,count
     cate_attr2_val1,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr2_val2,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr2_val3,count,funct_name,funct_param_1,...,funct_param_N
     ...
     cate_attr2_valX,count,funct_name,funct_param_1,...,funct_param_N
     cate_attr1_val3,count
     ...


     The look-up file is a comma separated values (CSV) file with the following
     structure:

     A) One row that contains two values:
        1) A categorical value of the first attribute. For all possible values
           of the first categorical attribute, one row must be specified in
           this look-up file.
        2) The count of this categorical value (a positive integer number).
           This determines the likelihood of how often a certain categorical
           value will be chosen.

     B) After a row with two values, as described under A), one or more rows
        containing the following values in columns must be given:
        1) A categorical value from the second categorical attribute.
        2) The count of this categorical value (a positive integer number).
           This determines the likelihood of how often a certain categorical
           value will be chosen.
       3) A function which generates the continuous value for this categorical
          value. Implemented functions currently are:
          - uniform
          - normal
       4) The parameters required for the function that generates the
          continuous values. They are:
          - uniform:  min_val, max_val
          - normal:   mu, sigma, min_val, max_val
                      (min_val and max_val can be set to None in which case no
                      minimum or maximum is enforced)

     Example:
       male,60
       canberra,20,uniform,50000,90000
       sydney,30,normal,75000,50000,20000,None
       melbourne,30,uniform,35000,200000
       perth,20,normal,55000,250000,15000,None
       female,40
       canberra,10,normal,45000,10000,None,150000
       sydney,40,uniform,60000,200000
       melbourne,20,uniform,50000,1750000
       brisbane,30,normal,55000,20000,20000,100000
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    # General attributes for all data set generators
    #
    self.number_of_atttributes = 3
    self.attribute_type =        'Compound-Categorical-Categorical-Continuous'

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('categorical1')):
        basefunctions.check_is_non_empty_string('categorical1_attribute_name',
                                                value)
        self.categorical1_attribute_name = value

      elif (keyword.startswith('categorical2')):
        basefunctions.check_is_non_empty_string('categorical2_attribute_name',
                                                value)
        self.categorical2_attribute_name = value

      elif (keyword.startswith('continuous_a')):
        basefunctions.check_is_non_empty_string('continuous_attribute_name',
                                                value)
        self.continuous_attribute_name = value

      elif (keyword.startswith('continuous_v')):
        basefunctions.check_is_non_empty_string('continuous_value_type',
                                                value)
        basefunctions.check_is_valid_format_str('continuous_value_type',
                                                value)
        self.continuous_value_type = value

      elif (keyword.startswith('look')):
        basefunctions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        basefunctions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('categorical1_attribute_name',
                                            self.categorical1_attribute_name)
    basefunctions.check_is_non_empty_string('categorical2_attribute_name',
                                            self.categorical2_attribute_name)
    basefunctions.check_is_non_empty_string('continuous_attribute_name',
                                            self.continuous_attribute_name)
    basefunctions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    basefunctions.check_is_flag('has_header_line', self.has_header_line)
    basefunctions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    if (self.categorical1_attribute_name == self.categorical2_attribute_name) \
       or \
       (self.categorical1_attribute_name == self.continuous_attribute_name) \
       or \
       (self.categorical2_attribute_name == self.continuous_attribute_name):
      raise Exception, 'Not all attribute names are different.'

    basefunctions.check_is_valid_format_str('continuous_value_type',
                                            self.continuous_value_type)

    # Load the lookup file - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     basefunctions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    cate_val1_dict = {}   # The categorical values from attribute 1 to be
                          # loaded from file, and their counts.

    cate_val2_dict = {}   # The categorical values from attribute 1 as keys
                          # and lists of categorical values (according to their
                          # counts) from attribute 2 as values.

    cont_funct_dict = {}  # For each pair of categorical attribute values the
                          # details of the function used for the continuous
                          # attribute.

    # Process attribute values from file and their details
    #
    list_counter = 0  # Counter in the list of lookup file data
    num_file_rows = len(lookup_file_data)
    rec_list = lookup_file_data[list_counter]

    while list_counter < num_file_rows:  # Process one row after another

      if (len(rec_list) < 2):  # Need at least one categorical value and count
        raise Exception, 'Illegal format in lookup file %s: %s' % \
                         (self.lookup_file_name, str(rec_list))
      cate_attr1_val =  rec_list[0].strip()
      try:
        cate_attr1_count = int(rec_list[1])
      except:
        raise Exception, 'Value count given for attribute 1 is not an ' + \
                         'integer number: %s' % (rec_list[1])

      if (cate_attr1_val == ''):
        raise Exception, 'Empty categorical attribute value 1 in lookup ' + \
                         'file %s' % (self.lookup_file_name)
      basefunctions.check_is_positive('cate_attr1_count', cate_attr1_count)

      if (cate_attr1_val in cate_val1_dict):
        raise Exception, 'Attribute value "%s" occurs twice in ' % \
                         (cate_attr1_val) + 'lookup file %s' % \
                         (self.lookup_file_name)

      cate_val1_dict[cate_attr1_val] = cate_attr1_count

      # Loop to process values of the second categorical attribute and the
      # corresponding continuous functions
      #
      list_counter += 1
      rec_list = lookup_file_data[list_counter]  # Get values from next line

      this_cate_val2_dict = {}  # Values of categorical attribute 2
      this_cont_funct_dict = {}

      # As long as there are data from the second categorical attribute 
      #
      while (len(rec_list) > 2):
        cate_attr2_val =  rec_list[0].strip()
        try:
          cate_attr2_count = int(rec_list[1])
        except:
          raise Exception, 'Value count given for categorical attribute 2 ' + \
                           'is not an integer number: %s' % (rec_list[1])
        cont_attr_funct = rec_list[2].strip()

        if (cate_attr2_val == ''):
          raise Exception, 'Empty categorical attribute 2 value in lookup ' + \
                           'file %s' % (self.lookup_file_name)
        basefunctions.check_is_positive('cate_attr2_count', cate_attr2_count)

        if (cate_attr2_val in this_cate_val2_dict):
          raise Exception, 'Attribute value "%s" occurs twice in ' % \
                           (cate_attr2_val) + 'lookup file %s' % \
                           (self.lookup_file_name)

        if (cont_attr_funct not in ['uniform','normal']):
          raise Exception, 'Illegal continuous attribute function ' + \
                           'given: "%s"' % (cont_attr_funct) + \
                           ' in lookup file %s' % (self.lookup_file_name)

        this_cate_val2_dict[cate_attr2_val] = cate_attr2_count

        # Get function parameters from file data
        #
        if (cont_attr_funct == 'uniform'):
          cont_attr_funct_min_val = float(rec_list[3])
          basefunctions.check_is_number('cont_attr_funct_min_val',
                                        cont_attr_funct_min_val)
          cont_attr_funct_max_val = float(rec_list[4])
          basefunctions.check_is_number('cont_attr_funct_max_val',
                                        cont_attr_funct_max_val)

          this_cont_funct_dict[cate_attr2_val] = [cont_attr_funct,
                                                  cont_attr_funct_min_val,
                                                  cont_attr_funct_max_val]
        elif (cont_attr_funct == 'normal'):
          cont_attr_funct_mu =    float(rec_list[3])
          cont_attr_funct_sigma = float(rec_list[4])
          try:
            cont_attr_funct_min_val = float(rec_list[5])
          except:
            cont_attr_funct_min_val = None
          if (cont_attr_funct_min_val != None):
            basefunctions.check_is_number('cont_attr_funct_min_val',
                                          cont_attr_funct_min_val)
          try:
            cont_attr_funct_max_val = float(rec_list[6])
          except:
            cont_attr_funct_max_val = None
          if (cont_attr_funct_max_val != None):
            basefunctions.check_is_number('cont_attr_funct_max_val',
                                          cont_attr_funct_max_val)
          this_cont_funct_dict[cate_attr2_val] = [cont_attr_funct,
                                                  cont_attr_funct_mu,
                                                  cont_attr_funct_sigma,
                                                  cont_attr_funct_min_val,
                                                  cont_attr_funct_max_val]

        list_counter += 1
        if (list_counter < num_file_rows):
          rec_list = lookup_file_data[list_counter]
        else:
          rec_list = []

      # Generate a list of categorical 2 values according to their counts
      #
      cate_attr2_val_list = []

      for (cate_attr2_val, val2_count) in this_cate_val2_dict.iteritems():

        # Append value as many times as given in their counts
        #
        new_list = [cate_attr2_val]* val2_count
        cate_attr2_val_list += new_list

      random.shuffle(cate_attr2_val_list)  # Randomly shuffle the list of values

      cate_val2_dict[cate_attr1_val] = cate_attr2_val_list

      # Store function data for each combination of categorial values
      #
      for cate_attr2_val in this_cont_funct_dict:
        cont_dict_key = cate_attr1_val+'-'+cate_attr2_val
        cont_funct_dict[cont_dict_key] = this_cont_funct_dict[cate_attr2_val]

    # Generate a list of values according to their counts for attribute 1
    #
    cate_attr1_val_list = []

    for (cate_attr1_val, val1_count) in cate_val1_dict.iteritems():

      # Append value as many times as given in their counts
      #
      new_list = [cate_attr1_val]* val1_count
      cate_attr1_val_list += new_list

    random.shuffle(cate_attr1_val_list)  # Randomly shuffle the list of values

    self.cate_attr1_val_list = cate_attr1_val_list
    self.cate_val2_dict =      cate_val2_dict
    self.cont_funct_dict =     cont_funct_dict

  # ---------------------------------------------------------------------------

  def create_attribute_values(self):
    """Method which creates and returns two categorical attribute values and
       one continuous value, where the second categorical value depends upon
       the first value, andthe continuous value depends on both categorical
       values. The two categorical values are randomly selected according to
       the provided frequency distributions, while  the continuous value is
       generated according to the selected function and its parameters.
    """

    assert self.cate_attr1_val_list != []
    assert self.cate_val2_dict != {}
    assert self.cont_funct_dict != {}

    cate_attr1_val = random.choice(self.cate_attr1_val_list)

    cate_attr2_list = self.cate_val2_dict[cate_attr1_val]

    cate_attr2_val = random.choice(cate_attr2_list)

    # Get the details of the function and generate the continuous value
    #
    cont_dict_key = cate_attr1_val+'-'+cate_attr2_val
    funct_details = self.cont_funct_dict[cont_dict_key]
    funct_name = funct_details[0]

    if (funct_name == 'uniform'):
      cont_attr_val = random.uniform(funct_details[1], funct_details[2])

    elif (funct_name == 'normal'):
      mu =      funct_details[1]
      sigma =   funct_details[2]
      min_val = funct_details[3]
      max_val = funct_details[4]
      in_range = False

      cont_attr_val = random.normalvariate(mu, sigma)

      while (in_range == False):
        if (((min_val != None) and (cont_attr_val < min_val)) or
            ((max_val != None) and (cont_attr_val > max_val))):
          in_range = False
          cont_attr_val = random.normalvariate(mu, sigma)
        else:
          in_range = True

      if (min_val != None):
        assert cont_attr_val >= min_val
      if (max_val != None):
        assert cont_attr_val <= max_val

    else:
      raise Exception, ('Illegal continuous function given:', funct_name)

    cont_attr_val_str = basefunctions.float_to_str(cont_attr_val,
                                                   self.continuous_value_type)
 
    return cate_attr1_val, cate_attr2_val, cont_attr_val_str

# =============================================================================

class GenerateContContCompoundAttribute(GenerateCompoundAttribute):
  """Generate two continuous attribute values, where the value of the second
     attribute depends upon the value of the first attribute.

     This for example allows the modelling of:
     - salary values that depend upon age values, or
     - blood pressure values that depend upon age values.

     The arguments that have to be set when this attribute type is initialised
     are:

     continuous1_attribute_name  The name of the first continuous attribute
                                 that will be generated. This name will be
                                 used in the header line to be written into
                                 the output file.

     continuous2_attribute_name  The name of the second continuous attribute
                                 that will be generated. This name will be
                                 used in the header line to be written into
                                 the output file.

     continuous1_funct_name      The name of the function that is used to
                                 randomly generate the values of the first
                                 attribute. Implemented functions currently
                                 are:
                                 - uniform
                                 - normal

     continuous1_funct_param     A list with the parameters required for the
                                 function that generates the continuous values
                                 in the first attribute. They are:
                                 - uniform:  [min_val, max_val]
                                 - normal:   [mu, sigma, min_val, max_val]
                                             (min_val and max_val can be set
                                             to None in which case no minimum
                                             or maximum is enforced)

     continuous2_function        A Python function that has a floating-point
                                 value as input (assumed to be a value
                                 generated for the first attribute) and that
                                 returns a floating-point value (assumed to be
                                 the value of the second attribute).

     continuous1_value_type      The format of how the continuous values in
                                 the first attribute are returned when they
                                 are generated. Possible values are 'int', so
                                 integer values are generated; or 'float1',
                                 'float2', to 'float9', in which case
                                 floating-point values with the specified
                                 number of digits behind the comma are
                                 generated.

     continuous2_value_type      The same as for the first attribute.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    # General attributes for all data set generators
    #
    self.number_of_atttributes = 2
    self.attribute_type =        'Compound-Continuous-Continuous'

    for (keyword, value) in kwargs.items():

      if (keyword.startswith('continuous1_a')):
        basefunctions.check_is_non_empty_string('continuous1_attribute_name',
                                                value)
        self.continuous1_attribute_name = value

      elif (keyword.startswith('continuous2_a')):
        basefunctions.check_is_non_empty_string('continuous2_attribute_name',
                                                value)
        self.continuous2_attribute_name = value

      elif (keyword.startswith('continuous1_funct_n')):
        basefunctions.check_is_non_empty_string('continuous1_funct_name',
                                                value)
        self.continuous1_funct_name = value

      elif (keyword.startswith('continuous1_funct_p')):
        basefunctions.check_is_list('continuous1_funct_param', value)
        self.continuous1_funct_param = value

      elif (keyword.startswith('continuous2_f')):
        basefunctions.check_is_function_or_method('continuous2_function',
                                                   value)
        self.continuous2_function = value

      elif (keyword.startswith('continuous1_v')):
        basefunctions.check_is_non_empty_string('continuous1_value_type',
                                                value)
        basefunctions.check_is_valid_format_str('continuous1_value_type',
                                                value)
        self.continuous1_value_type = value

      elif (keyword.startswith('continuous2_v')):
        basefunctions.check_is_non_empty_string('continuous2_value_type',
                                                value)
        basefunctions.check_is_valid_format_str('continuous2_value_type',
                                                value)
        self.continuous2_value_type = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('continuous1_attribute_name',
                                            self.continuous1_attribute_name)
    basefunctions.check_is_non_empty_string('continuous2_attribute_name',
                                            self.continuous2_attribute_name)
    basefunctions.check_is_non_empty_string('continuous1_funct_name',
                                            self.continuous1_funct_name)
    basefunctions.check_is_list('continuous1_funct_param',
                                self.continuous1_funct_param)
    basefunctions.check_is_function_or_method('continuous2_function',
                                              self.continuous2_function)
    basefunctions.check_is_non_empty_string('continuous1_value_type',
                                            self.continuous1_value_type)
    basefunctions.check_is_non_empty_string('continuous2_value_type',
                                            self.continuous2_value_type)

    if (self.continuous1_attribute_name == self.continuous2_attribute_name):
      raise Exception, 'Both attribute names are the same'

    basefunctions.check_is_valid_format_str('continuous1_value_type',
                                            self.continuous1_value_type)
    basefunctions.check_is_valid_format_str('continuous2_value_type',
                                            self.continuous2_value_type)

    # Check that the function for attribute 2 does return a float value
    #
    funct_ret = self.continuous2_function(1.0)
    if (not isinstance(funct_ret, float)):
      raise Exception, ('Function provided for attribute 2 does not return' + \
                        ' a floating-point value:', type(funct_ret))

    # Check type and number of parameters given for attribute 1 functions
    #
    if (self.continuous1_funct_name not in ['uniform','normal']):
      raise Exception, 'Illegal continuous attribute 1 function given: "%s"' % \
                         (self.continuous1_funct_name)

    # Get function parameters from file data
    #
    if (self.continuous1_funct_name == 'uniform'):
      assert len(self.continuous1_funct_param) == 2

      cont_attr1_funct_min_val = self.continuous1_funct_param[0]
      cont_attr1_funct_max_val = self.continuous1_funct_param[1]
      basefunctions.check_is_number('cont_attr1_funct_min_val',
                                    cont_attr1_funct_min_val)
      basefunctions.check_is_number('cont_attr1_funct_max_val',
                                    cont_attr1_funct_max_val)

      assert cont_attr1_funct_min_val < cont_attr1_funct_max_val

      self.attr1_funct_param = [cont_attr1_funct_min_val,
                                cont_attr1_funct_max_val]

    elif (self.continuous1_funct_name == 'normal'):
      assert len(self.continuous1_funct_param) == 4

      cont_attr1_funct_mu =      self.continuous1_funct_param[0]
      cont_attr1_funct_sigma =   self.continuous1_funct_param[1]
      cont_attr1_funct_min_val = self.continuous1_funct_param[2]
      cont_attr1_funct_max_val = self.continuous1_funct_param[3]

      basefunctions.check_is_number('cont_attr1_funct_mu', cont_attr1_funct_mu)
      basefunctions.check_is_number('cont_attr1_funct_sigma',
                                    cont_attr1_funct_sigma)

      basefunctions.check_is_positive('cont_attr1_funct_sigma',
                                        cont_attr1_funct_sigma)

      if (cont_attr1_funct_min_val != None):
        basefunctions.check_is_number('cont_attr1_funct_min_val',
                                      cont_attr1_funct_min_val)
        assert cont_attr1_funct_min_val <= cont_attr1_funct_mu

      if (cont_attr1_funct_max_val != None):
        basefunctions.check_is_number('cont_attr1_funct_max_val',
                                      cont_attr1_funct_max_val)
        assert cont_attr1_funct_max_val >= cont_attr1_funct_mu

      if (cont_attr1_funct_min_val != None) and \
            (cont_attr1_funct_max_val) != None:
        assert cont_attr1_funct_min_val < cont_attr1_funct_max_val

      self.attr1_funct_param = [cont_attr1_funct_mu,
                                cont_attr1_funct_sigma,
                                cont_attr1_funct_min_val,
                                cont_attr1_funct_max_val]

  # ---------------------------------------------------------------------------

  def create_attribute_values(self):
    """Method which creates and returns two continuous attribute values, with
       the the first continuous value according to the selected function and
       its parameters, and the second value depending upon the first value.
    """

    # Get the details of the function and generate the first continuous value
    #
    funct_name =    self.continuous1_funct_name
    funct_details = self.attr1_funct_param

    if (funct_name == 'uniform'):
      cont_attr1_val = random.uniform(funct_details[0], funct_details[1])

    elif (funct_name == 'normal'):
      mu =      funct_details[0]
      sigma =   funct_details[1]
      min_val = funct_details[2]
      max_val = funct_details[3]
      in_range = False

      cont_attr1_val = random.normalvariate(mu, sigma)

      while (in_range == False):
        if (((min_val != None) and (cont_attr1_val < min_val)) or
            ((max_val != None) and (cont_attr1_val > max_val))):
          in_range = False
          cont_attr1_val = random.normalvariate(mu, sigma)
        else:
          in_range = True

      if (min_val != None):
        assert cont_attr1_val >= min_val
      if (max_val != None):
        assert cont_attr1_val <= max_val

    else:
      raise Exception, ('Illegal continuous function given:', funct_name)

    # Generate the second attribute value
    #
    cont_attr2_val = self.continuous2_function(cont_attr1_val)

    cont_attr1_val_str = basefunctions.float_to_str(cont_attr1_val,
                                                   self.continuous1_value_type)
    cont_attr2_val_str = basefunctions.float_to_str(cont_attr2_val,
                                                   self.continuous2_value_type)

    return cont_attr1_val_str, cont_attr2_val_str


# =============================================================================
# Classes for generating a data set
# =============================================================================

class GenerateDataSet:
  """Base class for data set generation.

     This class and all of its derived classes provide methods that allow the
     generation of a synthetic data set according to user specifications.

     The following arguments need to be set when a GenerateDataSet instance is
     initialised:

     output_file_name     The name of the file that will be generated. This
                          will be a comma separated values (CSV) file. If the
                          file name given does not end with the extension
                          '.csv' then this extension will be added.

     write_header_line    A flag (True or false) indicating if a header line
                          with the attribute (field) names is to be written at
                          the beginning of the output file or not. The default
                          for this argument is True.

     rec_id_attr_name     The name of the record identifier attribute. This
                          name must be different from the names of all other
                          generated attributes. Record identifiers will be
                          unique values for each generated record.

     number_of_records    The number of records that are to be generated. This
                          will correspond to the number of 'original' records
                          that are generated.

     attribute_name_list  The list of attributes (fields) that are to be
                          generated for each record, and the sequence how they
                          are to be written into the output file. Each element
                          in this list must be an attribute name. These names
                          will become the header line of the output file (if
                          a header line is to be written).

     attribute_data_list  A list which contains the actual attribute objects
                          (from the classes GenerateAttribute and
                          GenerateCompoundAttribute and their respective
                          derived classes).

     unicode_encoding     The Unicode encoding (a string name) of the file.
  """

  # ---------------------------------------------------------------------------
  def __init__(self, **kwargs):
    """Constructor, set general attributes.
    """

    # General attributes for all data set generators
    #
    self.output_file_name =    None
    self.write_header_line =   True
    self.rec_id_attr_name =    None
    self.number_of_records =   0
    self.attribute_name_list = None
    self.attribute_data_list = None
    self.unicode_encoding =    None
    self.missing_val_str =     ''

    # The following dictionary will contain the generated records, with the
    # dictionary keys being the record identifiers (unique for each record),
    # while the dictionary values will be lists containing the actual attribute
    # values of these generated records.
    #
    self.rec_dict = {}

    for (keyword, value) in kwargs.items():  # Process keyword arguments

      if (keyword.startswith('output')):
        basefunctions.check_is_non_empty_string('output_file_name', value)

        # Make sure the file extension is correct
        #
        if (value.endswith('.csv') == False):
          value = value + '.csv'
        self.output_file_name = value

      elif (keyword.startswith('write')):
        basefunctions.check_is_flag('write_header_line', value)
        self.write_header_line = value

      elif (keyword.startswith('rec')):
        basefunctions.check_is_non_empty_string('rec_id_attr_name', value)
        self.rec_id_attr_name = value

      elif (keyword.startswith('number')):
        basefunctions.check_is_integer('number_of_records', value)
        basefunctions.check_is_positive('number_of_records', value)
        self.number_of_records = value

      elif (keyword.startswith('attribute_name')):
        basefunctions.check_is_list('attribute_name_list', value)
        if not value:
          raise Exception, 'attribute_name_list is empty: %s' % (type(value)) 
        self.attribute_name_list = value

      elif (keyword.startswith('attribute_data')):
        basefunctions.check_is_list('attribute_data_list', value)
        self.attribute_data_list = value

      elif (keyword.startswith('unicode')):
        basefunctions.check_unicode_encoding_exists(value)
        self.unicode_encoding = value

      else:
        raise Exception, 'Illegal constructor argument keyword: "%s"' % \
              (str(keyword))

    # Check if the necessary variables have been set
    #
    basefunctions.check_is_non_empty_string('output_file_name',
                                            self.output_file_name)
    basefunctions.check_is_non_empty_string('rec_id_attr_name',
                                            self.rec_id_attr_name)
    basefunctions.check_is_integer('number_of_records',
                                   self.number_of_records)
    basefunctions.check_is_positive('number_of_records',
                                    self.number_of_records)
    basefunctions.check_is_list('attribute_name_list',
                                self.attribute_name_list)
    basefunctions.check_is_list('attribute_data_list',
                                self.attribute_data_list)
    basefunctions.check_unicode_encoding_exists(self.unicode_encoding)

    # Remove potential duplicate entries in the attribute data list
    #
    attr_data_set = set()
    new_attr_data_list = []
    for attr_data in self.attribute_data_list:
      if (attr_data not in attr_data_set):
        attr_data_set.add(attr_data)
        new_attr_data_list.append(attr_data)
    self.attribute_data_list = new_attr_data_list

    # Check if the attributes listed in the attribute name list are all
    # different, i.e. no attribute is listed twice, that their names are all
    # different from the record identifier attribute name.
    #
    attr_name_set = set()
    for attr_name in self.attribute_name_list:
      if (attr_name == self.rec_id_attr_name):
        raise Exception, 'Attribute given has the same name as the record ' + \
                         'identifier attribute'
      if (attr_name in attr_name_set):
        raise Exception, 'Attribute name "%s" is given twice' % (attr_name)
      attr_name_set.add(attr_name)
    assert len(attr_name_set) == len(self.attribute_name_list)

    # Check if the attribute names listed in the attribute data list are all
    # different, i.e. no attribute is listed twice, that their names are all
    # different from the record identifier attribute name.
    #
    attr_name_set = set()
    for attr_data in self.attribute_data_list:

      if (attr_data.attribute_type == 'Compound-Categorical-Categorical'):
        attr1_name = attr_data.categorical1_attribute_name
        attr2_name = attr_data.categorical2_attribute_name
        attr3_name = ''

      elif (attr_data.attribute_type == 'Compound-Categorical-Continuous'):
        attr1_name = attr_data.categorical_attribute_name
        attr2_name = attr_data.continuous_attribute_name
        attr3_name = ''

      elif (attr_data.attribute_type == 'Compound-Continuous-Continuous'):
        attr1_name = attr_data.continuous1_attribute_name
        attr2_name = attr_data.continuous2_attribute_name
        attr3_name = ''

      elif (attr_data.attribute_type == \
            'Compound-Categorical-Categorical-Continuous'):
        attr1_name = attr_data.categorical1_attribute_name
        attr2_name = attr_data.categorical2_attribute_name
        attr3_name = attr_data.continuous_attribute_name

      else:  # A single attribute
        attr1_name = attr_data.attribute_name
        attr2_name = ''
        attr3_name = ''

      for attr_name in [attr1_name, attr2_name, attr3_name]:
        if (attr_name != ''):
          if (attr_name == self.rec_id_attr_name):
            raise Exception, 'Attribute given has the same name as the ' + \
                             'record identifier attribute'
          if (attr_name in attr_name_set):
            raise Exception, 'Attribute name "%s" is given twice' % \
                             (attr_name) + ' in attribute data definitions'
          attr_name_set.add(attr_name)

    # Check that there is an attribute definition provided for each attribute
    # listed in the attribute name list.
    #
    for attr_name in self.attribute_name_list:
      found_attr_name = False
      for attr_data in self.attribute_data_list:

        # Get names from attribute data
        #
        if (attr_data.attribute_type == 'Compound-Categorical-Categorical'):
          if ((attr_name == attr_data.categorical1_attribute_name) or \
              (attr_name == attr_data.categorical2_attribute_name)):
            found_attr_name = True
        elif (attr_data.attribute_type == 'Compound-Categorical-Continuous'):
          if ((attr_name == attr_data.categorical_attribute_name) or \
              (attr_name == attr_data.continuous_attribute_name)):
            found_attr_name = True
        elif (attr_data.attribute_type == 'Compound-Continuous-Continuous'):
          if ((attr_name == attr_data.continuous1_attribute_name) or \
              (attr_name == attr_data.continuous2_attribute_name)):
            found_attr_name = True
        elif (attr_data.attribute_type == \
              'Compound-Categorical-Categorical-Continuous'):
          if ((attr_name == attr_data.categorical1_attribute_name) or \
              (attr_name == attr_data.categorical2_attribute_name) or \
              (attr_name == attr_data.continuous_attribute_name)):
            found_attr_name = True
        else:  # A single attribute
          if (attr_name == attr_data.attribute_name):
            found_attr_name = True

      if (found_attr_name == False):
        raise Exception, 'No attribute data available for attribute "%s"' % \
                         (attr_name)

  # ---------------------------------------------------------------------------

  def generate(self):
    """Method which runs the generation process and generates the specified
       number of records.

       This method return a list containing the 'number_of_records' generated
       records, each being a dictionary with the keys being attribute names and
       values the corresponding attribute values.
    """

    attr_name_list = self.attribute_name_list  # Short-hands to increase speed
    rec_dict =       self.rec_dict
    miss_val_str =   self.missing_val_str

    num_rec_num_digit = len(str(self.number_of_records))-1  # For digit padding

    print
    print 'Generate records with attributes:'
    print ' ', attr_name_list
    print

    for rec_id in range(self.number_of_records):
      rec_id_str = 'rec-%s-org' % (str(rec_id).zfill(num_rec_num_digit))

      this_rec_dict = {}  # The generated attribute values (attribute names as
                          # keys, attribute values as values)
      this_rec_list = []  # List of attribute values of the generated data set

      for attr_data in self.attribute_data_list:

        if (attr_data.attribute_type == 'Compound-Categorical-Categorical'):
          attr1_name = attr_data.categorical1_attribute_name
          attr2_name = attr_data.categorical2_attribute_name
          attr1_val, attr2_val = attr_data.create_attribute_values()
          this_rec_dict[attr1_name] = attr1_val
          this_rec_dict[attr2_name] = attr2_val

        elif (attr_data.attribute_type == 'Compound-Categorical-Continuous'):
          attr1_name = attr_data.categorical_attribute_name
          attr2_name = attr_data.continuous_attribute_name
          attr1_val, attr2_val = attr_data.create_attribute_values()
          this_rec_dict[attr1_name] = attr1_val
          this_rec_dict[attr2_name] = attr2_val

        elif (attr_data.attribute_type == 'Compound-Continuous-Continuous'):
          attr1_name = attr_data.continuous1_attribute_name
          attr2_name = attr_data.continuous2_attribute_name
          attr1_val, attr2_val = attr_data.create_attribute_values()
          this_rec_dict[attr1_name] = attr1_val
          this_rec_dict[attr2_name] = attr2_val

        elif (attr_data.attribute_type == \
              'Compound-Categorical-Categorical-Continuous'):
          attr1_name = attr_data.categorical1_attribute_name
          attr2_name = attr_data.categorical2_attribute_name
          attr3_name = attr_data.continuous_attribute_name
          attr1_val, attr2_val, attr3_val = attr_data.create_attribute_values()
          this_rec_dict[attr1_name] = attr1_val
          this_rec_dict[attr2_name] = attr2_val
          this_rec_dict[attr3_name] = attr3_val

        else:  # A single attribute
          attr_name = attr_data.attribute_name
          attr_val = attr_data.create_attribute_value()
          this_rec_dict[attr_name] = attr_val

      # Compile output record
      #
      for attr_name in attr_name_list:
        attr_val = this_rec_dict.get(attr_name, miss_val_str)
        assert isinstance(attr_val, str) or isinstance(attr_val, unicode), \
               attr_val
        this_rec_list.append(attr_val)

      rec_dict[rec_id_str] = this_rec_list

      print 'Generated record with ID: %s' % (rec_id_str)
      print '  %s' % (str(this_rec_list))
      print

    print 'Generated %d records' % (self.number_of_records)
    print
    print '------------------------------------------------------------------'
    print

    return rec_dict

  # ---------------------------------------------------------------------------

  def write(self):
    """Write the generated records into the defined output file.
    """

    rec_id_list = self.rec_dict.keys()
    rec_id_list.sort()

    # Convert record dictionary into a list, with record identifier added
    #
    rec_list = []

    for rec_id in rec_id_list:
      this_rec_list = [rec_id]+self.rec_dict[rec_id]
      rec_list.append(this_rec_list)

    header_list = [self.rec_id_attr_name]+self.attribute_name_list
    basefunctions.write_csv_file(self.output_file_name, self.unicode_encoding,
                                 header_list, rec_list)

# =============================================================================
