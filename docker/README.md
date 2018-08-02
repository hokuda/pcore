# How to automate steps to provide debuginfo for RHEL7 core


In order to analyze RHEL7 core on Fedora 2x resolving symbols, you need to:

1. copy a pcore archive to RHEL7
1. un-tar a pcore archivre
1. run getdebuginfo
1. re-tar a pcore archive including debuginfo
1. copy back a pcore archive with debuginfo to Fedora 2x

This describes how to automate these steps using Docker container.

## Prepare Docker on Fedora and Docker image of RHEL

1. install docker on Fedora 2x

        $ sudo dnf install docker
        $ sudo mkdir /home/docker # choose a directory for docker as you like
        $ sudo chmod 701 /home/docker
        $ sudo vim /etc/sysconfig/docker
        OPTIONS='--selinux-enabled --log-driver=journald -g /home/docker'
        $ sudo systemctl enable docker
        $ sudo systemctl start docker

1. configure subscription management on Fedora 2x

        $ sudo dnf install dnf-plugin-subscription-manager.x86_64
        $ sudo dnf install docker-latest-rhsubscription.x86_64
        $ sudo subscription-manager register
        $ sudo subscription-manager attach --pool=$POOL_ID

      The pool id is shown by:

        $ sudo subscription-manager list --available

1. enable docker to run as non-root user on Fedora 2x

        $ sudo groupadd docker
        $ sudo usermod -a -G docker hokuda
        $ shutdown -r now

1. create docker image on Fedora 2x

        $ git clone https://github.com/hokuda/pcore.git
        $ cd pcore/docker/rhel7
        $ docker build -t rhel7/pcore .

   Once you created the rhel7/pcore image, you can reuse it for every pcore archives.

## Run run_getdebuginfo_rhel7.sh

   The run_getdebuginfo_rhel7.sh script generates a pcore archive with debuginfo from a pcore archive without debuginfo using a temporal Docker contaier. You will find the pcore-${timestamp}-debuginfo.tar.bz2 file in the current directory (Ensure you have write permission on the current directory).

        $ ./run_getdebuginfo_rhel7.sh /path/to/pcore-${timestamp}.tar.bz2

## Enjoy

        $ tar xvf pcore-${timestamp}-debuginfo.tar.bz2
        $ cd pcore-${timestamp}-debuginfo
        $ ./opencore.sh
        