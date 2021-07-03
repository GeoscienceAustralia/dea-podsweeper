FROM python:3.9.6-alpine

RUN pip install kubernetes click

ADD . .
