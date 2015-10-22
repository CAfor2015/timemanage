#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
url: http://127.0.0.1:5000/timesplit
method: POST
headers: Content-type: application/json
request body:
{"start":"2015-10-10 10:00", "end":"2015-10-10 16:00", "occupy_list":[{"start":"2015-10-10 12:00", "end":"2015-10-10 13:00"}, {"start":"2015-10-10 14:00","end":"2015-10-10 15:00"}], "slic":"900"}
'''

from flask import Flask, jsonify, abort
from flask import make_response, request
from time import localtime, strftime, strptime, mktime
from json import JSONDecoder, JSONEncoder

app = Flask(__name__)

_STRU='%Y-%m-%d %H:%M'

def _getstruttime(area):
  _areastr = {}
  _areastr['start'] = strftime(_STRU, localtime(area[0]))
  _areastr['end'] = strftime(_STRU, localtime(area[1]))
  return _areastr

def _timetosec(timestr):
#	z = JSONDecoder().decode(timestr)
	_start = mktime(strptime(timestr['start'], _STRU))
	_end = mktime(strptime(timestr['end'], _STRU))
	_area = [_start, _end]
	return _area

def _isinarea(timepoint, timearea):
	if (timepoint>=timearea[0]) and (timearea[1]>=timepoint):
		return True
	else:
		return False

@app.route('/timesplit', methods=['POST'])
def get_tiemtable():
	task = request.json

	# convert and validate the parameter start and end
	if task['start'] and task['end']:
		try:
			_end_time = mktime(strptime(task['end'], _STRU))
			_start_time = mktime(strptime(task['start'], _STRU))
		except:
			abort(400)
	else:
		abort(400)
	if _start_time > _end_time:
		abort(400)

	# convert and validate the parameter occupy_list
	_occupy_time_slot = []
	if len(task['occupy_list']) == 0:
		pass
	else:
		try:
			for item in task['occupy_list']:
				_start, _end = _timetosec(item)
				_occupy_time_slot.append([_start, _end])
		except:
			abort(400)
	_occupy_time_slot.append([_start_time, _start_time])
	_occupy_time_slot.append([_end_time, _end_time])
	_sorted_occupy_list = sorted(_occupy_time_slot, key=lambda x: x[0])

	# convert and validate the parameter slic
	if task['slic']:
		slic = int(task['slic'])
	else:
		abort(400)

	# get useable free time slot by parse the occupy list
	_useable_time_slot = []
	try:
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
	except:
		abort(500)

	# select time slot from useable time fragment list
	try:
		available_timeslot = []
		if len(_useable_time_slot):
			for item in _useable_time_slot:
				while 1:
					if item[0] + slic <= item[1]:
						available_timeslot.append(_getstruttime(
							[item[0], item[0]+slic]))
					else:
						break
					item[0] += slic
		else:
			pass
	except:
		abort(500)

	# get response to return
	return jsonify({'the useable time': available_timeslot})


@app.errorhandler(304)
def not_changed(error):
	return manke_response(jsonify({'error': 'Not changed as exespecet'}), 304)

@app.errorhandler(400)
def not_useable(error):
	return make_response(jsonify({'error': 'Not accept body format'}),400)

@app.errorhandler(403)
def refuse_access(error):
	return make_response(jsonify({'error': 'Forbidden'}),403)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed_method(error):
	return make_response(jsonify({'error': 'Not allowed method'}), 405)

@app.errorhandler(422)
def not_useable(error):
	return make_response(jsonify({'error': 'Unprocessable entity'}),422)

@app.errorhandler(429)
def not_useable(error):
	return make_response(jsonify({'error': 'Too many requests'}),429)

@app.errorhandler(500)
def server_errro(error):
	return make_response(jsonify({'error': 'Internal server error'}),500)

if __name__ == '__main__':
	app.run(debug=True)


