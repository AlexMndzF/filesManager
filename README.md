# File Manager

### Run steps:

1.Install requirements: <br>
```
python -m pip install -r filesManager/requirements.txt
```

2.Make sure the folder is created: <br>
```
Windows: C:\SGCF
Ubuntu/Mac: /opt/SGCF
```

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
6. Run server: <br> 
```
python manage.py runserver -h 0.0.0.0 -p 8080
```