#!/bin/bash
#please run as root 

if [ $# -ne 3 ]; then  
    echo "Usage:"  
    echo "$0 remoteUser remotePassword hostsFilePath"  
    exit 1  
fi

cd /root
masteruser=root
dstuser=$1
dstpass=$2
host_file=$3

cd /root
################prepare root key
cat << EOF >ssh_keygen.sh
#!/usr/bin/expect
spawn ssh-keygen
expect "*Enter file in which to save the key*"
send "\r"
expect "*Enter passphrase*"
send "\r"
expect "*Enter same passphrase again*"
send "\r"
interact
EOF

#############prepare send key
cat << EOF >ssh-copy-id.sh
keypath=$1
dstuser=$2
dstip=$3
dstpass=$4
#!/usr/bin/expect
spawn ssh-copy-id -i $keypath/id_rsa.pub $dstuser@$dstip
expect "*password*"
send "$dstpass\r"
expect "*ssh*"
send "\r"
interact
EOF

###########################################################################


#start to gen key
keypath=/root/.ssh
rm -rf $keypath
chmod 755 ssh_keygen.sh
sh ssh_keygen.sh

#send key to dest
cat $3 | while read line
do
  sh ssh-copy-id.sh $keypath $dstuser $line $dstpass
done


