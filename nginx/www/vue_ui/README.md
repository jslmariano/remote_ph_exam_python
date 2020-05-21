# ORDER DETAILS - VUEJS - PYTHON - MONGO - POSTGRES

## Overview

A modular restful api made from flask restplus, and already docker containerized. This is just a demo of a simple application with working mongodb and postgresql.

Check it out here: https://app.jslmariano.com/

NOTE: This link is down for now due to charges, if you want a demo please email me at **jslmariano at gmail dot com** :)

Requirements:

- Docker CE ( Could be hosted on windows, vmware or virtualbox | Debian 9 )
- Flask (latest)
- Python 3.7 ( Docker Image  python:3.7-slim )
- PostgreSQL ( Docker image postgres:latest )
- MongoDB ( Docker image mongo:4.0.8 )
- Nginx ( Docker image nginx:alpine )

## Notes

- Please see .env file for database configuration
- No need to import dummy database it will be handled by `docker-compose`
- If you bring up your docker in background using `docker-compose up -d`  please use `docker-compose logs -f <container-name>` to peek on console


## Local Dev Instructions

1. I recommend using Linux OS, if on windows install [virtualBox](https://www.wikihow.com/Install-VirtualBox).
2. Install docker for debian from this tutorial https://docs.docker.com/install/ and https://docs.docker.com/compose/install/
3. Open up terminal inside your VirtualBox and `ping google.com`
2. Clone files on your workspace - 
```
cd ~
git clone https://github.com/jslmariano/remote_ph_exam_python.git app
cd app/
```
4. Check your configuration files, change according to your project
    1. `docker_compose/app/.env`
    1. `docker_compose/mongodb/.env`
    1. `docker_compose/postgres/.env`
4. Build images - `docker-compose build` (This may take a while for 1st time, go grab your coffee :) )
    4. **FAIL SOMETIMES DUE TO NETWORK, JUST RUN IT AGAIN**
    5. Make sure you have network `ping google.com`
    6. Directory is not writable? You can use your home directory inside your virtualbox, see step 3
5. Start services - `docker-compose up -d --build`
6. Browse your application on - `http://localhost/order/`
7. Check you containers if all is running `docker ps -a`
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
304ee027285d        jsl-nginx           "nginx -g 'daemon of…"   26 hours ago        Up 26 hours         0.0.0.0:80->80/tcp         jsl-nginx
088d80e9787d        jsl-postgres        "docker-entrypoint.s…"   26 hours ago        Up 26 hours         0.0.0.0:5432->5432/tcp     jsl-postgres
62a0bacd9f34        jsl-app             "gunicorn --reload w…"   26 hours ago        Up About an hour    8080/tcp                   jsl-app
40d111374c77        mongo:4.0.8         "docker-entrypoint.s…"   26 hours ago        Up 26 hours         0.0.0.0:27017->27017/tcp   jsl-mongo

```
7. Checking logs inside container
```
docker-compose logs -f jsl-app
```
7. Database Setup   
   1. Initialize migration `docker exec -it jsl-app python manage.py db init`
   1. Prepare migration `docker exec -it jsl-app python manage.py db migrate`
   1. Apply migration `docker exec -it jsl-app python manage.py db upgrade`
   1. Load CSV files to DB  `docker exec -it jsl-app python manage.py load_csv`
8. (OPTIONAL) Test scripts are available, `docker exec -it jsl-app python manage.py test`
9. More troubleshooting [here](#troubleshooting)


## Restful API DEMO

If lazy to setup POSTMAN just go to `/api/v1` and swagger ui will help you out :)

1. Go to [Postman Docs](https://documenter.getpostman.com/view/6907051/Szmh2wHN?version=latest) and Click "Run in postman"
1. If your postman opens choose "Flask Modular RestPlus | Local" as environment to your top right corner
1. If the 2 above does not work, proceed below to the manual
1. Download and install postman here [Postman Download](https://www.postman.com/downloads/)
1. If you wanted to sign-in you can use your google account but this is optional
1. Repeat 1st instruction
1. On your left side panel you should see the "Flask Modular RestPlus" in Collections tab
1. Finally add environment variables
1. Click the gear icon on top right corner
1. Click "Add" button
1. Type "Flask Modular RestPlus | Local" as the environment name
1. Variables are
```
VARIABLE    | INITIAL VALUE    | CURRENT VALUE    |
host        | localhost        | localhost        |
token_auth  | (leave blank)    | (leave blank)    |
```

### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/ or http://localhost/


### Users ###

Create a user by POSTing to api `/user`, using curl or anything you are comfortable
with body
```
{
    "username":"admin",
    "email":"admmin@example.com",
    "password":"admin"
}
```

### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.

    NOTE: Authorization header is automatically updated in POSTMAN variable `token_auth` if you login using POSTMAN :)


### TROUBLESHOOTING

- If nginx is running then stop it because docker web container will listen to port 80
- If postgresql is running then stop it because docker postgresql container will listen to port 5432
- If using VirtualBox from windows you should mount you files properly for permission correction - `mount -t vboxsf -o rw,uid=1000,gid=1000 <share_name> <mount_path>`
- Local host url - `localhost`
- If using virtualBox then make sure port forwarding through NAT is correctly configured, look [here](https://www.howtogeek.com/122641/how-to-forward-ports-to-a-virtual-machine-and-use-it-as-a-server/) after reading, then make sure ports are forwarded EG: ( 80, 443, 5432, 8050,..  )


### Contributing
If you want to contribute to this flask modular restplus, clone the repository and just start making pull requests.

```
https://github.com/jslmariano/remote_ph_exam_python.git
```
