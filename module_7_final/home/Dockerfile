FROM python:3.9
WORKDIR /usr/src/app
COPY ./app ./
COPY ./requirements.txt ./
COPY ./app/models/model_opt.pkl ./app/models/
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./server.py" ]