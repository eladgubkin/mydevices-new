FROM python:3.8-slim

WORKDIR /app
RUN pip3 install pipenv


COPY Pipfile* ./
RUN pipenv install


COPY . ./

CMD pipenv run python3 ./auth_service/app.py
