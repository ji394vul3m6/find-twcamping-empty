LATEST_TAG=`git describe --tags --abbrev=0`
COMMIT=`git rev-parse --short HEAD`

set -e
CMD="docker build -t find-twcamping:$LATEST_TAG-$COMMIT -f Dockerfile ."
eval $CMD
docker tag find-twcamping:$LATEST_TAG-$COMMIT find-twcamping:$LATEST_TAG
docker tag find-twcamping:$LATEST_TAG-$COMMIT find-twcamping:latest