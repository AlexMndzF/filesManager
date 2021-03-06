# File Manager

### Run steps:

1.Install requirements: <br>
```
python -m pip install -r requirements.txt
```

2.Create the folder: <br>
```
Windows: C:\SGDF
Ubuntu/Mac: /opt/SGDF
```
* 2.1.For ubuntu/Mac execute: ```sudo mkdir /opt/SGDF```
* 2.2.Ubuntu/Mac needs special permissions through the folder, execute: ```sudo chmod 777 /opt/SGDF```

3.Drop tables: <br>
```
python manage.py drop_tables
```

4. Create tables: <br>
```
python manage.py create_tables
```
5. Insert users data: <br>
```
python manage.py add_data_tables
```
* The script allows you to enter another password for admin or user. You can skip this by pressing enter, the defaults users and passwords are:
    ````
  User: admin -> Password: admin
  User: user -> Password: user
  ````
6. Run server: <br> 
```
python manage.py runserver -h 0.0.0.0 -p 8080
```

## Test:

1. Run the command:
```
python -m unittest
```
2. Drop the tables:
```
python manage.py drop_tables
```