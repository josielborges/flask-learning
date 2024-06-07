FROM postgres:13-alpine
LABEL author="Josiel Eliseu Borges"
ADD ./data_setup.sql /docker-entrypoint-initdb.d/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]