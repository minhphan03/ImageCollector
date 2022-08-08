FROM python:3.7-alpine

ENV VIRTUAL_ENV=/opt/venv 
RUN python3 -m venv $VIRTUAL_ENV 
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN 
# Install depencencies
COPY requirements.txt .
RUN apk update && \
    pip install -r requirements.txt

# Copy others
RUN mkdir /project
RUN cd HOST_REPO

WORKDIR /HOST_REPO

COPY . .

CMD ["python3", "-u", "src/main.py"]

