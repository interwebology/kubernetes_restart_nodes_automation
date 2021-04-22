# Restart or Alert On Nodes That stay NotReady for over 5 Minutes.

**This was meant to reboot nodes in lab environments which it could still be used for with small adjustments to the script**

This script uses kubectl to switch between contexts listed in lab_cluster.txt and records NotReady nodes. 

If a node stays down for more then 5 minutes then a email is sent to the team members listed in the script.

An alert email has the following text.

```
Nodes in NotReady State
 

dev-cluster
172.27.120.44
172.27.120.4

cluster-lake-01
172.72.17.21
```

## Installation 



### kubectl

install using kubectl site instructions.

You can find more information about configuring kubectl [HERE](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

You will now need to use the secure copy command to transfer the file into your hosting VM

```
scp kubectl root@172.27.223.21:~
```
Now SSH into your box home directory and make the kubectl binary executable.

```
 chmod +x ./kubectl 
```

Move the binary in to your PATH.

```
 sudo mv ./kubectl /usr/local/bin/kubectl
```

### now configure kubectl 

You can find more information about configuring kubectl [HERE](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### Install packages

+ sudo yum install python-pip
+ sudo pip install jinja2

### Copy over kube_monitor.py script

Inside the repo on your local machine move app over to /usr/local/bin/app and 
add this to the remotes path

```
scp -r app root@172.27.123.21:/usr/local/bin/
```

### Add to Path

```
echo 'export PATH=$PATH:/usr/local/bin/app' >> ~/.profile 
```
then 

```
source ~/.profile
```
### Set Timezone
```
ln -sf /usr/share/zoneinfo/America/Denver /etc/localtime
```

### Setup The Script Cron Job

Edit the crontab by using the following command

```
crontab -e
```
The following top line starts the script at 9am Monday-Friday
and the bottom goes and kills the script at 5pm Moday-Friday

```
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/app:~/.kube

0 9 * * 1-5 nohup /usr/bin/python /opt/app/kube_monitor.py  >> /tmp/kube_monitor.log 2>&1
0 17 * * 1-5 pkill -f kube_monitor.py
```

### The lab_cluster.txt file

This file contains a cluster on each line and must be in the same folder as the kube_monitor script. These are the clusters you have setup for use with your kubectl.

**Congrats, You did the thing.**
