FROM python:3.6
ADD . /code
WORKDIR /code


ENV MAIN_PACKAGES  fontconfig libjpeg62-turbo libssl-dev libxext6 libxrender-dev xfonts-base xfonts-75dpi

RUN apt-get update -qq \
  && apt-get install --no-install-recommends -yq $MAIN_PACKAGES
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb
RUN dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb

RUN pip install -r requirements.txt
