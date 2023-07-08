FROM python:latest

COPY ./app.py ./requirements.txt /opt/app/

RUN pip install -r /opt/app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
