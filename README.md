#LA ZONE DEVELOPER TEST

simple quiz game built in python and django❤️❤️

used basic external movie api to fetch game data

Core Backend Service

# Features

- Start Game
- Play Game
- Get Score



## Installation

To run this service, you need to have the following dependencies installed:

- asgiref==3.7.2
- certifi==2023.11.17
- charset-normalizer==3.3.2
- Django==5.0.1
- djangorestframework==3.14.0
- idna==3.6
- python-decouple==3.8
- python-dotenv==1.0.0
- pytz==2023.3.post1
- requests==2.31.0


* Navigate to the project directory
* Install all dependencies using `pip install R> requirements.txt`
* Rename .env.example to .env in the root directory
* Migrate the database using `python manage.py make migrations & python manage.py migrate`
* Open http://localhost:8000/api/v1/heath on your browser to ensure the service is running
* Enjoy

## Run tests

* Run test with this command `python manage.py test core_backend.tests`
<img width="593" alt="Screenshot 2024-01-16 at 10 31 48 AM" src="https://github.com/jephthah-snr/la_zone-developer-test/assets/60290652/f08a21fd-ae4c-4e63-bcd1-112f1e1fdd31">
*test case all passed

## Documentation
postman api deocumentation available at [here](https://documenter.getpostman.com/view/13371791/2s9YsQ8pqn)

## Health Checks

This service supports readiness and liveliness probes via http://localhost:8000/api/v1/game/health/readyz endpoint

# Core-Backend
