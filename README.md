# DataAnalytics

## Environments

  python 3.7

  Django 2


## Run project
```sh
# change database settings from conf.py in import_database script

# open first terminal and install virtual environment & all packages in Import_Database script directory
$ virtualenv venv --system-site-packages
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python drop.py

# change database settings from settings.py in DataDashboard directory

# open second terminal and install virtual environment & all packages in DataDashboard directory
$ virtualenv venv --system-site-packages
$ source venv/bin/activate
$ pip install -r requirements.txt

# run migration
$ python manage.py migrate

# go to first terminal and run main.py
$ python main.py

# after import all records, create super user for dashboard app in second terminal
$ python manage.py createsuperuser

# run server in second terminal
$ python manage.py runserver

```

Thanks for reading the project
<Dinesh>
