#!/usr/bin/env bash

celery -A FasterRunner worker -l info -E &

until timeout 10 celery -A FasterRunner inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
celery -A FasterRunner flower --auto_refresh=True --port=5555
