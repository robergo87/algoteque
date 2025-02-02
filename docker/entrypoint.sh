#!/usr/bin/env bash
set -e
cmd="$@"

pip install psycopg2

function db_ready() {
    python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("dbname='$POSTGRES_DB' port='$POSTGRES_PORT' user='$POSTGRES_USER' host='$POSTGRES_HOST' password='$POSTGRES_PASSWORD'")
    print(conn)
except Exception as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

db_attempts=0
until db_ready; do
    >&2 echo "Database $POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB is unavailable - sleeping"
    sleep 1
    if [ "$db_attempts" -gt 30 ]
    then
        exit 1
    else
        db_attempts=$(($db_attempts+1))
    fi
done
>&2 echo "Database is up - continuing..."
echo "$cmd"
exec $cmd