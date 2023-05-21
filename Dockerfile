
FROM python:3.10

WORKDIR /home-project-billing

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY app ./app

CMD ["python", "-m", "app.main"]
