"""
Based on http://www.itl.nist.gov/div897/ctg/dm/sql_examples.htm
Reference docs/examples.rst for test numbers.
"""
import unittest

from functsql.query import *
from functsql.dictsql import *


def avg(seq, digits=2):
    if iter(seq) is seq:
        seq = list(seq)
    return round(sum(seq) / len(seq), digits)


class NISTtests(unittest.TestCase):

    def setUp(self):
        self.STATION = (
            {"ID": 13, "CITY": "Phoenix", "STATE": "AZ", "LAT_N": 33, "LONG_W": 112},
            {"ID": 44, "CITY": "Denver",  "STATE": "CO", "LAT_N": 40, "LONG_W": 105},
            {"ID": 66, "CITY": "Caribou", "STATE": "ME", "LAT_N": 47, "LONG_W": 68}
        )

        self.STATS = (
            {"ID": 13, "MONTH": 1, "TEMP_F": 57.4, "RAIN_I": 0.31},
            {"ID": 13, "MONTH": 7, "TEMP_F": 91.7, "RAIN_I": 5.15},
            {"ID": 44, "MONTH": 1, "TEMP_F": 27.3, "RAIN_I": 0.18},
            {"ID": 44, "MONTH": 7, "TEMP_F": 74.8, "RAIN_I": 2.11},
            {"ID": 66, "MONTH": 1, "TEMP_F": 6.7,  "RAIN_I": 2.10},
            {"ID": 66, "MONTH": 7, "TEMP_F": 65.8, "RAIN_I": 4.52}
        )

    def test_1(self):
        result = WHERE([('LAT_N', gt, 39.7)], self.STATION)
        self.assertEqual(tuple(result), (
            {"ID": 44, "CITY": "Denver",  "STATE": "CO", "LAT_N": 40, "LONG_W": 105},
            {"ID": 66, "CITY": "Caribou", "STATE": "ME", "LAT_N": 47, "LONG_W": 68}
        ))

    def test_2(self):
        result = SELECT(('ID', 'CITY', 'STATE'), self.STATION)
        self.assertEqual(tuple(result), (
            {"ID": 13, "CITY": "Phoenix", "STATE": "AZ"},
            {"ID": 44, "CITY": "Denver",  "STATE": "CO"},
            {"ID": 66, "CITY": "Caribou", "STATE": "ME"}
        ))

    def test_3(self):
        result = QUERY(self.STATION,
                 WHERE([('LAT_N', gt, 39.7)]),
                 SELECT(('ID', 'CITY', 'STATE')))
        self.assertEqual(tuple(result), (
            {"ID": 44, "CITY": "Denver",  "STATE": "CO"},
            {"ID": 66, "CITY": "Caribou", "STATE": "ME"}
        ))

    def test_4(self):
        result = JOIN((self.STATS, 'ID'), self.STATION)
        self.assertEqual(tuple(result), (
            {'ID': 13, 'CITY': 'Phoenix', 'STATE': 'AZ', 'LAT_N': 33, 'LONG_W': 112,
             'MONTH': 1, 'TEMP_F': 57.4, 'RAIN_I': 0.31},
            {'ID': 13, 'CITY': 'Phoenix', 'STATE': 'AZ', 'LAT_N': 33, 'LONG_W': 112,
             'MONTH': 7, 'TEMP_F': 91.7, 'RAIN_I': 5.15},
            {'ID': 44, 'CITY': 'Denver',  'STATE': 'CO', 'LAT_N': 40, 'LONG_W': 105,
             'MONTH': 1, 'TEMP_F': 27.3, 'RAIN_I': 0.18},
            {'ID': 44, 'CITY': 'Denver',  'STATE': 'CO', 'LAT_N': 40, 'LONG_W': 105,
             'MONTH': 7, 'TEMP_F': 74.8, 'RAIN_I': 2.11},
            {'ID': 66, 'CITY': 'Caribou', 'STATE': 'ME', 'LAT_N': 47, 'LONG_W': 68,
             'MONTH': 1, 'TEMP_F': 6.7,  'RAIN_I': 2.1},
            {'ID': 66, 'CITY': 'Caribou', 'STATE': 'ME', 'LAT_N': 47, 'LONG_W': 68,
             'MONTH': 7, 'TEMP_F': 65.8, 'RAIN_I': 4.52}
        ))

    def test_5(self):
        result = QUERY(self.STATS,
                 SELECT(('MONTH', 'ID', 'RAIN_I', 'TEMP_F')),
                 ORDER_BY(('MONTH', '-RAIN_I')))
        self.assertEqual(tuple(result), (
            {"ID": 66, "MONTH": 1, "TEMP_F": 6.7, "RAIN_I": 2.10},
            {"ID": 13, "MONTH": 1, "TEMP_F": 57.4, "RAIN_I": 0.31},
            {"ID": 44, "MONTH": 1, "TEMP_F": 27.3, "RAIN_I": 0.18},
            {"ID": 13, "MONTH": 7, "TEMP_F": 91.7, "RAIN_I": 5.15},
            {"ID": 66, "MONTH": 7, "TEMP_F": 65.8, "RAIN_I": 4.52},
            {"ID": 44, "MONTH": 7, "TEMP_F": 74.8, "RAIN_I": 2.11}
        ))

    def test_6(self):
        result = QUERY(self.STATION,
                 JOIN((self.STATS, 'ID')),
                 WHERE([('MONTH', eq, 7)]),
                 SELECT(('LAT_N', 'CITY', 'TEMP_F')),
                 ORDER_BY(('TEMP_F',)))
        self.assertEqual(tuple(result), (
            {'CITY': 'Caribou', 'LAT_N': 47, 'TEMP_F': 65.8},
            {'CITY': 'Denver',  'LAT_N': 40, 'TEMP_F': 74.8},
            {'CITY': 'Phoenix', 'LAT_N': 33, 'TEMP_F': 91.7}
        ))

    def test_7(self):
        result = QUERY(self.STATS,
                 REDUCE_BY('ID', (
                     (max, 'TEMP_F'),
                     (min, 'TEMP_F'),
                     (avg, 'RAIN_I'))))
        self.assertEqual(tuple(result), (
            {'avg:RAIN_I': 3.31, 'ID': 66, 'max:TEMP_F': 65.8, 'min:TEMP_F': 6.7},
            {'avg:RAIN_I': 1.15, 'ID': 44, 'max:TEMP_F': 74.8, 'min:TEMP_F': 27.3},
            {'avg:RAIN_I': 2.73, 'ID': 13, 'max:TEMP_F': 91.7, 'min:TEMP_F': 57.4}
        ))

    def test_8(self):
        avg_temp_gt_50 = \
             QUERY(self.STATS,
             REDUCE_BY('ID', [(avg, 'TEMP_F')]),
             WHERE([('avg:TEMP_F', gt, 50)]),
             SELECT_VALUES('ID'),
             AS(list))
        result = WHERE([('ID', IN, avg_temp_gt_50)], self.STATION)
        self.assertEqual(tuple(result), (
            {'ID': 13, 'STATE': 'AZ', 'LAT_N': 33, 'CITY': 'Phoenix', 'LONG_W': 112},
            {'ID': 44, 'STATE': 'CO', 'LAT_N': 40, 'CITY': 'Denver',  'LONG_W': 105}
        ))

    def test_9(self):
        result = UPDATE(('RAIN_I', lambda x: round(x + 0.01, 2)), self.STATS)
        self.assertEqual(tuple(result), (
            {'TEMP_F': 57.4, 'RAIN_I': 0.32, 'MONTH': 1, 'ID': 13},
            {'TEMP_F': 91.7, 'RAIN_I': 5.16, 'MONTH': 7, 'ID': 13},
            {'TEMP_F': 27.3, 'RAIN_I': 0.19, 'MONTH': 1, 'ID': 44},
            {'TEMP_F': 74.8, 'RAIN_I': 2.12, 'MONTH': 7, 'ID': 44},
            {'TEMP_F': 6.7,  'RAIN_I': 2.11, 'MONTH': 1, 'ID': 66},
            {'TEMP_F': 65.8, 'RAIN_I': 4.53, 'MONTH': 7, 'ID': 66}
        ))

    def test_10(self):
        result = QUERY(self.STATS,
                 UPDATE_WHERE(('TEMP_F', lambda x: 74.9),
                 (('ID', eq, 44), ('MONTH', eq, 7))))
        self.assertEqual(tuple(result), (
            {'TEMP_F': 57.4, 'MONTH': 1, 'RAIN_I': 0.31, 'ID': 13},
            {'TEMP_F': 91.7, 'MONTH': 7, 'RAIN_I': 5.15, 'ID': 13},
            {'TEMP_F': 27.3, 'MONTH': 1, 'RAIN_I': 0.18, 'ID': 44},
            {'TEMP_F': 74.9, 'MONTH': 7, 'RAIN_I': 2.11, 'ID': 44},
            {'TEMP_F': 6.7,  'MONTH': 1, 'RAIN_I': 2.1,  'ID': 66},
            {'TEMP_F': 65.8, 'MONTH': 7, 'RAIN_I': 4.52, 'ID': 66}
        ))

    def test_11(self):
        stations = QUERY(self.STATION,
                   WHERE([('LONG_W', lt, 90)]),
                   SELECT_VALUES('ID'), AS(list))
        result = DELETE_WHERE([('MONTH', eq, 7), ('ID', IN, stations), or_],
                 self.STATS, rpn=True)
        self.assertEqual(tuple(result), (
            {'MONTH': 1, 'TEMP_F': 57.4, 'RAIN_I': 0.31, 'ID': 13},
            {'MONTH': 1, 'TEMP_F': 27.3, 'RAIN_I': 0.18, 'ID': 44}
        ))

    def test_12(self):
        degC = lambda x: round((x - 32) * 5/9, 2)
        cm = lambda x: round(x * 0.3937, 2)
        METRIC_STATS = VIEW((
                 UPDATE(('TEMP_F', degC, 'TEMP_C')),
                 UPDATE(('RAIN_I', cm, 'RAIN_C')),
                 SELECT(('ID', 'MONTH', 'TEMP_C', 'RAIN_C'))))
        result = METRIC_STATS(self.STATS)
        self.assertEqual(tuple(result), (
            {'TEMP_C': 14.11, 'MONTH': 1, 'ID': 13, 'RAIN_C': 0.12},
            {'TEMP_C': 33.17, 'MONTH': 7, 'ID': 13, 'RAIN_C': 2.03},
            {'TEMP_C': -2.61, 'MONTH': 1, 'ID': 44, 'RAIN_C': 0.07},
            {'TEMP_C': 23.78, 'MONTH': 7, 'ID': 44, 'RAIN_C': 0.83},
            {'TEMP_C': -14.06, 'MONTH': 1, 'ID': 66, 'RAIN_C': 0.83},
            {'TEMP_C': 18.78, 'MONTH': 7, 'ID': 66, 'RAIN_C': 1.78}
         ))
        result = QUERY(self.STATS, METRIC_STATS,
                 WHERE([('TEMP_C', lt, 0), ('MONTH', eq, 1)]),
                 ORDER_BY(('RAIN_C')))
        self.assertEqual(tuple(result), (
            {'TEMP_C': -2.61, 'MONTH': 1, 'ID': 44, 'RAIN_C': 0.07},
            {'TEMP_C': -14.06, 'MONTH': 1, 'ID': 66, 'RAIN_C': 0.83}
        ))

    def test_13(self):
        def get_weather(city, STATION, STATS):
            output = []
            datafmt = ('month = {}, temperature = {}, rainfall = {}')
            station = QUERY(STATION,
                      WHERE([('CITY', eq, city)]),
                      SELECT_VALUES('ID'), AS(list))[0]
            if station:
                output.append('For the city {}, Station ID is {}'.format(city, station))
                output.append('And here is the weather data:')
                weather = QUERY(STATS,
                          WHERE([('ID', eq, station)]),
                          ORDER_BY('MONTH'), AS(list))
                for month in weather:
                    output.append(datafmt.format(
                                 *get(['MONTH', 'TEMP_F', 'RAIN_I'], month)))
                output.append('end of list')
            return output
        result = get_weather('Denver', self.STATION, self.STATS)
        self.assertEqual(result[0],
            'For the city Denver, Station ID is 44')
        self.assertEqual(result[1],
            'And here is the weather data:')
        self.assertEqual(result[2],
            'month = 1, temperature = 27.3, rainfall = 0.18')
        self.assertEqual(result[3],
            'month = 7, temperature = 74.8, rainfall = 2.11')
        self.assertEqual(result[4], 'end of list')
