FROM dynverse/dynwrap:py3.6

RUN pip install Cython

run pip install uncurl-seq

LABEL version 0.0.1

ADD . /code

ENTRYPOINT python /code/run.py
