import numpy as np
import pandas as pd
import os
import datetime as dt
from datetime import datetime
from dotenv import load_dotenv
from clickhouse_driver import Client
from data_wrapper import db_wrapper

load_dotenv()

HOST = os.getenv('HOST')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
CA = os.getenv('CA')
READONLY = os.getenv('READONLY')
ANALYTICAL_HOST = os.getenv('ANALYTICAL_HOST')
ANALYTICAL_PASSWORD = os.getenv('ANALYTICAL_PASSWORD')

# Подключаемся к боевой базе данных
wrap = db_wrapper.ClickHouseWrapper(host=HOST, user=USERNAME, password=PASSWORD, ca=CA)
# Подключаемся к аналитической БД с правами загрузки
client = Client(host=ANALYTICAL_HOST, user=USERNAME, password=ANALYTICAL_PASSWORD, ca_certs=CA, secure=True)


sensors = [
# Потребление ввода холодильной машины
{
    "db": "genesis_arena", "name": "map12e_142", "measurement": "Total AP energy", 
    "channel": 1, "phase": 0, "name_in_df": "cm_consumption", "mode": "max-min"
},
# Мгновенная мощность компрессоров
{
    "db": "genesis_arena", "name": "map12e_142", "measurement": "Total P", 
    "channel": 2, "phase": 0, "name_in_df": "state1", "mode": "max-min"
},
{
    "db": "genesis_arena", "name": "map12e_142", "measurement": "Total P",
    "channel": 3, "phase": 0, "name_in_df": "state2", "mode": "max-min"
},
{
    "db": "genesis_arena", "name": "map12e_142", "measurement": "Total P",
    "channel": 4, "phase": 0, "name_in_df": "state3", "mode": "max-min"
},
{
    "db": "genesis_arena", "name": "map12e_145", "measurement": "Total P",
    "channel": 1, "phase": 0, "name_in_df": "state4", "mode": "max-min"
},
# Мгновенная мощность конденсаторов
{
    "db": "genesis_arena", "name": "map12e_23", "measurement": "Total P", 
    "channel": 1, "phase": 0, "name_in_df": "condensator4", "mode": "mean"
},
{
    "db": "genesis_arena", "name": "map12e_49", "measurement": "Total P", 
    "channel": 2, "phase": 0, "name_in_df": "condensator1", "mode": "mean"
},
{
    "db": "genesis_arena", "name": "map12e_49", "measurement": "Total P", 
    "channel": 3, "phase": 0, "name_in_df": "condensator2", "mode": "mean"
},
{
    "db": "genesis_arena", "name": "map12e_49", "measurement": "Total P", 
    "channel": 4, "phase": 0, "name_in_df": "condensator3", "mode": "mean"
},
# Мощность циркуляционного насоса
{
    "db": "genesis_arena", "name": "map12e_145", "measurement": "Total P", 
    "channel": 3, "phase": 0, "name_in_df": "power_pump", "mode": "mean"
},
# Температура поверхности льда
{
    "db": "genesis_arena", "name": "msw-v3_2", "measurement": "Temperature", 
    "channel": 0, "phase": 0, "name_in_df": "temp_ice", "mode": "mean"
},
# Внешняя температура
{
    "db": "genesis_arena", "name": "weather_owm", "measurement": "Temperature",
    "channel": 0, "phase": 0, "name_in_df": "temp_outside", "mode": "mean"
},
# Внешняя влажность
{
    "db": "genesis_arena", "name": "weather_owm", "measurement": "Humidity",
    "channel": 0, "phase": 0, "name_in_df": "hum_outside", "mode": "mean"
},
# Внутреняя температура 
{
    "db": "genesis_arena", "name": "msw-v3_175", "measurement": "Temperature",
    "channel": 0, "phase": 0, "name_in_df": "temp_inside", "mode": "mean"
},
# Внутреняя влажность 
{
    "db": "genesis_arena", "name": "msw-v3_175", "measurement": "Humidity",
    "channel": 0, "phase": 0, "name_in_df": "hum_inside", "mode": "mean"
}
]

client.execute('USE akarmanov_test_db')
start = client.execute('SELECT MAX(time) FROM genesis_arena_prediction_ice')[0][0]

start = start - dt.timedelta(hours=3, minutes=10)
end = dt.datetime.now().replace(microsecond=0, second=0) - dt.timedelta(hours=3)
presample = dt.timedelta(minutes=1)

df = wrap.get_particular_sensors(start, end, sensors, presample_time=presample,  without_confidence=True)

df = (df
 .tz_localize(None)
 .reset_index(names=['time'])
 .assign(temp_ice=lambda df: np.where(df['temp_ice'].between(-6, 3), df['temp_ice'], np.NaN))
 .pipe(lambda df: df.ffill().bfill())
 .assign(power_compressors=lambda df: df[['state1', 'state2', 'state3', 'state4']].sum(axis=1))
 .assign(power_condensators=lambda df: df[['condensator1', 'condensator2', 'condensator3', 'condensator4']].sum(axis=1))
 .assign(prediction_temp_ice=lambda df: np.NaN)
)

client.execute('USE akarmanov_test_db')
client.insert_dataframe('''
INSERT INTO "genesis_arena_prediction_ice" (
    time, temp_ice, power_compressors, power_condensators, power_pump,
    cm_consumption, temp_outside, temp_inside, hum_outside, hum_inside,
    prediction_temp_ice
) VALUES
''',
    df[['time', 'temp_ice', 'power_compressors', 'power_condensators', 'power_pump',
    'cm_consumption', 'temp_outside', 'temp_inside', 'hum_outside', 'hum_inside',
    'prediction_temp_ice']],
    settings=dict(use_numpy=True)
)