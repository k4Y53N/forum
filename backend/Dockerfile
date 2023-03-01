FROM python:3.9
COPY . /usr/home/backend
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/home/backend
RUN pip3 install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["sh", "startserver.sh" ]