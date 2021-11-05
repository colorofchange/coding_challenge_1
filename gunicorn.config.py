# Comment out for local development
# certfile = '/code/stout.colorofchange.org/fullchain1.pem'
# keyfile = '/code/stout.colorofchange.org/privkey1.pem'
######################################################

bind = ['0.0.0.0:443','0.0.0.0:80' ]
worker_tmp_dir = '/dev/shm'
workers=2
threads=4 
worker_class= 'gthread'
loglevel = 'debug'