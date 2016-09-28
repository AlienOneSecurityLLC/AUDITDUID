#!/usr/bin/env python

'''
Date Aug 7, 2012
'''
###########
'''
Disclaimer: All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''
##########

__author__ = "Justin Jessup & Adam Reber"

import os, shutil, glob, datetime

def list_files(path_name):
    """
    function to list files in a directory path
    """
    glob_paths = glob.glob(path_name)
    for path in glob_paths:
        yield path

def head_file(file_name, line_count):
    """
    Python implementation of Linux/Unix head utility - output first N lines of file
    """
    return [s for (i, s) in enumerate(open(file_name)) if i < line_count]

def which_mapfile(path_name):
    """
    Determine the next map file we can write to - if map.0.properties exits - else default map.0.properties
    """
    file_list = []
    map_filter = "map.*.properties"
    for file_name in list_files(os.path.join(path_name, map_filter)):
        file_list.append(int(file_name.split('.')[1]))
    if not file_list:
        return "map.0.properties"
    else:
        file_num = str(max(file_list))
        file_name = "map." + file_num + ".properties"
        
	line = head_file(os.path.join(path_name, file_name), 1)[0]
	if 'UID' in line:
            os.remove((os.path.join(path_name,file_name)))
            return file_name
        else:
            return "map." + str(max(file_list) + 1) + ".properties"

def cull_uid(map_file, file_name):
    """
    cull/pull username and UID from /etc/passwd
    getter ArcSight schema field deviceCustomNumber3
    setter ArcSight schema field sourceuserName
    write output to identified free map.*.properties file
    """
    a1 = open(file_name, 'r')
    user = [ (i.split(':')[0],i.split(':')[2]) for i in a1 if "/nologin" not in i ]
    f = open(map_file,"w")
    date_time_one = (str(datetime.datetime.now()).split(' ')[0])
    date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
    f.write("# UID mapfile " +date_time_one+ '-' +date_time_two + '\n')
    f.write("event.deviceCustomNumber3,set.event.sourceUserName\n")
    [ f.write("%s,%s\n" % (i[1],i[0])) for i in user if "sudcoadm" not in i]
    f.close()
    a1.close()
    
def mov_map(src_path, dst_path):
    """
    new map file is created within current working directory
    move the new map file to the correct $ARCSIGHT_CONNECTOR_HOME/map $PATH location
    """
    if os.path.isfile(dst_path):
        os.remove(dst_path)
    
    if os.path.isfile(src_path):
        try:
            shutil.copy(src_path, dst_path)
        except IOError:
            print "ERROR: cannot write file to destination."
    else:
        print "ERROR: cannot open source file."
    
def main():
    """
    If the script is rerun via Tivoli remove any previous
    Map file in the current working directory
    """
    path_name = "/opt/app/arcsight/sys_pipe/current/user/agent/map/"
    file_name = which_mapfile(path_name)
    """
    Cull usernames and UID's from passwd file
    """
    cull_uid(file_name, "/etc/passwd")
    dst_path = "/opt/app/arcsight/sys_pipe/current/user/agent/map/" + file_name
    mov_map(file_name, dst_path)

# Execution Main Function
if __name__ == '__main__':
    main()
