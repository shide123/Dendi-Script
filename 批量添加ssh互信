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

rm -rf /root/.ssh
chmod 755 ssh_keygen.sh
sh ssh_keygen.sh

cat $3 | while read line
do
  ssh-copy-id -i $ssh/id_rsa.pub $2@$line
done
