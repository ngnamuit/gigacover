# INTRO
sample-python-api is a RestAPIs simple.
It provides a UI manage routing and JWT for authentication requests.
[![Screenshot](https://i.imgur.com/SaCq8NQ.png)](sample-python-api)

# INSTALLING
### Local environment
You need to install postgreSQL and create a database before or you can install these easily 
by following this [site](https://www.linode.com/docs/databases/postgresql/how-to-install-postgresql-on-ubuntu-16-04/).

Then you must to modify the config.ini file.
```
[DEFAULT]
DatabaseHost = your_host
DatabaseName = your_database_name
DatabaseUserName = your_databse_user_name
DatabasePassword = your_databse_password
JWT_SECRET_KEY = your_secret_key
```
Install dependencies.
```bash
    pip install -r requirements.txt
```
Run app 
```bash
    FLASK_APP=app.py flask run
```
Open http://127.0.0.1:5000 in a browser.


### Production enviroment
You need to install postgreSQL and create a database.
Then you must to modify config.ini file.
```
[DEFAULT]
DatabaseHost = your_host
DatabaseName = your_database_name
DatabaseUserName = your_databse_user_name
DatabasePassword = your_databse_password
JWT_SECRET_KEY = your_secret_key
```
I recommend you using the following technologies to deploy this app:
```
sample-python-api: Server backend
Nginx: Reverse proxy
Gunicorn: Deploy flask app
Supervisor: Monitor and control gunicorn process
```

And you can install by following these command:
- Install nginx and supervisor
```
sudo apt-get install nginx supervisor
```
- Create a supervisor file in /etc/supervisor/conf.d/sample_python_api.conf and configure it according to your requirements.
```
[program:sample_python_api]
directory=/home/ubuntu/sample_python_api
command=/home/ubuntu/.env/bin/gunicorn gunicorn --workers=5 test:app app:flask_app -b 127.0.0.1:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/sample_python_api/sample_python_api.err.log
stdout_logfile=/var/log/sample_python_api/sample_python_api.out.log
```
- To enable the configuration:
```
$ sudo supervisorctl reread
$ sudo service supervisor restart
```
- To check the status of all monitored app, use the following command:
```
$ sudo supervisorctl status
```
- Setup nginx
```
$ sudo vim /etc/nginx/conf.d/virtual.conf
```
- Paste the following configuration:
```
server {
    listen       80;
    server_name  your_public_dnsname_here;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```
- Restart the nginx web server.
```
$ sudo nginx -t
$ sudo service nginx restart
```
Open your_public_dnsname in a browser.
# USAGE
- First, you need to login to get JWT token
[![Screenshot](https://i.imgur.com/fiYQnYs.png)](sample-python-api)

- Add this JWT to request header to use apis.
[![Screenshot](https://i.imgur.com/UExMSDZ.png)](sample-python-api)

- Add new customer api
[![Screenshot](https://i.imgur.com/XyBBx5O.png)](sample-python-api)

- Get customer api
[![Screenshot](https://i.imgur.com/WB6plVl.png)](sample-python-api)

- Delete customer api
[![Screenshot](https://i.imgur.com/2e90XcS.png)](sample-python-api)

- Update a customer api
[![Screenshot](https://i.imgur.com/uFDkxPH.png)](sample-python-api)

- When your JWT  has expired or incorrect: 
[![Screenshot](https://i.imgur.com/Dz0F16G.png)](sample-python-api)