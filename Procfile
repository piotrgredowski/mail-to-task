web: ./lib/crypting.py decrypt && python -m mail_to_task.__init__
worker: rqscheduler --url ${REDIS_URL} --db 0 -i 5 & python worker.py
