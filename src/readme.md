## Building Instructions

### Requirements
* [docker](https://www.docker.com/)
* docker compose
* python 3.7
* 5 GB or so of room for containers

### Build steps
* cd into src
* run 'docker-compose build'
* build can take up to 10 minutes
* run 'docker-compose up'
* Website should be running at "http://127.0.0.1:8000/hotornot/"
* Basic Overview of backend api can be found at "http://127.0.0.1:5000"

> :warning: **Note**: Once entity-ident container is up takes 5-10 mins to download stanza models

> :warning: **Note**: System only has data collected between Nov 11th 2020 to Dec 15th 2020

### Test Steps

#### Entity Identifcation tests

* go to src/backend/apps/entity_identification/tests
* edit test.py with note if desired
* run test.py
* results stored in data/eval_sentiment/results

#### Sentiment analysis tests

* go to src/backend/apps/sentiment_analysis/tests
* edit test.py with note if desired
* run test.py
* results stored in data/eval_sentiment/results

#### Prediction tests

* go to src/backend/apps/prediction/tests
* edit test_prediciton.py
* change bottom of \__main__ to required test
* run test_prediction.py
* results stored in data/eval_prediction/results

#### Backend API unit tests

* go to src/backend/backend_api/tests
* run 'api_tests.py' and 'points_tests' to test bakcend api calls

## Src Rundown 

### Directory structure

    src
    ├── backend 
    │   ├── apps                        
    │   │   ├── entity_identification   # Context analysis component
    │   │   ├── news-crawler            # News crawler component
    │   │   ├── prediction              # Stock prediciton component
    │   │   ├── sentence_extraction     # Sentence extraction component
    │   │   └── sentiment_analysis      # Sentiment analysis component
    │   ├── backend_api                 # Backend api 
    │   ├── control                     # Control component 
    ├── database   
    │   ├── main                        # Main db sql
    │   ├── timeseries                  # Timesries db sql
    │   ├── scripts                     # Data input scripts
    └── frontend                        # Django webapp


### Description 
Project split into three parts: backend, database, frontend
#### /backend

* /apps contains components for collecting and processing articles. Each component has its own docker file and API
* backend_api contains flask API which communicates to the main and timeseries database
* control component for communicating with '/apps' components and backend api 

#### /database
contains SQL for main and timeseries databases along with some scripts used to input data into them.

#### /frontend
Contains the django webapp  

