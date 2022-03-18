FROM python:3.8.10
RUN pip3 install requests
WORKDIR /serv1/
ADD . /serv1
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001


COPY . .

CMD ["python3", "service1.py"]











