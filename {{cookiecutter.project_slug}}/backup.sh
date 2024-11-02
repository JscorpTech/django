file=/tmp/db-$(/usr/bin/date +\%Y-%m-%d-%H:%M:%S).sql
container=9560b8175cfd
/usr/bin/docker container exec $container pg_dump -U postgres django > $file
scp $file /home/backup/db/document/
rm $file