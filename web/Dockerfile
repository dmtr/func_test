FROM python:3.5.1
RUN mkdir -p /app/func_test
ADD func_test /app/func_test/
RUN pip install --upgrade pip
WORKDIR /app
RUN pip3 install -r func_test/requirements.txt
RUN useradd -M web
RUN chown web:web /app
USER web
