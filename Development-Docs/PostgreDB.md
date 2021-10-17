# Database Configuration 

1. Request a DB from [site](https://dbod.web.cern.ch/)
2. Wait for approval and credentials from DB team. 
3. Connect to LxPlus if working from outside the CERN network to run the following commands. 

    * To connect to psql client and change password using creds provided by DB team

    ```
    psql -h <ip-alias> -p <port> -U admin
    ALTER ROLE admin WITH PASSWORD 'new_password';
    ```

    * To list databases and tables in psql respactively

    ```
    \l
    \dt
    ```

    * Create a new database
    ```
    CREATE DATABASE devmlp
    ```
    * To connect to this database
    ```
    \c devmlp 
    ```

4. Add the required environment variables in `settings.py` and OpenShift for this database
```
'ENGINE': config('DJANGO_DATABASE_ENGINE')
'NAME': config('DJANGO_DATABASE_NAME')
'USER': config('DJANGO_DATABASE_USER')
'PASSWORD': config('DJANGO_DATABASE_PASSWORD')
'HOST': config('DJANGO_DATABASE_HOST')
'PORT': config('DJANGO_DATABASE_PORT')
```
