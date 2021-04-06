## Building project (More detail in src/Readme)
Project requires [docker](https://www.docker.com/) and docker compose to build. Images require at least 5GB of free space

* cd into src
* run 'docker-compose build'
* can take up to 10 minutes to build
* build can take up to 10 minutes
* Website should be running at "http://127.0.0.1:8000/hotornot/"
* Basic Overview of backend api can be found at "http://127.0.0.1:5000"

> :warning: **Note**: Once entity-ident container is up takes 5-10 mins to download stanza models

> :warning: **Note**: System only has data collected between Nov 11th 2020 to Dec 15th 2020

## Project Structure Structure

    src
    ├── backend 
    │   ├── apps                # diffrent backend components 
    │   ├── backend_api         # Backend api 
    │   ├── control             # Control component 
    ├── database   
    │   ├── main                # Main db sql
    │   ├── timeseries          # Timesries db sql
    │   ├── scripts             # Data input scripts
    └── frontend                # Django webapp
    