FROM postgres:14

# Time Zone
ENV TZ Asia/Tokyo

# /docker-entrypoint-initdb.d配下にある*.sqlファイルは起動後実行される
COPY init.sql /docker-entrypoint-initdb.d/init.sql