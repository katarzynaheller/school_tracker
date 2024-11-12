# SCHOOL TRACKER
Backend part (API) for school app designed to manage children/students activities, events and  progress in educational institution. App is build with several components: for planning events, reporting meal and behaviour status and for chat with teacher. 


## Purpose:
Project's purpose is to improve communication between parent and teacher as well as provide help for parents in tracking child's achievements and preparing for planned events. Funtionalities can be adjusted to the type of insitution. For example: meals can be tracked for nursery but grades/points for school.

## How to run app locally (Docker):

### Build image locally:
docker compose -f develop.yaml build

### Run docker containers (Django and PostgreSQL):
`docker compose -f develop.yaml up`

### Remove containers:
`docker compose -f develop.yaml down`

### Create superuser
`docker compose exec school_tracker_container bash`
`python manage.py create superuser`

### Login to app
`0.0.0.0:8000/app/v1/admin/`

### Run tests
`docker compose exec school_tracker_container bash`
`python manage.py tests`

// Note: when file has custom name different that "docker-compose.yaml" docker deamon expects `-f` flag with correct yaml's file name in terms to find it. File in this repository is named this way to provide more flexability when need for different environment will arise. 

# Licence:
CC BY-NC-ND 4.0