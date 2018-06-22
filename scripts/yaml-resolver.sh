#!/bin/bash
: ${1?Missing openapi spec file}

help(){
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



FROM=$(normpath $1); shift
FROM_DIR=$(dirname $FROM)
FROM_INNER="/tmp/$(basename $FROM)"
docker run --rm \
        --user=$UID:$GID \
        -v $FROM_DIR:/tmp:z \
        -v $PWD:/code:z \
        --entrypoint /usr/bin/env \
        ioggstream/api-spec-converter \
        python /code/scripts/yaml-resolver.py  "$FROM_INNER" $@

