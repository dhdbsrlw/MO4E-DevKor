import os
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# 모듈로 만들어서 import 했다. 
# # __init__.py 없으면 모듈로 인식 안되니 주의해라.
from src.quant_algo import get_market_fundamental, select_columns, remove_row_fundamental, rank_fundamental, select_stock, print_selected_stock

seoul_time = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

# default args 따로 지정해서 넣어줘도 된다. 
# 고정값으로 들어가는 값들은 따로 지정해서 넣어줘도 딘다.
default_args = {
    'owner': 'devkor',
    'retries': 3, # 만약 태스크가 하나 실패했을 경우, 언제 다시 재시도할지 그 횟수와 얼마의 시간 차를 두고 실행할 것인지에 관한 것이다.
    'retry_delay': timedelta(minutes=1)
}

# 에어플로우의 시간이 헷갈릴 수 있다. (startdate 와 실제 처음 실행되는 날짜가 다르다.)
# 예: '10시30분-10시40분' 의 데이터를 가지고 처리하고 싶으면, 실행 시작 시간을 10시 40분으로 둬야 한다.
# start_date 와 schedule_interval 관련
with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='중간고사 화이팅~.~',
    schedule_interval=timedelta(minutes=10), 
    start_date=pendulum.datetime(2023, 10, 9, tz=seoul_time), # tz: time zone '서울표준시각'으로 설정
    catchup=False, # 과거의 start date 부터 쭉 build 하라는 요청을 off 시킬 수 있는데, 그것과 관련된 것이다.
    tags=['quant', 'example'] 
) as dag:
    
    # 한 태스크에는 하나의 작업만 들어가도록 해라. 그래야 디버깅을 할 수 있다. 
    get_market_fundamental_task = PythonOperator(
        task_id="get_market_fundamental_task",
        python_callable=get_market_fundamental,
    )

    select_columns_task = PythonOperator(
        task_id="select_columns_task",
        python_callable=select_columns,
    )

    remove_row_fundamental_task = PythonOperator(
        task_id="remove_row_fundamental_task",
        python_callable=remove_row_fundamental,
    )

    rank_fundamental_task = PythonOperator(
        task_id="rank_fundamental_task",
        python_callable=rank_fundamental,
    )

    select_stock_task = PythonOperator(
        task_id="select_stock_task",
        python_callable=select_stock,
    )

    print_selected_stock_task = PythonOperator(
        task_id="print_selected_stock_task",
        python_callable=print_selected_stock,
    )


# 다운스트림으로 태스크 실행
get_market_fundamental_task >> select_columns_task >> remove_row_fundamental_task >> rank_fundamental >> select_stock_task >> print_selected_stock_task
