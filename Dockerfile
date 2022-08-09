FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv 
RUN python3 -m venv $VIRTUAL_ENV 
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install depencencies
COPY requirements.txt .
RUN apt-get update && \
    pip install -r requirements.txt

# Copy others
RUN mkdir project && cd project

WORKDIR /project

COPY . .

CMD ["python3", "-u", "src/main.py"]

