FROM python:latest

WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN chmod +X run.sh

CMD ["bash","run.sh"]