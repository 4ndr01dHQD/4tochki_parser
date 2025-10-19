FROM python:3.12.5-bullseye

ENV PATH="${PATH}:/root/.local/bin" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN pip install --upgrade pip && pip install poetry

RUN poetry install --only main --no-root

COPY . .

WORKDIR /src/

ENTRYPOINT ["python3", "main.py"]

