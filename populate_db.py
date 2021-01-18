from sqlalchemy import create_engine
import pandas as pd
# import clear_tables

engine = create_engine('sqlite:///db.sqlite3')

df_task_types = pd.read_csv('generated/task_types.csv')
df_task_types.index += 1
df_task_types.to_sql(name='tasks_tasktype', con=engine, index=True, index_label="id",  if_exists='append', method='multi')

df_tasks = pd.read_csv('generated/tasks.csv')
df_tasks.index += 1
df_tasks.to_sql(name='tasks_task', con=engine, index=True, index_label="id",  if_exists='append', method='multi')

df_users = pd.read_csv('generated/users.csv')
df_users.index += 1
df_users.to_sql(name='accounts_user', con=engine, index=True, index_label="id",  if_exists='append', method='multi')

df_saved_users = pd.read_csv('generated/saved_users.csv')
df_saved_users.index += len(df_users) + 1
not_null_char_cols = "password,first_name,last_name,username,email,phone_number,post_code,address_line_1,address_line_2,city,county".split(",")
df_saved_users[not_null_char_cols] = df_saved_users[not_null_char_cols].fillna("")
df_saved_users.to_sql(name='accounts_user', con=engine, index=True, index_label="id",  if_exists='append', method='multi')

