#!/bin/bash
# Generate a python-flask app from the swagger.yaml
set -eo pipefail

usage(){
	echo "$0 path_to_swagger.yaml path_to_project_dir"

	echo "
	This script requires gnu coreutils. If you are on mac please
	- check readlink behavior (eg. use greadlink)
        - remove trailing \":z\" from docker run as it's selinux specific.
	"
}

normpath(){
	# Normalize path.
	readlink -f "$1"
}

: {1?Missing infile}
: {2?Missing outdir}

IMG=swaggerapi/swagger-codegen-cli

docker run --rm \
	--user=$UID:$GID \
	-v $(normpath "$1"):/swagger.yaml:z \
	-v $(normpath "$2"):/outdir:z $IMG \
	generate -l python-flask -o /outdir -i /swagger.yaml


