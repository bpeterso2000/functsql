functsql
========
An experiment in loosely emulating SQL-style syntax using pure Python
functional programming:

* simple
* stateless
* composable
* lazy
* readable

Inspired by PyToolz: http://toolz.rtfd.org

-----------------------------------------------------------------------------

Current tests are based on the NIST SQL Project.

Reference: http://www.itl.nist.gov/div897/ctg/dm/sql_examples.htm

See the 'tests/nist_tests.py' module for working examples of functsql's syntax.

* The 1st block in the following examples is standard SQL syntax.
* The 2nd block is the equivalent Python functsql syntax.

-----------------------------------------------------------------------------

Example 1::

    SELECT * FROM STATION
    WHERE LAT_N > 39.7;

    ...

    WHERE([('LAT_N', gt, 39.7)], STATION)

-----------------------------------------------------------------------------

Example 2::

    SELECT ID, CITY, STATE FROM STATION;

    ...

    SELECT(('ID', 'CITY', 'STATE'), STATION)

-----------------------------------------------------------------------------

Example 3::

    SELECT ID, CITY, STATE FROM STATION
    WHERE LAT_N > 39.7;

    ...

    QUERY(STATION,
    WHERE(('LAT_N', gt, 39.7)),
    SELECT(('ID', 'CITY', 'STATE')))

-----------------------------------------------------------------------------

Example 4::

    SELECT * FROM STATION, STATS
    WHERE STATION.ID = STATS.ID;

    ...

    JOIN((STATS, 'ID'), STATION)

-----------------------------------------------------------------------------

Example 5::

    SELECT MONTH, ID, RAIN_I, TEMP_F
    FROM STATS 
    ORDER BY MONTH, RAIN_I DESC;

    ...

    QUERY(STATS,
    SELECT(('MONTH', 'ID', 'RAIN_I', 'TEMP_F')),
    ORDER_BY(('MONTH', '-RAIN_I')))

-----------------------------------------------------------------------------

Example 6::

    SELECT LAT_N, CITY, TEMP_F
    FROM STATS, STATION
    WHERE MONTH = 7
    AND STATS.ID = STATION.ID
    ORDER BY TEMP_F;

    ...

    QUERY(STATION,
    JOIN((STATS, 'ID')),
    WHERE(('MONTH', eq, 7)),
    SELECT(('LAT_N', 'CITY', 'TEMP_F')),
    ORDER_BY(('TEMP_F',)))

-----------------------------------------------------------------------------

Example 7::

    SELECT MAX(TEMP_F), MIN(TEMP_F), AVG(RAIN_I), ID 
    FROM STATS 
    GROUP BY ID;

    ...

    QUERY(self.STATS,
    REDUCE_BY('ID', (
        (max, 'TEMP_F'),
        (min, 'TEMP_F'),
        (avg, 'RAIN_I'))))

-----------------------------------------------------------------------------

Example 8::

    SELECT * FROM STATION 
    WHERE 50 < (SELECT AVG(TEMP_F) FROM STATS 
    WHERE STATION.ID = STATS.ID);

    ...

    avg_temp_gt_50 = \
        QUERY(STATS,
        REDUCE_BY('ID', (avg, 'TEMP_F')),
        WHERE(('avg:TEMP_F', gt, 50)),
        SELECT_VALUE('ID'),
        AS(list))

    result = \
        WHERE(('ID', IN, avg_temp_gt_50), STATION)

-----------------------------------------------------------------------------

Example 9::

    UPDATE STATS SET RAIN_I = RAIN_I + 0.01;

    ...

    UPDATE(('RAIN_I', lambda x: x + 0.01), STATS)

-----------------------------------------------------------------------------

Example 10::

    UPDATE STATS SET TEMP_F = 74.9 
    WHERE ID = 44 
    AND MONTH = 7;

    ...

    QUERY(STATS,
    UPDATE_WHERE(('TEMP_F', lambda x: 74.9),
    (('ID', eq, 44), ('MONTH', eq, 7))))

