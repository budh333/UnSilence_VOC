FROM alpine:latest

RUN apk update && apk add --no-cache curl python2 tar mailcap

# Fetch  brat
COPY brat-v1.3_Crunchy_Frog.tar.gz /brat-v1.3_Crunchy_Frog.tar.gz

RUN tar -xzvf brat-v1.3_Crunchy_Frog.tar.gz && rm brat-v1.3_Crunchy_Frog.tar.gz

WORKDIR /brat-v1.3_Crunchy_Frog/

COPY config.py ./

RUN mkdir /data /work && ln -s /data . && ln -s /work .

EXPOSE 8080

CMD ["python2", "/brat-v1.3_Crunchy_Frog/standalone.py", "8080"]
