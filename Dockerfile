FROM python:3.12.0
ENV PYTHONDONTWRITEBYTECODE=1
# pythonunbuffred allows any data to be send directly to the terminal without bien buffred
#  also we get the msgs in real time 
ENV PYTHONUNBUFFRED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
