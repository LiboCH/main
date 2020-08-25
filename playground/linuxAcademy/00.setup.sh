#!/bin/bash

echo "Create new hosts file"
grep -v la /etc/hosts > /tmp/hosts
i=1
while read l ; do
    h=$(echo "${l}" | cut -d: -f3 )
    echo "${h}" la${i} | tee -a /tmp/hosts
    i=$((i + 1))
done < hosts
sudo mv /tmp/hosts /etc/hosts

echo "Putting ssh key"

while read l ; do
    h=$(echo "${l}" | cut -d: -f3 )
    u=$(echo "${l}" | cut -d: -f1 )
    p=$(echo "${l}" | cut -d: -f2 )

    echo $h
	scp ~/.ssh/id_rsa.pub  ${u}@${h}:~/.ssh/authorized_keys
    ssh -n -t "${u}@${h}" "echo 135atl24! | sudo -S cp -r /home/${u}/.ssh/authorized_keys /root/.ssh" </dev/null
    ssh -n -t "${u}@${h}" "echo 135atl24! | sudo -S sudo yum install -y epel-release" < /dev/null
    ssh -n -t "${u}@${h}" "echo 135atl24! | sudo -S sudo yum install -y ansible" < /dev/null
done < hosts


echo "[la]" 
i=1
while read l ; do
    h=$(echo "$l" | cut -d: -f3 )
    u=$(echo "$l" | cut -d: -f1 )
    p=$(echo "$l" | cut -d: -f2 )
    echo "la${i} ansible_ssh_host=${h} ansible_ssh_user=root" 
    i=$(($i + 1))
done < hosts


