FROM debian:bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 python3-pip gcc curl python3-dev autoconf python3-dev\
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root
COPY . .
EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", "rgb_assets.api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
