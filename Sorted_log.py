import tarfile
import gzip as g
import sys

def write_data_to_one_file(M , F , FN): #M = member  F = file type FN = file name
    print M.name
    f = t.extractfile(M)
    if F == 3:
        List = f.readlines()
    if F == 2:
        List = g.GzipFile(fileobj=f).readlines()
    if len(List) > 0: # check if the read file is not empty then only go ahead
        output_file = open(FN,'a')
        output_file.writelines(List)
        output_file.close()        

def check_file_type(M): # function to check file type
    f = t.extractfile(M)
    if M.isdir():
        return 1
    elif f.read(2).encode("hex") == GZIP_MAGIC_NUMBER: # Read first 2 bytes to check the magic number
        return 2
    elif M.isfile():
        return 3

GZIP_MAGIC_NUMBER = "1f8b" # magic number to confirm it is a gzip file
file_name = "var_log.tar.gz" # "var_log.tgz"

t = tarfile.open(file_name, 'r:*') #open tar file in read mode 

tar_mem_name = t.getnames() #get the tar member names
tar_mem_name.sort(reverse=True) # sort tar member names list in reverse order

for i in tar_mem_name:
    if "/var/log/syslog" in i:
        file_type = check_file_type(t.getmember(i)) # check file type (dir/gzip/text) it will return 1 for dir , 2 for gzip and 3 for text file
        write_data_to_one_file(t.getmember(i),file_type , 'syslog')
    if "/var/log/messages" in i:
        file_type = check_file_type(t.getmember(i)) 
        write_data_to_one_file(t.getmember(i),file_type , 'messages')
    if "/var/log/chassisd" in i:
        file_type = check_file_type(t.getmember(i)) 
        write_data_to_one_file(t.getmember(i),file_type , 'chassisd')