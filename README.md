python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

alembic upgrade head

python -m app.manage createsuperuser --email=admin1@example.com --password=vjyntu
python -m app.manage runserver