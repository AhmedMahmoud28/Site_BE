# Site_BE

Creating API Endpoints

# Setup

Install the requirements file on your machine

pip install .\requirments.txt

Create .env file on this repo and provide secret key for the project and database configuration

# Generate secret key

- py manage.py shell # enter the interactive shell
- from django.core.management.utils import get_random_secret_key # importing the function from utils
- print(get_random_secret_key()) # generating and printing the SECRET_KEY
- copy the key and place it in .env file

# Usage

Use the site for adding items in subscribe list
Go to subscription and "post" to add your subscription

# note

- Packageapp has a test in tests.py
- Swagger is provided
