FROM python:3.6-slim

LABEL MAINTAINER="Matheus Jericó <matheusjerico1994@hotmail.com>"

RUN mkdir /code

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt &&\
    python -m nltk.downloader punkt &&\
	python -m nltk.downloader stopwords

WORKDIR /code

COPY . /code

RUN chmod +x -R /code/

EXPOSE 8080

# CMD ["./run.sh"]