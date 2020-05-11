FROM registry.access.redhat.com/ubi8/ubi
RUN /usr/bin/yum -y install elfutils gdb bzip2 unzip
COPY tmp/getdebuginfo /
COPY tmp/pcore.main /
COPY run_doctest.sh /
RUN chmod +x /getdebuginfo
RUN chmod +x /pcore.main
RUN chmod +x /run_doctest.sh
