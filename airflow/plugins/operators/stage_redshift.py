from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
 
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 delimiter="t",
                 ignore_headers=1,
                 file_type = "",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers
        self.file_type = file_type

    def execute(self, context):
        self.log.info('implementing')
        aws_hook = AwsHook(self.aws_credentials_id)
        #credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3:/{}/{}".format(self.s3_bucket, rendered_key)
        region = 'us-west-2'
        maxerror = "acceptinvchars as '^'"
        manifest = 'manifest'
        #json = "FORMAT AS JSON {} "
        songs_copy = ("""    COPY staging_songs 
                             FROM 's3://udacity-dend/song_data'
                             ACCESS_KEY_ID ''
                             SECRET_ACCESS_KEY ''
                             region 'us-west-2'
                             emptyasnull
                             blanksasnull
                             maxerror 10
                             ACCEPTINVCHARS AS '^'
                             format as json 'auto';"""
                     )
        
        redshift.run(songs_copy)
        
        events_copy = (  """ COPY staging_events
                             FROM 's3://udacity-dend/log_data'
                             ACCESS_KEY_ID ''
                             SECRET_ACCESS_KEY ''
                             region 'us-west-2'
                             emptyasnull
                             blanksasnull
                             maxerror 10
                             ACCEPTINVCHARS AS '^'
                             format as json 'auto'; """)
        redshift.run(events_copy)
