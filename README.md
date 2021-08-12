## checkpr.py

Quick script to make sure PRs are linked to issues, in the right milestone and project catetory, etc. Mostly meets the requirements of the SUSE Rancher K3s/RKE2 team PR process.

### Sample Output
```console
[Backport 1.21] Bumped k3s version to bring in updated HNS Network  call. by @phillipsj	https://github.com/rancher/rke2/pull/1606
	[open] [Backport 1.21] The waitManagementIP function in pkg/daemons/agent/agent_windows.go is calling the incorrect HNS function.	https://github.com/rancher/rke2/issues/1604
		Milestone: v1.21.3+rke2r2 - To Test
		Tag:       v1.21.3-rc5+rke2r2

[Release 1.21] - Update k3s to resolve for s3 folder handling when listing snapshots by @briandowns	https://github.com/rancher/rke2/pull/1601
	[open] s3 snapshots do not show in the rancher 2.6 UI	https://github.com/rancher/rke2/issues/1551
		Milestone: v1.22.0+rke2r1 - To Test
		Tag:       v1.21.3-rc5+rke2r2

[release 1.21] bump calico to 3.19.2 by @rosskirkpat	https://github.com/rancher/rke2/pull/1594
	[open] [release 1.21] bump calico to 3.19.2	https://github.com/rancher/rke2/issues/1593
		Milestone: v1.21.3+rke2r2 - To Test
		Tag:       v1.21.3-rc5+rke2r2

[release-1.21] Update Calico version to v3.19.2 by @manuelbuil	https://github.com/rancher/rke2/pull/1587
	[open] [release-1.21] RKE2 Cluster running Calico seemingly losing UDP traffic when transiting through service IP to remotely located pod	https://github.com/rancher/rke2/issues/1586
		Milestone: v1.21.4+rke2r1 - To Test
		Tag:       v1.21.3-rc5+rke2r2

[release-1.21] Bump hardened-kubernetes to v1.21.3-rke2r2 by @brandond	https://github.com/rancher/rke2/pull/1583
	[closed] [release-1.21] Cluster is stuck in upgrading state when upgrading to v1.21.3-rc4+rke2r2	https://github.com/rancher/rke2/issues/1581
		Milestone: v1.21.3+rke2r2 - Done Issue / Merged PR
		Tag:       v1.21.3-rc5+rke2r2
		Closed by: @rancher-max

[Release-1.21] Update k3s to fix node stuck on removal by @galal-hussein	https://github.com/rancher/rke2/pull/1543
	[closed] [Release-1.21] Node stuck at deletion due to finalizer 	https://github.com/rancher/rke2/issues/1561
		Milestone: v1.21.3+rke2r2 - Done Issue / Merged PR
		Tag:       v1.21.3-rc5+rke2r2
		Closed by: @rancher-max
```
