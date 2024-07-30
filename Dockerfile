FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN mkdir /image_generator

# Set the working directory to /image_generator
WORKDIR /image_generator
# Copy the current directory contents into the container at /image_generator
ADD . /image_generator/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=image_generator.settings

CMD ["celery", "-A", "image_generator", "worker", "--loglevel=info"]