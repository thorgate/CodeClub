FROM python:3.6-slim
COPY ./tester.py /src/tester.py
COPY ./reporter.py /src/reporter.py
COPY ./solution.py* /src/
COPY ./requirements.txt /src/requirements.txt
WORKDIR /src
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "reporter.py"]
