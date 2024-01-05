# base image for running tests
FROM python:3.11

# set the workdir to /app
WORKDIR /app

# copy pyproject and poetry lockfile for stepped installation
COPY pyproject.toml poetry.lock ./

# install poetry and poetry dynamic versioning
# hadolint ignore=DL3013
RUN pip install --no-cache-dir poetry

# copy the rest of the repository
COPY . .

# install env from poetry
RUN poetry install -v --no-interaction

# set an alias for running python through the poetry env
# hadolint ignore=DL3059
RUN echo 'alias python="poetry run python"' >> ~/.bashrc
