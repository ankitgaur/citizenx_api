

source activate py37env
export LD_LIBRARY_PATH=/home/ubuntu/anaconda2/lib
#nohup uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi > uwsgi.out &
nohup uwsgi --http :8000 --module citizenx.wsgi > uwsgi.out &
