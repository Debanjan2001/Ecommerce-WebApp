# Ecommerce-WebApp

This is a simple Ecommerce website implemented using Django 3.1 and Python 3.8. It is hosted on Heroku. You can check the product here: [https//:ecommerce-debanjan.herokuapp.com/](https//:ecommerce-debanjan.herokuapp.com/)


### Screenshots of the app
![ Ecommerce-WebApp Screenshots](Ecommerce.gif)

### Instructions to run it locally

Clone This Project (Make Sure You Have Git Installed)
```
git clone https://github.com/Debanjan2001/Ecommerce-WebApp.git
```

Change your directory to the cloned repo

```
cd <<Your Download Location Here>>/Ecommerce-Webapp
```

Install Dependencies 
```
pip install -r requirements.txt
```
Feel free to create your own virtual environment to manage all the requirements in one place.( Check the `DigitalOcean` link below: it contains setup instructions for virtual environment as well. I would highly encourage you to create a virtual environment so that your main workspace does not get clustered with unneccessary packages.)

Now you need to configure database (Postgres). Follow the steps below. Alternatively, you can follow the steps from [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04)
Steps: Enter these commands one by one in your terminal:
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
sudo -u postgres psql
```

Now you will enter Postgres Session. Now run the following commands:
```
CREATE DATABASE ecommerce_database;
CREATE USER admin WITH PASSWORD 'ecommerce';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC+05:30';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_database TO admin;
```

Now your database is configured to manage this app. Exit the session using the command:
```
\q
```

Run migrations for django. (Make Sure you are in directory same as manage.py)
```
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations
```

Create SuperUser to get admin login for managing site.
```
python manage.py createsuperuser
```

Run this command so that Django can serve static files from one location.
```
python manage.py collectstatic
```

Now You might have noticed, I have an automated mail service. I created a personal email address and added it to django settings using the following steps:

1. Go to `ecommerce` folder in project directory and open `private_settings.py` folder

2. If you have an alternate email address, please add your email address and password in place of `YOUR_EMAIL_ADDRESS` and `YOUR_EMAIL_PASSWORD`. Please do not share these with anyone. I would recommend doing this with an alternate email for a reason which is explained after a few steps.

3. Run the following command in terminal to get a secret key for django: 
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 
```

4. You will receive a secret key in the terminal when you run this command. Copy paste this key in place of `YOUR_SECRET_KEY` inside `private_settings.py`.

5. After all these steps, now I would tell you why I asked you to use an alternate email. For django to use the smtp mail server and your email address for mailing, you need to do the following:

6. Login with your email account.

7. Go to this site: [https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps) and turn on `ALLOW LESS SECURE APPS`.

8. `Some apps and devices use less secure sign-in technology, which makes your account vulnerable.` (According to Google). So Google recommends turning this off. But for this project I am using the service for simplicity.

After all these steps , you can run the app. 
```
python manage.py runserver
```

### Reason of Superuser profile page error on starting the application.
On starting app, superuser will not have any profile because we created superuser from terminal. So you need to go to django admin panel to create a profile page for him.
