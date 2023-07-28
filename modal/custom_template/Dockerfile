FROM python:3.10

WORKDIR /app

COPY data/* /app/data/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY src/ /app/src
COPY model.py /app/model.py
COPY modal_wrapper.py /app/modal_wrapper.py

CMD ["python", "model.py"]
