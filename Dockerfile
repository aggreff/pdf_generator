FROM python:3.6
ADD . /code
WORKDIR /code

ENV MAIN_PACKAGES  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
RUN apt-get update -qq \
  && apt-get install --no-install-recommends -yq $MAIN_PACKAGES

RUN pip install -r requirements.txt
