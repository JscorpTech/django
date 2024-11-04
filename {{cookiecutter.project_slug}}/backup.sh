file=/tmp/db-$(/usr/bin/date +\%Y-%m-%d-%H:%M:%S).sql
container=postgres
/usr/bin/docker container exec $container pg_dump -U postgres django > $file
mc cp $file b2/buket-name
rm $file