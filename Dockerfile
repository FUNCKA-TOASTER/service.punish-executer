# Use Python 3.10 base image
FROM python:3.10.0

# Metadata
LABEL author="Oidaho" email="oidahomain@gmail.com"

# Set build arguments
ARG vk_group_token
ARG vk_group_id
ARG sql_host
ARG sql_port
ARG sql_user
ARG sql_pswd
ARG alchemy_dialect
ARG alchemy_driver
ARG alchemy_database
ARG rabbitmq_host
ARG rabbitmq_port
ARG rabbitmq_vhost
ARG rabbitmq_user
ARG rabbitmq_pswd

# Set environment variables
ENV vk_group_token $vk_group_token
ENV vk_group_id $vk_group_id
ENV sql_host $sql_host
ENV sql_port $sql_port
ENV sql_user $sql_user
ENV sql_pswd $sql_pswd
ENV alchemy_dialect $alchemy_dialect
ENV alchemy_driver $alchemy_driver
ENV alchemy_database $alchemy_database
ENV rabbitmq_host $rabbitmq_host
ENV rabbitmq_port $rabbitmq_port
ENV rabbitmq_vhost $rabbitmq_vhost
ENV rabbitmq_user $rabbitmq_user
ENV rabbitmq_pswd $rabbitmq_pswd

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