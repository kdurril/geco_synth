# Functions that generate a continuous dependent attribute value.
#
# These are functions that require as input a floating-point value (assumed to
# have been generated as the first continuous attribute), and they return a
# floating-point value which will be the dependent continuous attribute
# value.
#
# Examples of such functions are:
# - Blood pressure values that depend upon age values.
# - Salary values that depend upon age values.
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

# -----------------------------------------------------------------------------
#
def blood_pressure_depending_on_age(age):
  """Randomly generate a blood pressure value depending upon the given age
     value.

     It is assumed that for a given age value the blood pressure is normally
     distributed with an average blood pressure of 75 at birth (age 0) and of
     90 at age 100, and standard deviation in blood pressure of 4.
  """

  if ((not isinstance(age, int)) and (not isinstance(age, float))):
    raise Exception, 'Age value given is not a number: %s' % (str(age))

  if (age < 0) or (age > 130):
    raise Exception, 'Age value below 0 or above 130 given'

  avrg_bp = 75.0 + age/100.0

  std_dev_bp = 4.0

  bp = random.normalvariate(avrg_bp, std_dev_bp)

  if bp < 0.0:
    bp = 0.0
    print 'Warning, blood pressure value of 0.0 returned!'

  return bp

# -----------------------------------------------------------------------------

def salary_depending_on_age(age):
  """Randomly generate a salary value depending upon the given age value.

     It is assumed that for a given age value the salary is uniformly
     distributed with an average salary of between 20,000 at age 18 (salary
     will be set to 0 if an age is below 18) and 80,000 at age 60.

     The minimum salary will stay at 10,000 while the maximum salary will
     increase from 30,000 at age 18 to 150,000 at age 60.
  """

  if ((not isinstance(age, int)) and (not isinstance(age, float))):
    raise Exception, 'Age value given is not a number: %s' % (str(age))

  if (age < 0) or (age > 130):
    raise Exception, 'Age value below 0 or above 130 given'

  if (age < 18.0):
    sal = 0.0

  else:
    min_sal = 10000.0
    max_sal = 10000.0 + (age-18.0)*(140000./42)

    sal = random.uniform(min_sal, max_sal)

  return sal

# -----------------------------------------------------------------------------
