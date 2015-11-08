#!/bin/bash

NAME="cleverup-crm"                                  # Name of the application
DJANGODIR=/opt/cleverup/cleverup             # Django project directory
SOCKFILE=/opt/run/cleverup/socket  # we will communicate using this unix socket
USER=cleverup                                     # the user to run as
GROUP=cleverup                                     # the group to run as
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=frontend.settings.prod
DJANGO_WSGI_MODULE=cleverup                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../env/bin/waitress-serve ${DJANGO_WSGI_MODULE}.wsgi:application \
  --unix_socket $SOCKFILE