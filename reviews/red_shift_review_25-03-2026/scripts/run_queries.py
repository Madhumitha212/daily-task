from config.get_redshift import get_redshift_client
import time

def run_redshift_query(sql):
    redshift_client = get_redshift_client()
    response = redshift_client.execute_statement(
        Database="telecom_dw",
        Sql=sql,
        WorkgroupName="telecom1-workgroup"
    )
  
    statement_id = response['Id']
    while True:
        status = redshift_client.describe_statement(Id=statement_id)
        # print(status)
        if status['Status'] in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        time.sleep(2)
    if status['Status'] == 'FAILED':
        raise Exception(f"Query failed: {status['Error']}")
    return redshift_client.get_statement_result(Id=statement_id) if "SELECT" in sql.upper() else None

