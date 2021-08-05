#!/bin/bash

echo 'Run genesys2 script v1 -cbu'
export LD_LIBRARY_PATH='./lib'
echo 'checking library for genesys2'
ldd ./genesys_2 | grep cmaes
DATE="$(date +%Y-%m-%d_%H-%M)"
#current path
CPATH="$(pwd | xargs basename)"

#generate filename from time and path
log_filename=$DATE'_genesys_log_'$CPATH'.txt'

echo "Starting Genesys 2 with logging to "$log_filename
#execute the optimisation as bg job
./genesys_2 --mode=optim -j=all >$log_filename&

wait

DATE_after="$(date +%Y-%m-%d_%H-%M)"
#current path
pwd="$(pwd)"
echo "Calculation to log: "$log_filename" finished on machine" $HOSTNAME $DATE_after $pwd | mailx -s "GENESYS-CALC-Job finished" christianbussar@gmail.com