-----------------------------------------------------------------------------

Example 11::

    DELETE FROM STATS
    WHERE MONTH = 7
    OR ID IN (SELECT ID FROM STATION
    WHERE LONG_W < 90);

    ...

    stations = \
        QUERY(STATION,
        WHERE(('LONG_W', lt, 90)),
        SELECT_VALUE('ID'), AS(list))

    result = \
        DELETE_WHERE([
            ('MONTH', eq, 7), ('ID', IN, stations), or_
        ], STATS, rpn=True)

-----------------------------------------------------------------------------

Example 12::

    --- part a ---

    CREATE VIEW METRIC_STATS (ID, MONTH, TEMP_C, RAIN_C) AS 
    SELECT ID, 
    MONTH, 
    (TEMP_F - 32) * 5 /9, 
    RAIN_I * 0.3937 
    FROM STATS;

    ...

    METRIC_STATS = \
        VIEW((
        UPDATE(('TEMP_F', degC, 'TEMP_C')),
        UPDATE(('RAIN_I', cm, 'RAIN_C')),
        SELECT(('ID', 'MONTH', 'TEMP_C', 'RAIN_C'))))

    --- part b ---

    SELECT * FROM METRIC_STATS 
    WHERE TEMP_C < 0 AND MONTH = 1 
    ORDER BY RAIN_C;

    ...

    QUERY(self.STATS, METRIC_STATS,
    WHERE((('TEMP_C', lt, 0), ('MONTH', eq, 1))),
    ORDER_BY(('RAIN_C')))


-----------------------------------------------------------------------------

Example 13::

    #include<stdio.h> 
    #include<string.h> 
    EXEC SQL BEGIN DECLARE SECTION;

    long station_id; 
    long mon; 
    float temp; 
    float rain; 
    char city_name[21]; 
    long SQLCODE;
    EXEC SQL END DECLARE SECTION; 
    main() 
    { 
    /* the CONNECT statement, if needed, goes here */ 
    strcpy(city_name,"Denver"); 
    EXEC SQL SELECT ID INTO :station_id
    FROM STATION 
    WHERE CITY = :city_name;
    if (SQLCODE == 100)
    { 
    printf("There is no station for city %s\n",city_name); 
    exit(0); 
    }
    printf("For the city %s, Station ID is %ld\n",city_name,station_id);  
    printf("And here is the weather data:\n"); 
    EXEC SQL DECLARE XYZ CURSOR FOR
    SELECT MONTH, TEMP_F, RAIN_I 
    FROM STATS 
    WHERE ID = :station_id 
    ORDER BY MONTH;
    EXEC SQL OPEN XYZ; 
    while (SQLCODE != 100) {
    EXEC SQL FETCH XYZ INTO :mon, :temp, :rain; 
    if (SQLCODE == 100)
    printf("end of list\n");
    else
    printf("month = %ld, temperature = %f, rainfall = %f\n",mon,temp,rain);
    }
    EXEC SQL CLOSE XYZ; 
    exit(0); 
    }

    ...

    def get_weather(city, STATION, STATS):
        datafmt = ('month={}, temperature={}, rainfall={}')
        station = QUERY(STATION, WHERE(('CITY', eq, city)), SELECT('ID'))
        if station:
            print('For the city {}, Station ID is {}'.format(city, station))
            print('And here is the weather data:')
            weather = QUERY(STATS, WHERE(('ID', eq, station)), ORDER_BY('MONTH')
            for month in weather:
                datafmt.format(*get(('MONTH', 'TEMP_F', 'RAIN_I')))
            print('end of list')
        else:
            print('There is no station for city {}'.format(city)

    RESULT
    ------
    For the city Denver, Station ID is 44
    And here is the weather data:
    month = 1, temperature = 27.30, rainfall = 0.18
    month = 7, temperature = 74.80, rainfall = 2.11
    end of list
