FROM python:latest

WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["poetry", "run python app.py"]