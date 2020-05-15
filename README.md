# FLASK MODULAR RESTFUL With Docker Compose

## Overview

A modular restful api made from flask restplus, and already docker containerized. This is just a working demo between yelp and google vision api

Searches somehow locked to MANILA coordinates but may return other addresses depending on YELP API, Use the search box to populate the business names. Then choose from business names on the left side panel to show the reviews with the emotion tags related to **"joyLikelihood"** and **"sorrowLikelihood"** per review

Check it out here: https://app.jslmariano.com/

Requirements:

- Docker CE ( Could be hosted on windows, vmware or virtualbox | Debian 9 )
- Python 3.7
- Flask (latest)

## Notes

- Please see .env file for database configuration
- No need to import dummy database it wll be handled by `docker-compose`
- If you bring up your docker in background please use `docker-compose logs` to peek on console


## Local Dev Instructions

1. Install docker from this tutorial https://docs.docker.com/install/ and https://docs.docker.com/compose/install/
1. Extract the files on your workspace - `/<path_to_workspace>/yelp_twist`
1. Go to your project directory - `/<path_to_workspace>/yelp_twist`
1. Build images - `docker-compose build` (This may take a while for 1st time, go grab your coffee :) )
1. Start services - `docker-compose up`
1. Browse your applciation on - `localhost`
1. (OPTIONAL) Run migration for new tables ` docker exec -it jsl-app /usr/local/bin/python manage.py db migrate`
1. (OPTIONAL) Test scripts are available, `docker exec -it jsl-app /usr/local/bin/python manage.py test`

## Google Cloud Vision API
1. You need to understand the api here https://cloud.google.com/vision/docs
2. There is a lot of working example there using multiple programming languages
3. If you on local you need a Google Service Account json KEY file
4. And set it up like this https://serverfault.com/questions/848580/how-to-use-google-application-credentials-with-gcloud-on-a-server 

## YELP API DEMO

1. For the yelp endpoint api to work on your local you need to create your **API KEY** here : https://www.yelp.com/developers/v3/manage_app
2. Save the file to `web/credential_keys/yelp_api_key.json` with proper json format of 
```
{
    "app_name": "<App Name>",
    "contact_email": "<Email used in yelp>",
    "client_id": "<Client ID>",
    "api_key": "<API Key>"
}
```
3. Edit your docker environment `docker_compose/app/.env` add `YELP_CREDENTIALS=credential_keys/yelp_api_key.json`
4. Go back to your client window and check docker config using `docker-compose config` 
5. check if your `YELP_CREDENTIALS` in there

## Restful API DEMO

If lazy to setup POSTMAN just go to `/api/v1` and swagger ui will help you out :)

1. Go to https://documenter.getpostman.com/view/6907051/Szmh2wHN?version=latest and Click "Run in postman"
1. If your postman opens choose "Flask Modular RestPlus | Local" as environment to your top right corner
1. If the 2 above does not work, proceed below to the manual
1. Download and install postman here https://www.postman.com/downloads/
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


### Contributing
If you want to contribute to this flask modular restplus, clone the repository and just start making pull requests.

```
https://github.com/jslmariano/yelp_twist.git
```
