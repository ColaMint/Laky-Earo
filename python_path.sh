#!/bin/bash

pythonpath=$(cd "$(dirname "$0")"; pwd)
export PYTHONPATH=$pythonpath:$PYTHONPATH
echo $PYTHONPATH
