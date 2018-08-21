FROM python:3.6

RUN pip install cython

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install -r requirements/requirements.txt
EXPOSE 5000
CMD ["./appRun.sh", "start"]
