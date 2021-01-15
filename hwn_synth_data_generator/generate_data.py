import pandas as pd
import random
from datetime import timedelta, datetime
from essential_generators import DocumentGenerator

source_dir = "source/"
res_dir = "generated/"
base_n = 20
next_user_id = 2
task_type_num = 6
task_statuses = ("OP", "EXP", "AS", "CL", "DN")

random.seed(a=12)
gen = DocumentGenerator()

with open(source_dir + "surnames.txt") as f:
    surnames = f.read().splitlines()
with open(source_dir + "names_female.txt") as f:
    f_names = f.read().splitlines()
with open(source_dir + "names_male.txt") as f:
    m_names = f.read().splitlines()
names = f_names + m_names


def generate_persons(is_volunteer=True, n=100):
    global next_user_id
    res = []
    for _ in range(n):
        uid = next_user_id
        next_user_id += 1
        is_requestee = not is_volunteer
        name = random.choice(names)
        surname = random.choice(surnames)
        person = [uid, name, surname, is_volunteer, is_requestee]
        if is_volunteer:
            dbs = random.randrange(2)
            person.append(bool(dbs))
        res.append(person)
    return res


def gen_random_time(start, end):
    return start + timedelta(hours=random.randint(1, (end - start).total_seconds() // 3600))


def gen_random_period(rel_start_hours, rel_end_hours):
    now = datetime.now()
    start, end = now + timedelta(hours=rel_start_hours), now + timedelta(hours=rel_end_hours)
    t1, t2 = gen_random_time(start, end), gen_random_time(start, end)
    return min((t1, t2)), max((t1, t2))


def generate_tasks(n=300):
    res = []
    for _ in range(n):
        dbs_needed = False  # TODO hardcoded for now
        type_id = random.randrange(1, task_type_num + 1)
        description = gen.sentence()
        owner_id = random.randrange(req_id_first, req_id_last + 1)
        volunteer_id = pd.NA
        status = random.choice(task_statuses)
        if status in ["AS", "DN"]:
            volunteer_id = random.randrange(vol_id_first, vol_id_last + 1)
        if status == "EXP":
            start_time, end_time = gen_random_period(-300, 0)
        elif status in ["AS", "OP"]:
            start_time, end_time = gen_random_period(-100, 500)
        elif status == "DN":
            start_time, end_time = gen_random_period(-500, 100)
        elif status == "CL":
            start_time, end_time = gen_random_period(-300, 300)
        task = (type_id, owner_id, volunteer_id, status, start_time, end_time, dbs_needed, description)
        res.append(task)
    return res

# generate person lists: volunteers and requestees
# ids of volunteers are in range (1..base_n)
vol_id_first = next_user_id
volunteers = generate_persons(is_volunteer=True, n=base_n)
vol_id_last, req_id_first = next_user_id - 1, next_user_id
requestees = generate_persons(is_volunteer=False, n=base_n * 5)
req_id_last = next_user_id - 1

# generate tasks
tasks = generate_tasks(n=base_n * 15)

# create dataframe from generated persons
person_cols = ["id", "first_name", "last_name", "is_volunteer", "is_requestee"]
req_cols = person_cols
vol_cols = person_cols + ["dbs"]
task_cols = "type_id", "owner_id", "volunteer_id", "status", \
            "start_time", "end_time", "dbs_needed", "description"

req_df = pd.DataFrame(requestees, columns=req_cols)
vol_df = pd.DataFrame(volunteers, columns=vol_cols)
task_df = pd.DataFrame(tasks, columns=task_cols)

req_df.to_csv(res_dir + "requestees.csv", index=False)
vol_df.to_csv(res_dir + "volunteers.csv", index=False)
task_df.to_csv(res_dir + "tasks.csv", index=False)
