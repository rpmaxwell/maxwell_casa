from flask import Flask, Blueprint, request, render_template, flash, jsonify
from sqlalchemy.exc import IntegrityError
from project.dconn import Conn
conn = Conn('home_automation', 'garden')
from datetime import datetime
import json

garden_blueprint = Blueprint('garden', __name__)


@garden_blueprint.route('/record_sensor_reading', methods=['POST'])
def get_sensor_reading():
    row = request.json
    print(row)
    q = """
    INSERT INTO
                garden.sensor_readings_ft
    (device_id, measurement_id, measured_value, dt) 
    VALUES (
        :device_id
        ,:measurement_id
        ,:measured_value
        ,CURRENT_TIMESTAMP
    )
    """
    conn.execute_raw_query(q, params=row)
    return 'OK'


@garden_blueprint.route('/record_device_state', methods=['POST'])
def get_device_state():
    row = request.json
    q = """
    INSERT INTO
                garden.device_event_ft
    (device_id, device_io_state, dt) 
    VALUES (
        :device_id
        ,:device_io_state
        ,CURRENT_TIMESTAMP
    )
    """
    conn.execute_raw_query(q, params=row)
    return 'OK'


def get_device_status():
    q = """
    SELECT 
        dd.device_name
        ,de.device_io_state
        ,de.dt
    FROM 
          garden.device_event_ft de
    JOIN 
            garden.device_dm dd
        ON dd.device_id = de.device_id
    JOIN (
            SELECT
                device_id
                ,MAX(dt) as dt
            FROM 
                garden.device_event_ft
            GROUP BY 1
        ) latest
        ON latest.device_id = dd.device_id
            AND latest.dt = de.dt
    ORDER BY 1;
    """
    results = conn.execute_raw_query(q)
    d = {'location': 'living room', 'message': 'hello'}
    for rec in results:
        name = rec['device_name'].lower()
        d[name] = rec['device_io_state']
        d['{}_dt'.format(name)] = json.dumps(rec['dt'], default=lambda x: x.isoformat())
    return d


def get_latest_sensor_readings():
    q = """
        SELECT 
            CASE WHEN mdm.medium_measured = 'air temperature' THEN 'temperature'
                 WHEN mdm.medium_measured = 'relative humidity' THEN 'humidity'
                 WHEN mdm.medium_measured = 'visible light' THEN 'light_intensity'
                 ELSE NULL END as measurement_name
            ,srf.measured_value
            ,srf.dt 
        FROM 
            garden.sensor_readings_ft srf
            JOIN ( 
                SELECT 
                        mdm.medium_measured
                        ,srf.measurement_id
                        ,MAX(srf.dt) as dt 
                FROM    
                        garden.sensor_readings_ft srf
                JOIN
                        garden.measurement_dm mdm
                    ON mdm.measurement_id = srf.measurement_id
                WHERE
                        srf.measured_value > 0 AND srf.measurement_id IN (1, 2, 3)
                GROUP BY 
                        1, 2) as latest
            ON latest.dt = srf.dt 
                AND latest.measurement_id = srf.measurement_id
        JOIN   
                garden.measurement_dm mdm
            ON 
                srf.measurement_id = mdm.measurement_id
        ORDER BY 1;
    """
    results = conn.execute_raw_query(q)
    d = {'location': 'living room', 'message': 'hello'}
    for rec in results:
        name = rec['measurement_name']
        d[name] = rec['measured_value']
        d['{}_dt'.format(name)] = json.dumps(rec['dt'], default=lambda x: x.isoformat())
    return d