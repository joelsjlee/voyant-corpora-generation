FROM python:3

COPY compose/voyant_generator/bin /bin

COPY compose/context/ /input/

WORKDIR /bin

CMD source voyant_gen_script.sh
