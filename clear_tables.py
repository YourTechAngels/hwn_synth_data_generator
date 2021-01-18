from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


engine = create_engine('sqlite:///db.sqlite3')
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
# print(session.query(User).all())
session.query(Task).delete()
session.query(TaskType).delete()
session.query(User).delete()
session.commit()
print("---------------------------------")
print("Number of records in User table: ", session.query(User).count())
print("Number of records in Task table: ", session.query(Task).count())
print("Number of records in TaskType table: ", session.query(TaskType).count())
