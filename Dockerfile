FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get -y install ffmpeg libavcodec-extra git && \
    pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install git+https://github.com/openai/whisper.git 

COPY ./app/ .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]