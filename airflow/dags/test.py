from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
from airflow.operators.postgres_operator import PostgresOperator
#import create_tables
import datetime
import logging
#import sql

dag = DAG('testtable',
          description='tesing connection',
          start_date=datetime.datetime.now()               
        )
"""
Drop_table = PostgresOperator(
    task_id="Drop_tables",
    dag=Table_dag,
    postgres_conn_id="redshift",
    sql = create_tables.drop_table_queries
    
)

start_operator = PostgresOperator(
    task_id='Begin_execution',
    dag=Table_dag,
    postgres_conn_id='redshift',
    sql="create_table.sql"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=Table_dag,
    table = "staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="/udacity-dend",
    s3_key="song_data"
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=Table_dag,
    table = "staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="/udacity-dend",
    s3_key= "log_data"
)
#Drop_table >> start_operator
#start_operator >>stage_songs_to_redshift 
stage_songs_to_redshift >>stage_events_to_redshift """
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    postgres_conn_id="redshift",
    sql=SqlQueries.songplay_table_insert
)
load_Time_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    postgres_conn_id="redshift",
    sql=SqlQueries.time_table_insert
)
load_songplays_table>>load_Time_dimension_table
