#*ArcSight Use Case* 

#*Mapping Auditd UID to Username*

The Linux C2 auditing tool auditd event log type outputs integer UID's which are not useful in the context of correlation across thousands of Linux systems. From a correlation perspective and an Identity View perspective and in an effort to detect standard Cyber intrusion sets and Insider Threat activities on Linux systems, it becomes highly useful to convert integer UID's to string usernames for monitoring purposes, leveraging ArcSight map file functionality to get one attribute and reset said attribute with the desired attribute. Furthermore, this use case when run from a more aggressive crontab schedule can serve as a rudiment ability to detect in realtive real time the addition or subtraction of a user account/s from a 
Linux server system.

#*Special Requirements*


1.) Use case can function for a remote or native smart connector whether you are utilizing syslog/syspipe/file smart connectors

2.) Remote methodology requires uncommenting of an Rsync over SSH function within the attached script to push the updated map file on schedule to the remote connector collection system housing the smart connector whose map file needs to be updated. The solution can scale out to meet the requirements of a remote collection smart connector array. Note that Rsync will need to be leveraged in order to overwrite the remote map file of the smart connector in question.

#*Methodology*

1.)The attached Python script will run from Linux cron.hourly - or if standard cyber intrusion set monitoring is the objective then set a more aggressive crontab schedule of every minute, and you will have as afore stated a rudiment methodology to detect additions or subtractions of user accounts on the Linux system under monitoring.

2.) The script simply culls all UID's, that possess a system $SHELL, and their corresponding username from the /etc/passwd file, populating a mapfile. Where the getter is the ArcSight schema field event.deviceCustomNumber3 and the setter is the ArcSight schema field event.sourceUserId.
Resultant map file entries will appear as such.

UID,Usename

0,root


3.) Within the ArcSight Console the auditd data type will then appear with ArcSight schema field event.sourceUserId populated with the username that generated the auditd event log entry. This becomes very useful for Identity View user tracking, or user access tracking in general on Linux based systems.

4.) Note that the attached script can function if the ArcSight Linux Syspipe Smart Connector is installed native, or if the remote smart connector is utilized, in which case the Python script includes an rsync over ssh function to transfer the map file product to the remote system housing the ArcSight Smart Connector.

5.) cull_uid.cron script can be placed in /etc/cron.hourly or in /etc/cron.daily otherwise if you wish to run every minute for a more agressive monitoring solution then set the following cront entry for the root user running the cronjob

*/1 * * * * /usr/bin/python /opt/app/arcsight/cull_uid.py > /var/tmp/cull_uid_output

#*Tools Utilized in Testing and Validation of this Use Case*

ArcSight 5.2 Patch 1&
Current Version ArcSight Linux Syspipe Smart Connector&
Python 2.7.3&
OpenSSH Client & Server&
Rsync&
Linux crontab

#*Tested On*

Red Hat Enterprise Linux 5 & Red Hat Enterprise Linux 6

#*Dependency NOTE:*

cull_uid.py and error_handle.py must be in the same working directory as error_handle.py is called by cull_uid.py
