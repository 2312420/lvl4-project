# User manual 

## Running Project

### Running entire system
* cd in to src folder
* run 'docker-compose build'
* build can take up to 10 minutes
* run 'docker-compose up' to run system
* run 'docker-compose down' to stop system

### Containers
| Component Name       | Container ID         | port
|----------------------|----------------------|----------------------|
| Main database        | dbmain               | 5432
| Time-series database | dbtime               | 5433
| Frontend webapp      | frontend             | 8000
| Backend API          | backend-api          | 5000
| Context analysis     | entity-ident         | 5001
| Sentence extraction  | sentenece-extraction | 5002
| Sentiment Analysis   | sentiment-analysis   | 5003
| Stock Prediction     | prediction           | 5004
| Control              | control              | -
| News Crawler         | news-crawler         | -

Individual components can be run by using the command 
>docker-compose run \<container ID>

For example running 'docker-compose run frontend' will start the webapp and the other containers it depends on.

## Using
Some components need time to download required data once their containers are active. The control component will wait for these components to become fully operational before processing articles and sentences.

When the system if fully operational the webapp should be running on 
>"http://127.0.0.1:8000/hotornot/"

This is the homepage and contains a list of all the companies in the system (That have had articles collected on them). Clicking on company box will take you to the indvidual company page. The backend API documenation can also be found at 

> "http://127.0.0.1:5000"


