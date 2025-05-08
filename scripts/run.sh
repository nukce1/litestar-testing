#!/bin/sh

alembic -c ./app/db/alembic.ini upgrade head

litestar run --host 0.0.0.0 --port 8000
