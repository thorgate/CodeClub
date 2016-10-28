# README for CodeClub

 - Python:  3.4
 - DB:      PostgreSQL
 - Docker:  v1.12.3+

## Setting up development

**Create virtualenv**

 `virtualenv --python=python3.4 venv`

 `. ./venv/bin/activate`

or if you use virtualenvwrapper

 `mkvirtualenv codeclub`

 `workon codeclub`

**Install dependencies**

 `pip install -r requirements/local.txt`

**Switch to internal codeclub dir**

 `cd codeclub`

**Create local settings**

Create `settings/local.py` from `settings/local.py.example`

    cp settings/local.py.example settings/local.py

(now you can also open the project in PyCharm without running into issues due to missing virtualenv/settings)

**Apply database migrations**

 `python manage.py migrate`

## RabbitMQ setup (on Ubuntu)

https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-rabbitmq

`echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list`

`curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add -`

`apt-get update`

`sudo apt-get install rabbitmq-server`

## Celery and RabbitMQ setup (on Mac)

**RabbitMQ**

`brew update`

`brew install rabbitmq`

If not already in PATH then `PATH=$PATH:/usr/local/sbin`

`rabbitmq-server` starts the server

**Celery**

`celery -A codeclub worker --loglevel=info`

## Running tests

Use `py.test` for running tests. It's configured to run the entire test-suite of the project by default.

    py.test

You can also use `--reuse-db` or `--nomigrations` flags to speed things up a bit. See also:
https://pytest-django.readthedocs.org/en/latest/index.html

### Coverage

You can also calculate tests coverage with `coverage run -m py.test && coverage html`,
the results will be in `cover/` directory.



This project includes Bower integration.
To install existing dependencies, run `bower install` in the inner project dir (where manage.py is).
To add a dependency, run `bower install <package-name> --save`.
Deploying with Fabric will ensure that all Bower dependencies are also installed in the server.
If you don't have Bower installed, you can get it by running `npm install -g bower`.
