FROM python:3-alpine

RUN apk add --no-cache pcre nodejs npm

COPY client /app/client
COPY server /app/server

RUN cd /app/server && pip3 install poetry
RUN cd /app/server && poetry install
RUN cd /app && npm install --prefix client && npm run build --prefix client

RUN apk del nodejs npm && rm -rf /var/cache/apk/*

WORKDIR /app/server
EXPOSE 5000

CMD ["poetry","run","gunicorn","-w","4","-b","0.0.0.0:5000","app:app"]
