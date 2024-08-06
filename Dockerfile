# Use Python 3.10 base image
FROM python:3.10.0

# Metadata
LABEL author="Oidaho" email="oidahomain@gmail.com"

# Set build arguments
ARG TOKEN
ARG GROUPID

# Set environment variables
ENV TOKEN $TOKEN
ENV GROUPID $GROUPID

ARG SQL_HOST
ARG SQL_PORT
ARG SQL_USER
ARG SQL_PSWD

ENV SQL_HOST $SQL_HOST
ENV SQL_PORT $SQL_PORT
ENV SQL_USER $SQL_USER
ENV SQL_PSWD $SQL_PSWD

# Set working directory
WORKDIR /service

# Install poetry
RUN pip install poetry

# Copy only the dependency information
COPY pyproject.toml ./

# Install dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "start.py"]