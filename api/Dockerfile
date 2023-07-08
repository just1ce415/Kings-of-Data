FROM python:latest

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY ./api.py ./sift.py ./requirements.txt /opt/app/

RUN pip install -r /opt/app/requirements.txt

ENTRYPOINT ["python", "/opt/app/api.py"]
