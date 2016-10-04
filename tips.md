tips
---

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

* how to add JWS3 repository

  RHEL7:

      subscription-manager repos --enable jws-3-for-rhel-7-server-rpms

