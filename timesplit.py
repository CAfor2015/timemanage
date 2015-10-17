#!/urs/bin/env python
# -*- coding: utf-8 -*-

__author__='wangzhenyu'


from json import JSONDecoder, JSONEncoder
from time import localtime, strftime, strptime, mktime

_stru='%Y-%m-%d %H:%M'

def _getstrutstr(area):
  '''
  convert seconds to timestr 
  '''
  _areastr = {}
  _areastr['start'] = strftime(_stru, localtime(area[0]))
  _areastr['end'] = strftime(_stru, localtime(area[1]))
  return _areastr

def _timetosec(timestr):
  '''
  convert timestr to seconds
  '''
  z = JSONDecoder().decode(timestr[0])
  _start = mktime(strptime(z['start'], _stru))
  _end = mktime(strptime(z['end'], _stru))
  _area = [_start, _end]
  return _area

def _isinarea(timepoint,timearea):
  if (timepoint>=timearea[0]) and (timearea[1]>=timepoint):
    return True
  else:
    return False

def _isoutarea(timepoint,timearea):
  if (timepoint<=timearea[0]) or (timearea[1]<=timepoint):
    return True
  else:
    return False

def _getfreetime(timearea, busyarea, splitsec):
  '''
  generator that judge whether an timearea could be return.
  of course the main judging logic is in this part
  '''
  _free_time_s = timearea[0]
  _free_time_e = timearea[0]+splitsec
  while _isinarea(_free_time_e, timearea):
    _areanow = [_free_time_s, _free_time_e]
    if _isoutarea(busyarea[0]+1, _areanow) and _isoutarea(busyarea[1]-1, _areanow):
      if _isoutarea(_free_time_s, busyarea) and _isoutarea(_free_time_e, busyarea):
        yield _areanow
    else:
      pass
    _free_time_s += splitsec
    _free_time_e += splitsec

def get_timetable(start, end, occupy_list, slice):
  available_timeslot = []
  if not start or not end:
    print 'Strat or end time not specified.'
    return available_timeslot

  try:
    _start_time = mktime(strptime(start, _stru))
    _end_time = mktime(strptime(end, _stru))
  except ValueError:
    print 'Start or end time string format is not crrenct.'
    return available_timeslot

  if _start_time >= _end_time:
    print 'Start time is after end time.'
    return available_timeslot

  _outservertime = _timetosec(occupy_list)
  
  a = _getfreetime([_start_time, _end_time], _outservertime, slice)
  while 1:
    try:
      available_timeslot.append(JSONEncoder().encode(_getstrutstr(a.next())))
    except StopIteration:
      break
  return available_timeslot
    
