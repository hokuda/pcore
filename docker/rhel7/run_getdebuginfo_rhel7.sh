#!/bin/sh

PCORE_ARCHIVE=$1

if [ "x$PCORE_ARCHIVE" == "x" ]; then
    echo "usage $0 pcore-\${timestamp}.tar.bz2"
    exit 1
fi

if [ -f $PCORE_ARCHIVE ]; then
    echo "Found $PCORE_ARCHIVE" 1>&2
else
    echo "Not found $PCORE_ARCHIVE" 1>&2
    exit 1
fi

PCORE_ARCHIVE_BASENAME=`basename $PCORE_ARCHIVE`
PCORE_ARCHIVE_BASENAME_NO_EXTENSION=`echo $PCORE_ARCHIVE_BASENAME | sed s/\.tar\.bz2//`

CONTAINERID=`docker run --rm -d rhel7/pcore /sbin/init`

echo "Copying $PCORE_ARCHIVE to the container $CONTAINERID"
docker cp $PCORE_ARCHIVE $CONTAINERID:/

echo "Unpacking $PCORE_ARCHIVE on the container $CONTAINERID"
docker exec $CONTAINERID tar xvf /$PCORE_ARCHIVE_BASENAME

echo "Running getdebuginfo on the container $CONTAINERID"
# the "-t" option to disable buffering stdout/err
docker exec -t $CONTAINERID /bin/bash -c "cd /$PCORE_ARCHIVE_BASENAME_NO_EXTENSION && ./getdebuginfo"

echo "Moving /$PCORE_ARCHIVE_BASENAME_NO_EXTENSION to /${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo on the container $CONTAINERID"
docker exec $CONTAINERID /usr/bin/mv /$PCORE_ARCHIVE_BASENAME_NO_EXTENSION /${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo

echo "Packing files in /${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo into ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo.tar.bz2 on the container $CONTAINERID"
docker exec $CONTAINERID /usr/bin/tar Jcvf ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo.tar.bz2 ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo

echo "Copying ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo.tar.bz2 on the container $CONTAINERID to this host"
docker cp $CONTAINERID:/${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo.tar.bz2 .

echo "Stopping the container $CONTAINERID"
docker stop $CONTAINERID

echo "debuginfo files are provided. Run:"
echo "tar xvf ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo.tar.bz2; cd ${PCORE_ARCHIVE_BASENAME_NO_EXTENSION}-debuginfo"
echo "./opencore.sh"
