from snowflake import connector

def get_snowflake_connection():
    conn = connector.connect(
        user='RCWA202411',
        password='Rcw1234=',
        account='PGWEBMOBILE',
        warehouse='PROJETRCW',
        database='PROJETRCW_DB',
        schema='ProjetRCWSchema'
    )
    return conn
