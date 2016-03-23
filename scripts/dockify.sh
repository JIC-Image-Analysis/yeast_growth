#!/bin/bash

DATADIR=`pwd`/data
CODEDIR=`pwd`/scripts
OUTPUTDIR=`pwd`/output
CONTAINER=jicscicomp/jicbioimage

docker run -v $DATADIR:/data -v $CODEDIR:/code -v $OUTPUTDIR:/output -it --rm $CONTAINER
