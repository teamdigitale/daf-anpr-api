#!/bin/bash
set -eo pipefail

die(){
	echo "ERROR: $@"
	exit 1
}
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

: ${1?Please specify a file to convert}
FROM="$(normpath "$1")"; shift
test -f "$FROM" || die "File not found: $FROM"

which docker >&2 || die "You need docker to run this file."

build(){
	# Eventually build docker image.
	docker >&2 build -t api-spec-converter $(dirname $(normpath $0))  || die "Cannot build docker image."
}

docker run --rm \
	--user=$UID:$GID \
	-v $(dirname $FROM):/tmp:z \
	--entrypoint /usr/local/bin/api-spec-converter \
 	ioggstream/api-spec-converter \
	"/tmp/$(basename $FROM)" --syntax="${FROM##*.}" --from=openapi_3 --to=swagger_2 $@


