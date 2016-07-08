FROM continuumio/miniconda3
MAINTAINER eterna2 <eterna2@hotmail.com>

RUN apt-get update && \
  apt-get install -y -f \
  build-essential \
  pkg-config \
  python-dev \
  git \
  libffi6 \
  libffi-dev \
  libfreetype6 && \
  rm -rf /var/lib/apt/lists/*
  
RUN conda install \
  jupyter \
  numpy \
  pandas \
  scikit-learn \
  matplotlib
  
RUN pip install falcon gunicorn python-Levenshtein

RUN pip install -U textblob
RUN python -m textblob.download_corpora

RUN pip install -U textacy
RUN python -m spacy.en.download

COPY ./*.py /app/

WORKDIR /app
EXPOSE 80
CMD ["gunicorn","-b","0.0.0.0:80","server:app","-t","6000"]