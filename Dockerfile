FROM python:3

RUN mkdir HOST_REPO
RUN cd HOST_REPO

WORKDIR /HOST_REPO

COPY . .

CMD ["python3", "-u", "src/main.py"]