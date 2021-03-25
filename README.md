# consultasapi
[![Python application](https://github.com/alysonbg/consultasapi/actions/workflows/djang_project.yml/badge.svg)](https://github.com/alysonbg/consultasapi/actions/workflows/djang_project.yml)
Projeto de api para marcar gerenciar a marcação de consultas médicas
Instruções de instalação(Python 3.9) com sqlite:

git clone https://github.com/alysonbg/consultasapi.git
cd cd conculstasapi
cp contrib/env-sample .env
python -m pip install pipenv
pipenv sync
pipenv shell
python manage.py migrate
python manage.py collectstatic
python manage.py runserver