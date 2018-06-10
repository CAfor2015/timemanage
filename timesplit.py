#!/urs/bin/env python
# -*- coding: utf-8 -*-

from json import JSONDecoder, JSONEncoder
from time import localtime, strftime, strptime, mktime

_stru='%Y-%m-%d %H:%M'

def _getstrutstr(area):
  '''
  convert seconds to struct time str
  args: second list like [xxxxxxxx, ccccccc]
  return: dict like {"start":"","end":""}
  '''
  _areastr = {}
  _areastr['start'] = strftime(_stru, localtime(area[0]))
  _areastr['end'] = strftime(_stru, localtime(area[1]))
  return _areastr

def _timetosec(timestr):
  '''
  convert timestr to seconds
  args: struct time json string like "{'start':'', 'end':''}"
  return: second list like [xxxxxxx, cccccccc]
  '''
  z = JSONDecoder().decode(timestr)
  _start = mktime(strptime(z['start'], _stru))
  _end = mktime(strptime(z['end'], _stru))
  _area = [_start, _end]
  return _area

def _isinarea(timepoint,timearea):
  '''
  discrimenate whether a timepoint in period of time
  args: timepoint be discrimenated in second format like xxxxxxx
        timearea discrimenated in secomd list format like [xxxxxxx, ccccccc]
  return: True / False (timepoint in / out timearea)
  '''
  if (timepoint>=timearea[0]) and (timearea[1]>=timepoint):
    return True
  else:
    return False

def get_timetable(start, end, occupy_list, slic):
  # parament validate
  available_timeslot = []
  if not start or not end:
    print 'Strat or end time not specified.'
    return available_timeslot

  # convert start and end time into seconds
  try:
    print start, end
    _start_time = mktime(strptime(start, _stru))
    _end_time = mktime(strptime(end, _stru))
  except ValueError:
    print 'Start or end time string format is not correct.'
    return available_timeslot

  # validate whether endtime is latter then starttime provid by arguments 
  if _start_time >= _end_time:
    print 'Start time is after end time.'
    return available_timeslot

  # convert occupy list into seconds and sorted it
  _occupy_time_slot = []
  try:
    for item in occupy_list:
      _start, _end = _timetosec(item)
      _occupy_time_slot.append([_start, _end])
  except ValueError:
    print 'occupy_list`s time string format is not correct.'
    return available_timeslot

  # start end time must insure append to the list[-1] otherwise will have bug
  _occupy_time_slot.append([_start_time, _start_time])
  _occupy_time_slot.append([_end_time, _end_time])
  _sorted_occupy_list = sorted(_occupy_time_slot, key=lambda x: x[0])

  # get useable time slot by parse the occupy list
  _useable_time_slot = []
  for i in range(len(_sorted_occupy_list)-1):
    _pre_end = _sorted_occupy_list[i][1]
    _next_start = _sorted_occupy_list[i+1][0]
    if _isinarea(_pre_end, [_start_time, _end_time]):
      if _pre_end <= _next_start:
        _useable_time_slot.append([_pre_end, _next_start])      
      else:
        _sorted_occupy_list[i+1][1] = _pre_end
        continue
    else:
      break

  # select time slot from useable time fragment list
  if len(_useable_time_slot):
    for item in _useable_time_slot:
      while 1:
        if item[0] + slic <= item[1]:
          available_timeslot.append(_getstrutstr([item[0], item[0] + slic]))
        else:
          break
        item[0] += slic
  else:
    pass

  # convert second time into json string
  _json_available_timeslot = []
  if len(available_timeslot):
    _json_available_timeslot = map(lambda x: JSONEncoder().encode(x), available_timeslot)
      
  print _json_available_timeslot
  return _json_available_timeslot
