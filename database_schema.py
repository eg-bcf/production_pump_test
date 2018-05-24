import sqlite3
from sqlalchemy import *

db = create_engine('sqlite:///pump.db')
db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

pumps = Table('pumps', metadata,
    Column('board', String),
    Column('operator', String),
    Column('date', REAL),#how
    Column('serial_number', Integer),
    Column('pump_description', String),
    Column('customer', String),
    Column('purchase_order', String),
    Column('velocity', Integer),
    Column('acceleration', Integer),
    Column('type', String),
    Column('size', Integer),
    Column('piston', String),
    Column('head', String),
    Column('seal', String),
    Column('port_size', Integer),
    Column('prime_port', Integer),
    Column('tpi', Integer),
    Column('home_position', Integer),
    Column('valve', Integer),
    Column('sequential', Boolean),
    Column('dispense_percent', REAL),
    Column('dispense_1', REAL),
    Column('dispense_2', REAL),
    Column('dispense_3', REAL),
    Column('dispense_4', REAL),
    Column('dispense_5', REAL),
    Column('dispense_6', REAL),
    Column('dispense_7', REAL),
    Column('dispense_8', REAL),
    Column('dispense_9', REAL),
    Column('dispense_10', REAL),
    Column('backlash_value', REAL),
    Column('average', REAL),
    Column('stdev', REAL),
    Column('cv', REAL),
    Column('target', REAL),
    Column('variation', REAL),
    Column('test_description', Text)
)
pumps.create()
