FROM python:3.9
WORKDIR /usr/home/backend
COPY requirements.txt /usr/home/backend
RUN pip3 install -r requirements.txt
COPY . /usr/home/backend
ENV PYTHONUNBUFFERED=1
RUN python3 manage.py collectstatic --noinput
EXPOSE 8000
ENTRYPOINT ["sh", "startserver.sh" ]