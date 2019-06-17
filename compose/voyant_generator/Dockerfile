FROM python:3

COPY compose/voyant_generator/bin /run

COPY compose/context/ /input/

WORKDIR /run

CMD /bin/sh voyant_gen_script.sh
