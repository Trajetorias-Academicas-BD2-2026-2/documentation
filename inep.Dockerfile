FROM python:3.12-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends postgresql-client \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .
CMD ["bash", "scripts/run-inep-docker-demo.sh"]
