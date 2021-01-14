import pandas as pd
import random
import source.admin_record

source_dir = "source/"
res_dir = "generated/"
base_n = 200
next_user_id = 2

random.seed(a=5)

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


def generate_tasks(n=150):
    res = []
    for _ in range(n):
    #     TODO
        task = None
        res.append(task)
    return res

# generate person lists: volunteers and requestees
# ids of volunteers are in range (1..base_n)
vol_id_first = next_user_id
volunteers = generate_persons(is_volunteer=True, n=base_n)
vol_id_last, req_id_first = next_user_id - 1, next_user_id
requestees = generate_persons(is_volunteer=False, n=base_n*2)
req_id_last = next_user_id - 1

# create dataframe from generated persons
person_cols = ["id", "first_name", "last_name", "is_volunteer", "is_requestee"]
req_cols = person_cols
vol_cols = person_cols + ["dbs"]

req_df = pd.DataFrame(requestees, columns=req_cols)
vol_df = pd.DataFrame(volunteers, columns=vol_cols)

req_df.to_csv(res_dir + "requestees.csv", index=False)
vol_df.to_csv(res_dir + "volunteers.csv", index=False)
