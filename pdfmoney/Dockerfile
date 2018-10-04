# A minimal pdftotext service for the POC. 
FROM ubuntu:18.04

MAINTAINER vgheorgh (vgheorgh@steelcase.com)

RUN apt-get update && apt-get install -y python python-pip poppler-utils

COPY run_pdftotext.sh /tmp/run_pdftotext.sh

ENTRYPOINT ["/bin/bash", "/tmp/run_pdftotext.sh"]