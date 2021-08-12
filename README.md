## checkpr.py

Quick script to make sure PRs are linked to issues, in the right milestone and project catetory, etc. Mostly meets the requirements of the SUSE Rancher K3s/RKE2 team PR process.

### Sample Output
```console
[Release-1.21] Upgrade k3s in 1.21 by @galal-hussein	https://github.com/rancher/rke2/pull/1490
	[closed] [Release-1.21] Systemd does not get notified with READY state in etcd only nodes	https://github.com/rancher/rke2/issues/1485
		Milestone: v1.21.4+rke2r1 - Done Issue / Merged PR
		Closed by: @rancher-max

[release 1.21] bump versions in Windows Dockerfile by @rosskirkpat	https://github.com/rancher/rke2/pull/1484
	[closed] [release 1.21] bump versions in Windows Dockerfile 	https://github.com/rancher/rke2/issues/1482
		Milestone: v1.21.3+rke2r2 - Done Issue / Merged PR
		Closed by: @rancher-max

[backport-1.21] Bump ingress-nginx chart to 3.34.002 by @erikwilson	https://github.com/rancher/rke2/pull/1478
	[closed] Default deployment of rke2-ingress-nginx has load balancer service enabled in RKE2 1.21.2	https://github.com/rancher/rke2/issues/1446
		Milestone: v1.21.3+rke2r2 - Done Issue / Merged PR
		Closed by: @rancher-max

moving all steps into one pipeline for dist dir to be available by @luthermonson	https://github.com/rancher/rke2/pull/1440
	NO LINKED ISSUES FOUND

[Release-1.21] Upgrade k3s bootstrap 121 by @galal-hussein	https://github.com/rancher/rke2/pull/1428
	[closed] [1.21 backport] Agent nodes fail to upgrade via SUC	https://github.com/rancher/rke2/issues/1416
		Milestone: v1.21.3+rke2r1 - Done Issue / Merged PR
		Tag:       v1.21.3+rke2r1
		Closed by: @rancher-max

[release-1.21] Bump kubernetes versions to GA build by @brandond	https://github.com/rancher/rke2/pull/1421
	[closed] [release-1.21] kubectl version should show same tag as RKE2 tag	https://github.com/rancher/rke2/issues/1425
		Milestone: v1.21.3+rke2r1 - Done Issue / Merged PR
		Tag:       v1.21.3+rke2r1
		Closed by: @rancher-max
```
