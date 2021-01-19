import pandas as pd
import random
from datetime import timedelta, datetime, date
from string import ascii_letters
from essential_generators import DocumentGenerator
from faker import Faker

source_dir = "source/"
res_dir = "generated/"

base_n = 20
user_count = 0
task_type_num = 6
task_statuses = ("OP", "EXP", "AS", "CL", "DN")
person_cols = ["first_name", "last_name", "uid", "email", "password", "date_of_birth",
               "phone_number", "post_code", "date_joined", "is_active", "is_staff",
               "is_superuser", "is_volunteer", "dbs", "username", "city", "county",
               "address_line_1", "address_line_2"]
task_cols = ["task_type_id", "description", "requestee_id", "volunteer_id", "status",
            "start_time", "end_time", "min_duration", "dbs_required"]

random.seed(a=12)
gen = DocumentGenerator()
Faker.seed(0)
fake = Faker("en_GB")


with open(source_dir + "surnames.txt") as f:
    surnames = f.read().splitlines()
with open(source_dir + "names_female.txt") as f:
    f_names = f.read().splitlines()
with open(source_dir + "names_male.txt") as f:
    m_names = f.read().splitlines()
names = f_names + m_names


def generate_persons(is_volunteer=True, n=100):
    global user_count
    res = []
    for _ in range(n):
        user_count += 1
        name = random.choice(names)
        surname = random.choice(surnames)
        uid = "".join([random.choice(ascii_letters) for _ in range(10)])
        email = gen.email()
        password = "".join([random.choice(ascii_letters) for _ in range(20)])
        dob = date(1920, 1, 1) + timedelta(days=random.randrange(30000))
        # phone_number = f'0{random.choice((1,2,3,7))} + {"".join([random.randrange(10) for _ in range(10)])}'
        phone_number = fake.phone_number()
        post_code = fake.postcode()
        is_superuser = False
        is_staff = False
        date_joined = datetime.now()
        is_active = True
        username = email
        # TODO generate address
        city, county, address_line_1, address_line_2 = '','','',''
        dbs = random.randrange(2) if is_volunteer else False

        person = [name, surname, uid, email, password, dob, phone_number, post_code,
                  date_joined, is_active, is_staff, is_superuser, is_volunteer, dbs,
                  username, city, county, address_line_1, address_line_2]
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
        dbs_required = False  # TODO hardcoded for now
        min_duration = 0    # TODO hardcoded for now
        task_type_id = random.randrange(1, task_type_num + 1)
        description = gen.sentence()
        requestee_id = random.randrange(vol_count + 1, user_count + 1)
        volunteer_id = pd.NA
        status = random.choice(task_statuses)
        if status in ["AS", "DN"]:
            volunteer_id = random.randrange(1, vol_count + 1)
        if status == "EXP":
            start_time, end_time = gen_random_period(-300, 0)
        elif status in ["AS", "OP"]:
            start_time, end_time = gen_random_period(-100, 500)
        elif status == "DN":
            start_time, end_time = gen_random_period(-500, 100)
        elif status == "CL":
            start_time, end_time = gen_random_period(-300, 300)
        task = (task_type_id, description, requestee_id, volunteer_id, status,
                start_time, end_time, min_duration, dbs_required)
        res.append(task)
    return res


# generate users lists: volunteers and requestees
# ids of volunteers are in range (1..n)
volunteers = generate_persons(is_volunteer=True, n=base_n)
vol_count = user_count
requestees = generate_persons(is_volunteer=False, n=base_n * 5)
users = volunteers + requestees

# generate tasks
tasks = generate_tasks(n=base_n * 15)

# create dataframe from generated persons
user_df = pd.DataFrame(users, columns=person_cols)
task_df = pd.DataFrame(tasks, columns=task_cols)

user_df.to_csv(res_dir + "users.csv", index=False)
task_df.to_csv(res_dir + "tasks.csv", index=False)
