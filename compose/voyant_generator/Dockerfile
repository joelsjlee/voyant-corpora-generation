FROM python:3

COPY /bin /bin

COPY /python /python

COPY /newspapers /input/newspapers

COPY keywords.txt /input

ENV CONTAINER_VOL container_volume

ENV VOYANT_GEN_INPUT voyant_generator_input

ENV VOYANT_GEN_OUTPUT voyant_generator_output

VOLUME [/${CONTAINER_VOYANT_GEN_VOL}]

WORKDIR /python

CMD voyant_gen_script.sh
