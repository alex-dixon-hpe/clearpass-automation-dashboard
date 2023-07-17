FROM ubuntu
WORKDIR /app

RUN apt update
RUN apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
