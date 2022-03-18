
FROM python:3.8.10
RUN pip3 install requests
WORKDIR /serv3/
ADD . /serv3
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5003


COPY . .

CMD ["python3", "service3.py"]


