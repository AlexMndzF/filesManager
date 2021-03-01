# pdfTool

### First steps:

1. Drop tables:
    ``python manage.py drop_tables```
2. Create tables :
    ```python manage.py create_tables```
3. Insert users data:
    ```python manage.py add_data_tables```
4. Run server:
   ```python manage.py runserver -h 0.0.0.0 -p 8080```
   
### Backend Spec:

The application has 4 endpoints:

1. /login/ => Receive the user and password through form, returns a valid token
2. /pdf/ (POST) =>  Endpoint to post a pdf.
3. /pdf/ (GET) => Returns all pdf available on database and not erased (stratus= True).
4. /pdf/\<id>/ (DELETE) => Delete the file of a pdf if the user has permissions, on databse this action only put status= False