# docker run -it -v ${HOME}:/root muccg/jira
#
FROM python:2.7

ENV PYTHONUNBUFFERED 1

COPY ./app /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
VOLUME /root/

CMD ["python", "client.py"]
