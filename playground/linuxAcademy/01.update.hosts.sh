#!/bin/bash
echo "Create new hosts file"
grep -v la /etc/hosts > /tmp/hosts
i=1
while read l ; do
    h=$(echo "${l}" | cut -d: -f3 )
	ip=$(dig +short "${h}")
    echo "${ip}" la${i} | tee -a /tmp/hosts
    i=$((i + 1))
done < hosts
sudo mv /tmp/hosts /etc/hosts


