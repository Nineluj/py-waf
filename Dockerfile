FROM python:3

# RUN pip3 install protobuf pynacl passlib argon2_cffi pyyaml

WORKDIR /app

ADD . /app/

ENTRYPOINT ["/bin/bash"]