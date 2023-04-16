FROM python:3.11
WORKDIR /root
COPY requirements.txt .
COPY freqBigrammes.txt .
COPY main.py .
RUN pip install -r requirements.txt
CMD python main.py cli