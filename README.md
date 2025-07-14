# tweetProject
Django Project


python3 -m venv .venv
source venv/bin/activate
pip install django
pip install --upgrade pip
pip freeze > requirements.txt
pip install -r requirements.txt

django-admin startproject tweet_root

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py startapp tweet

python manage.py makemigrations tweet