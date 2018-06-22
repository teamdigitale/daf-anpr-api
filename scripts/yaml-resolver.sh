#!/bin/bash
: ${1?Missing openapi spec file}

FROM=$(readlink -f $1); shift
FROM_DIR=$(dirname $FROM)
FROM_INNER="/tmp/$(basename $FROM)"
docker run --rm \
        --user=$UID:$GID \
        -v $FROM_DIR:/tmp:z \
        -v $PWD:/code \
        --entrypoint /usr/bin/env \
        ioggstream/api-spec-converter \
        python /code/scripts/yaml-resolver.py  "$FROM_INNER" $@

