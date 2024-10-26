FROM mysql:5.7
ENV  MYSQL_ROOT_PASSWORD=1234
ENV  MYSQL_DATABASE=malhaedgh_db
ADD  ./init/* /docker-entrypoint-initdb.d