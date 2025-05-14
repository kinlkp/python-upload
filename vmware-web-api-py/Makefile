# make find hostname=xxxx
findn1:
	 ./vm.py -s n1vsmvcsaa0001.nonprod.empf.local -u 'administrator@nonprod.empf.local' -p "${VMWARE}" \
	 -nossl --datacenter-name Non-Production --action find --vm-name $(hostname)

snapshotn1:
	 ./vm.py -s n1vsmvcsaa0001.nonprod.empf.local -u 'administrator@nonprod.empf.local' -p "${VMWARE}" \
	 -nossl --datacenter-name Non-Production --action snapshot

findp1:
	 ./vm.py -s p1vsmvcsaa0001.prod.empf.local -u 'administrator@prod.empf.local' -p "${VMWARE}" \
	 -nossl --datacenter-name Production --action find --vm-name $(hostname)

snapshotp1:
	 ./vm.py -s p1vsmvcsaa0001.prod.empf.local -u 'administrator@prod.empf.local' -p "${VMWARE}" \
	 -nossl --datacenter-name Production --action snapshot
