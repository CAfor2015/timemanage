#!/urs/bin/env python
# -*- coding: utf-8 -*-

'''
__author__='zhenyu'
'''

import unittest
from timesplit import get_timetable

class TimeTableTestCase(unittest.TestCase):
  
  def test_start_end_not_given(self):
    time_table = get_timetable(None, None, [], 1800)
    self.assertEqual(0, len(time_table))

  def test_start_latter_then_end(self):
    time_table = get_timetable('2015-10-11 11:30', '2015-10-10 14:00',
                               ['{"start":"2015-10-10 12:00","end":"2015-10-10 12:30"}'],
                               1800)
    self.assertEqual(0, len(time_table))

  def test_time_not_in_right_fromat(self):
    time_table = get_timetable('2015-10-10', '2015-10-10 14:00:00',
                               ['{"start":"2015-10-10 12:00","end":"2015-10-10 12:30"}'],
                               1800)
    self.assertEqual(0, len(time_table))

  def test_time_all_occupy(self):
    time_table = get_timetable('2015-10-10 11:00', '2015-10-10 14:00',
                               ['{"start":"2015-10-10 11:00", "end":"2015-10-10 14:00"}'],
                               1800)
    self.assertEqual(0, len(time_table))

  def test_tiem_over_occupy(self):
    time_table = get_timetable('2015-10-10 11:00', '2015-10-10 14:00',
                               ['{"start":"2015-10-09 11:00", "end":"2015-10-10 15:00"}'],
                               1800)
    self.assertEqual(0, len(time_table))

  def test_time_normal(self):
    time_table = get_timetable('2015-10-10 10:00', '2015-10-10 16:00',
                               ['{"start":"2015-10-10 12:00", "end":"2015-10-10 14:00"}'],
                               1800)
    self.assertEqual(8, len(time_table))

  def test_diffrent_slice(self):
    time_table = get_timetable('2015-10-10 10:00', '2015-10-10 16:00',
                               ['{"start":"2015-10-10 12:00", "end":"2015-10-10 14:00"}'],
                               900)
    self.assertEqual(16, len(time_table))


if __name__ == '__main__':
  unittest.main()
