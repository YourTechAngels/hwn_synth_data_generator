import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import pandas as pd


def clear_tables(engine):
    metadata = MetaData(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    User = Base.classes.accounts_user
    Task = Base.classes.tasks_task
    TaskType = Base.classes.tasks_tasktype
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Number of records in User table: ", session.query(User).count())
    print("Number of records in Task table: ", session.query(Task).count())
    print("Number of records in TaskType table: ", session.query(TaskType).count())
    print("---------------------------------")
    # print(session.query(User).all())
    session.query(Task).delete()
    session.query(TaskType).delete()
    session.query(User).delete()
    session.commit()
    print("Number of records in User table: ", session.query(User).count())
    print("Number of records in Task table: ", session.query(Task).count())
    print("Number of records in TaskType table: ", session.query(TaskType).count())
    print("---------------------------------")


def populate(engine):
    df_task_types = pd.read_csv('generated/task_types.csv')
    df_task_types.index += 1
    df_task_types.to_sql(name='tasks_tasktype', con=engine, index=True, index_label="id",  if_exists='append', method='multi')
    print(f'{len(df_task_types)} task_type entries have been inserted')

    df_tasks = pd.read_csv('generated/tasks.csv')
    df_tasks.index += 1
    df_tasks.to_sql(name='tasks_task', con=engine, index=True, index_label="id",  if_exists='append', method='multi')
    print(f'{len(df_tasks)} task entries have been inserted')

    df_users = pd.read_csv('generated/users.csv')
    not_null_char_cols = "password,first_name,last_name,username,email,phone_number,post_code,address_line_1,address_line_2,city,county".split(
        ",")
    df_users[not_null_char_cols] = df_users[not_null_char_cols].fillna("")
    df_users.index += 1
    df_users.to_sql(name='accounts_user', con=engine, index=True, index_label="id",  if_exists='append', method='multi')
    print(f'{len(df_users)} user entries have been inserted')

    try:
        df_saved_users = pd.read_csv('generated/saved_users.csv')
        df_saved_users.index += len(df_users) + 1
        df_saved_users[not_null_char_cols] = df_saved_users[not_null_char_cols].fillna("")
        df_saved_users.to_sql(name='accounts_user', con=engine, index=True, index_label="id",  if_exists='append', method='multi')
        print(f'{len(df_saved_users)} saved user entries have been inserted')
    except FileNotFoundError:
        print('No saved users to add.')


if __name__ == "__main__":
    to_clear_db = False
    db_path = 'db.sqlite3'

    # parse arguments
    if len(sys.argv) > 1:
        args_to_parse = sys.argv[1:]
        if "-d" in args_to_parse:
            args_to_parse.remove("-d")
            to_clear_db = True
        if args_to_parse:
            db_path = args_to_parse[0]

    engine = create_engine(r'sqlite:///' + db_path)
    if to_clear_db:
        clear_tables(engine)
    sys.exit(populate(engine))
