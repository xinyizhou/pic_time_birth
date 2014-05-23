import os
import stat
import time
import exifread
from datetime import date

SUFFIX_FILTER = ['.jpg','.png','.mpg','.mp4','.thm','.bmp','.jpeg','.avi','.mov']
DELETE_FILES = ['thumbs.db','sample.dat']


def lele_birth(y,m,d):
    n1 = date(2013,07,26)
    n2 = date(int(y),int(m),int(d))
    n3 = n2 - n1
    return '_lele_'+str(n3.days+1)+'_days'
        
def isTargetedFileType(filename):
    filename_nopath = os.path.basename(filename)
    f,e = os.path.splitext(filename_nopath)
    if e.lower() in SUFFIX_FILTER:
        return True
    else:
        return False    

def isDeleteFile(filename):
    filename_nopath = os.path.basename(filename)
    if filename_nopath.lower() in DELETE_FILES:
        return True
    else:
        return False   
        
def generateNewFileName(filename):
    try:
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
        else:
            raise "[%s] is not a file!\n" % filename
    except:
        raise "unopen file[%s]\n" % filename
        
    data = exifread.process_file( fd )
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            tmp_t = str(t).replace(":","-")[:10]
            dateStr = tmp_t + "_" + str(t)[11:].replace(":","") + lele_birth(tmp_t.split('-')[0],tmp_t.split('-')[1],tmp_t.split('-')[2])
        except:
            state = os.stat(filename)
            tmp_t = time.strftime("%Y-%m-%d", time.localtime(state[-2]))
            dateStr = time.strftime("%Y-%m-%d_%M%H%S", time.localtime(state[-2])) + lele_birth(tmp_t.split('-')[0],tmp_t.split('-')[1],tmp_t.split('-')[2])
    else:
        state = os.stat(filename)
        tmp_t = time.strftime("%Y-%m-%d", time.localtime(state[-2]))
        dateStr = time.strftime("%Y-%m-%d_%M%H%S", time.localtime(state[-2])) + lele_birth(tmp_t.split('-')[0],tmp_t.split('-')[1],tmp_t.split('-')[2])
    
    dirname = os.path.dirname(filename)
    filename_nopath = os.path.basename(filename)
    f,e = os.path.splitext(filename_nopath)
    
    newFileName = os.path.join(dirname, dateStr + e).lower()
    return newFileName
    

def scandir(startdir):
    os.chdir(startdir)
    for obj in os.listdir(os.curdir) :
        if os.path.isfile(obj):
            if isTargetedFileType(obj):
                print obj
                newFileName = generateNewFileName(obj)
                print "rename [%s] =&gt; [%s]" % (obj, newFileName)
                os.rename(obj, newFileName)
            elif isDeleteFile(obj):
                print "delete [%s]: " % obj
                os.remove(obj)
            else:   
                pass

        if os.path.isdir(obj) :
            scandir(obj)
            os.chdir(os.pardir)
    

if __name__ == "__main__":
    path = "/Users/xinyizhou/Desktop/lele_91"
    scandir(path)