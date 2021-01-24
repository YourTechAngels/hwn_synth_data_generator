### Description
The aim of this project is to facilitate fake data generation for HelpWhoNeeds project.

### Prerequisite  
SQLite DB with the project schema should be created.
By default file 'db.sqlite3' in this project root folder will be used

### Usage
1. Create venv
2. Run `pip install -r requirements.txt`
3. Activate venv
4. (Optional) To generate data run `python generate_data.py`
5. (Optional) If you have users you wish to keep / insert into the db, 
rename `saved_users_template.csv` into `saved_users.csv` and insert your users data accordingly to the template.
   More than 1 user can be added.
6. To insert data into local SQLITE db run  
   ```python populate_db.py -l [db_path]```  
   where **db_path** - absolute or relative path to your DB file which is to be populated with data.  
         Absolute path should be defined as follows:  
         _Unix/Mac_: `/absolute/path/to/foo.db`
         _Windows_: `C:\path\to\foo.db`
   If `db_path` is not defined than script will search for `db.sqlite3` file in its root folder.  
   ####
   To use any other than sqlite db its configuration should be put into `db_params.json` file according to template.
   After filling it run
   ```python populate_db.py [config_name]```  
   where **config_name** - a name of configuration from `db_params.json`.
   By default HelpWhoNeeds default configuration `aws_mysql` is used.  
   For defaulted config no parameters needed:  
   ```python populate_db.py```
   

#### Notes  
Data from https://namecensus.com as a source of names and surnames.
Probably, later Faker package will be used with this goal 
