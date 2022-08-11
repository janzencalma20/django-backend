# Cohere Backend

## Requirements
Access to the following github repositories is required to run the code:
- https://github.com/electricalcoolingsolutions/pyleecan
- https://github.com/electricalcoolingsolutions/LPTN-backend (only required for the solverIncl branch)

An environment file (.env) is required to run this repository. 

If you don't have access to any of the resources in this section, please contact [kevin.bersch@electricalcoolingsolutions.com]().

## Installation
The following instructions are valid for Linux (Ubuntu). Syntax might differ on Windows and MacOS.

### Backend
- Clone repository: `git clone https://github.com/electricalcoolingsolutions/Cohere_Backend`
- Initialise submodules: `git submodule update --init --recursive`
- Create python virtual environment: `python -m venv venv`
- Source virtual environment: `source venv/bin/activate`
- Install wheel: `pip install wheel`
- Install modules: `pip install -r requirements.txt`

### Database
- Update apt: `sudo apt update`
- Install postgresql: `sudo apt install postgresql postgresql-contrib`
- Start postgresql: `sudo service postgresql start`
- Log into postgresql: `sudo -u postgres psql`
- Change password: `ALTER USER postgres WITH PASSWORD 'new_password';`
- Create database: `CREATE DATABASE cohere_db;`
- Grant access: `GRANT ALL PRIVILEGES ON DATABASE cohere_db TO postgres;`

### Redis
- Update apt: `sudo apt update`
- Install Redis: `sudo apt install redis-server`
- Add to autostart: Change `supervised no` to `supervised systemd` in /etc/redis/redis.conf (autostart will not work on WSL)
- Restart redis: `sudo systemctl restart redis.service` or `sudo service redis-server start` (WSL)

## Run backend
Make sure postgresql and redis-server are running before running the backend (have to be restarted after reboot).
- Activate venv: `source venv/bin/activate`
- Migrate database: `python manage.py migrate`
- Run backend: `python manage.py runserver`
- Start celery (in separate terminal): `celery -A Dimensions_api worker -l info`

## Update
- Pull updates: `git pull`
- If new migrations have been applied: `python manage.py migrate`

## Coding Guidelines
This project follows the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). Please stick to the following guidelines in particular:
- Function Names: lower_case_with_underscores
- Class Names: CapWords
- Doc strings: Every function should include a doc string explaining its purpose/use
- Leave a blank line between methods and functions
- Leave 2 blank lines between classes




