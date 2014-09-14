import unittest
from us_states import USStates

class USStatesTest(unittest.TestCase):
  
  def setUp(self):
    self.us_states = USStates() 

  def test_is_valid_code(self):
    self.assertTrue(self.us_states.is_valid_code('CA'))
    self.assertTrue(self.us_states.is_valid_code('TX'))
    self.assertTrue(self.us_states.is_valid_code('OK'))

  def test_is_valid_code_should_be_case_sensitive(self):
    self.assertFalse(self.us_states.is_valid_code('ca'))
    self.assertFalse(self.us_states.is_valid_code('cA'))
    self.assertFalse(self.us_states.is_valid_code('Ca'))

  def test_is_valid_code_invalid_code_does_not_validate(self):    
    self.assertFalse(self.us_states.is_valid_code('XY'))
    
  def test_by_name(self):
    self.assertEqual('CT', self.us_states.by_name('Connecticut'))    
    self.assertEqual('MS', self.us_states.by_name('Mississippi'))    
    self.assertEqual('UT', self.us_states.by_name('Utah'))    

  def test_by_name_unknown_returns_as_none(self):
    self.assertIsNone(self.us_states.by_name('Germany')) 

  def test_by_coords(self):
    # Sacramento, California
    self.assertEqual('CA', self.us_states.by_coords(38.3454, -121.2935)) 

    # Austin, Texas
    self.assertEqual('TX', self.us_states.by_coords(30.25, -97.75)) 

    # Baton Rouge, Lousiana
    self.assertEqual('LA', self.us_states.by_coords(30.4500, -91.1400)) 

  def test_by_coords_unknown_returns_as_none(self):
    # Moscow, Russia
    self.assertIsNone(self.us_states.by_coords(55.7500, 37.6167))

    # Canberra, Australia
    self.assertIsNone(self.us_states.by_coords(-35.3075, 149.1244))

    # New Delhi, India 
    self.assertIsNone(self.us_states.by_coords(28.6139, 77.2089))

if __name__ == '__main__':
    unittest.main()
  
