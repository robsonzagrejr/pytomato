FROM python:latest

WORKDIR /app
COPY . .
RUN pip install poetry
RUN make install

CMD ["make", "app"]