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




######copy key 
set timeout 10  
set username [lindex $argv 0]
set hostname [lindex $argv 1]   
set password [lindex $argv 2]  
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub $username@$hostname
expect {
            #first connect, no public key in ~/.ssh/known_hosts
            "Are you sure you want to continue connecting (yes/no)?" {
            send "yes\r"
            expect "password:"
                send "$password\r"
            }
            #already has public key in ~/.ssh/known_hosts
            "password:" {
                send "$password\r"
            }
            "Now try logging into the machine" {
                #it has authorized, do nothing!
            }
        }
expect eof


