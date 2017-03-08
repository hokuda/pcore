tips
---

* how to resiter system to subscription manager

        subscription-manager register --username=$RHSM_USERNAME --password=$RHSM_PASSWORD

* how to attach subscription

        subscription-manager attach --pool=$RHSM_POOLID

* how to add RHSCL(Red Hat Software Collections) repository

  RHEL7:

      subscription-manager repos --enable rhel-server-rhscl-7-rpms
      subscription-manager repos --enable rhel-server-rhscl-7-debug-rpms
      subscription-manager repos --enable rhel-server-rhscl-7-source-rpms

  RHEL6:

      subscription-manager repos --enable rhel-server-rhscl-6-rpms
      subscription-manager repos --enable rhel-server-rhscl-6-debug-rpms
      subscription-manager repos --enable rhel-server-rhscl-6-source-rpms

  See [here](https://access.redhat.com/documentation/en-US/Red_Hat_Software_Collections/2/html/2.2_Release_Notes/chap-Installation.html) for detail.

* how to add EAP6.4 repository

  RHEL7:

      subscription-manager repos --enable jb-eap-6.4-for-rhel-7-server-rpms
      subscription-manager repos --enable jb-eap-6.4-for-rhel-7-server-source-rpms
      subscription-manager repos --enable jb-eap-6.4-for-rhel-7-server-debug-rpms

  RHEL6:

      subscription-manager repos --enable jb-eap-6.4-for-rhel-6-server-rpms
      subscription-manager repos --enable jb-eap-6.4-for-rhel-6-server-source-rpms
      subscription-manager repos --enable jb-eap-6.4-for-rhel-6-server-debug-rpms

* how to add EAP7.0 repository

  RHEL7:

      subscription-manager repos --enable jb-eap-7.0-for-rhel-7-server-rpms
      subscription-manager repos --enable jb-eap-7.0-for-rhel-7-server-source-rpms
      subscription-manager repos --enable jb-eap-7.0-for-rhel-7-server-debug-rpms

* how to add JWS3 repository

  RHEL7:

      subscription-manager repos --enable jws-3-for-rhel-7-server-rpms

* how to add JBCS repository

  RHEL7:

      subscription-manager repos --enable=jb-coreservices-1-for-rhel-7-server-rpms
      subscription-manager repos --enable=jb-coreservices-1-for-rhel-7-server-source-rpms
      subscription-manager repos --enable=jb-coreservices-1-for-rhel-7-server-debug-rpms

  RHEL6:

      subscription-manager repos --enable=jb-coreservices-1-for-rhel-6-server-rpms
      subscription-manager repos --enable=jb-coreservices-1-for-rhel-6-server-source-rpms
      subscription-manager repos --enable=jb-coreservices-1-for-rhel-6-server-debug-rpms

