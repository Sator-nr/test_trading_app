from sqlalchemy import Table, Column, MetaData, Integer, String, TIMESTAMP

metadata = MetaData()

operation = Table(
    'operation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quantity', String),
    Column('figi', String),
    Column('instrument_type', String, nullable=False),
    Column('date', TIMESTAMP),
    Column('type', String)
)