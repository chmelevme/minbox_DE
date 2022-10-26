FROM python:3.9

WORKDIR /usr/src/app

COPY ./Docker/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src



CMD ["python3"]