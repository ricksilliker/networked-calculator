FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/calculator ./calculator

# Host must not be localhost since it's running in an isolated environment,
# and I need it to connect to things outside the container.
ENV TEST_HOST "0.0.0.0"
ENV TEST_PORT "5454"

EXPOSE 5454

CMD ["python", "-m", "calculator.server"]
