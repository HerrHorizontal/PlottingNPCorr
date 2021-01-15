#!/bin/bash

# -- get the location of this script (thisdir)
_thisdir=${BASH_ARGV[0]}
_thisdir=$(cd "$(dirname "${_thisdir}")"; pwd)
_thisdir=$(python -c "import os,sys; print(os.path.realpath(os.path.expanduser(sys.argv[1])))" ${_thisdir})

# -- set up environment variables pointing to analysis modules
export LUMBERJACK_CONFIGPATH="$LUMBERJACK_CONFIGPATH:${_thisdir}/cfg/python/Lumberjack"
export PALISADE_CONFIGPATH="$PALISADE_CONFIGPATH:${_thisdir}/cfg/python/Palisade"
