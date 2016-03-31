#!/bin/bash

DATADIR=`pwd`/data
CODEDIR=`pwd`/scripts
OUTPUTDIR=`pwd`/output
CONTAINER=yeastprocessor

#docker run -v $DATADIR:/data:ro -v $CODEDIR:/code:ro -v $OUTPUTDIR:/output -it --rm $CONTAINER python /code/ready.py
docker run --link some-redis:redis -v $DATADIR:/data:ro -v $CODEDIR:/code:ro -v $OUTPUTDIR:/output --rm $CONTAINER python /code/populate.py
