# get list of root directory    # get file filters
# get all file information
# store file information in a db?
# index seg of fn

# monitor of change???

# search GUI ? 
# get input for search
# name : more than 1 character
# size/time
# op? fuzzy? 

import scandir

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.
    for path, subdirs, files in scandir.walk(directory):
        for filename in files:
            filepath = (filename, path)  # better to include extension in fn as a single search target (but seg particluarly )
            # fd = [root]            # fn = filename.rsplit('.', 1)             # if len(fn)==1 then fn.append('')
            # fd.append( fn )   # bad split if some system have no concept of posfix and take . as a normal char
            ## Join the two strings in order to form the full filepath.
            ## os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.

mypath='d:\\'
fL = get_filepaths(mypath)

import sqlite3
conn = sqlite3.connect(r'd:\testfm1.db')
cur = conn.cursor()
cur.execute( 'drop table if exists filelist' )  # include extension in fn as a single search target (but seg particluarly )
cur.execute( 'create table if not exists filelist(fn, path)' )  # include extension in fn as a single search target (but seg particluarly )
conn.commit()

cur.executemany( 'insert into filelist values (?,?)', fL )
conn.commit()

cur.execute( 'drop table if exists seglist' )  # include extension in fn as a single search target (but seg particluarly )
cur.execute( 'create table if not exists seglist(seg, fn)' )  # include extension in fn as a single search target (but seg particluarly )
conn.commit()

def substr(string, minlen=0, maxlen=-1):  # value of len para is str's max index, actual length is 1 + para value
    a=[] #set()
    # better if 2-bytes coding can be identified
    for length in range(minlen, len(string)):
        for start in range(len(string)-length):
            a.append(string[start:start+length+1])
        if maxlen==length: break
    return a


def rSubstr(string):
    a=[] #set()
    # better if 2-bytes coding can be identified
    for leftTrunc in range(len(string)):
      a.append(string[leftTrunc:])
    return a


def splits(str, delimiters):
  rslt = []
  tmps = ''
  for c in list(str):
    if c not in delimiters:
      tmps += c
    else:
      rslt.append( tmps )
      tmps = ''
  rslt.append( tmps )
  return rslt


def segStr(string, minl=0, maxl=-1):  # value of len para is str's max index, actual length is 1 + para value
    a=[] #set()
    tmp = string.rsplit( '.', 1 )
    if len(tmp)>1:
      a.append( tmp[1] )
    fpLongNameFileLog = open( 'LongNameFile.log', 'a' )
    #if len( tmp[0] ) > 20:
    tmpSegs = splits( tmp[0], ' .-_~{}' )
    segNum = len( tmpSegs )
    for s in tmpSegs:
      if len(s) > 30:  # multi-words? what strategy? what will be such string? further split with ~() ?
        if segNum > 2:  # !!! need to optimize how to search if this long seg is the only seg of this fn
          fpLongNameFileLog.write( string.encode('utf8') ) #print string # replace with log later
          fpLongNameFileLog.write( '\n' ) #print string # replace with log later
          continue
      a.extend( substr(s, min( len(s)/5, 2 ), maxlen=maxl) )
    #else:
    #  a = substr( tmp[0], min( len(tmp[0])/5, 2 ), maxlen=maxl )
    fpLongNameFileLog.close()
    return a


segFnList = []
fpHeaveSegFileLog = open( 'HeavySegFile.log', 'w' )
for fn,path in fL:
  segList = segStr(fn, maxl=8)  #set( substr(fn) )
  if len(segList)>50:
    #print len(segList), fn    #break
    fpHeaveSegFileLog.write( fn.encode( 'utf8' ) )
    fpHeaveSegFileLog.write( '\n' )
  #segFnList.append( len(segList) )
  for seg in segList:
    segFnList.append( (seg,fn) )

fpHeaveSegFileLog.close()

cur.executemany( 'insert into seglist values (?,?)', list( set(segFnList) ) )
conn.commit()




l=[('a','aa'),('b','bb'),('b','bb'),('b','bbb')]


########################################################################################

# chip scale

# slice
# n n-1 ... 1      n(n+1)/2
# n n-1 ... n-l+1  l(n+n-l+1)/2    len between 1 and maximum l
# 1 2 ... m+1      (m+1)(m+1+1)/2  len between n-0 and minimum n-m 
# m=n-6            (n-5)(n-4)/2    n/2 + 9n/2 - 20/2 = 5n-10
# m=n-7            (n-6)(n-5)/2    n/2 + 11n/2 - 30/2 = 6n-15
# m=n-8            (n-7)(n-6)/2    n/2 + 13n/2 - 42/2 = 7n-21
# m=n-9            (n-8)(n-7)/2    n/2 + 15n/2 - 56/2 = 8n-28
# m=n-10           (n-9)(n-8)/2    n/2 + 17n/2 - 72/2 = 9n-36

# word style name???with empty  the word with maximum length 
# char seach | word search
# Ë«×Ö½Ú±àÂë

# n:1-5      sub:1-n                                             n(n+1)/2
# n:6-8      sub:2-n        1(2n-1+1)/2=n      n(n+1)/2 - n    = n(n-1)/2
# n:9-...    sub:3-6        2(2n-2+1)/2=2n-1   8n-28 - (2n-1)  = 6n-27
# n>20???












# con: version search v3.2.1
def segStr1(string, minl=0, maxl=-1):  # value of len para is str's max index, actual length is 1 + para value
    a=[] #set()
    tmp = string.rsplit( '.', 1 )
    if len(tmp)>1:
      a.append( tmp[1] )
    fpLongNameFileLog = open( 'LongNameFile.log', 'a' )
    #if len( tmp[0] ) > 20:
    tmpSegs = splits( tmp[0], ' .-_~{}' )
    segNum = len( tmpSegs )
    for s in tmpSegs:
      if len(s) > 30:  # multi-words? what strategy? what will be such string? further split with ~() ?
        if segNum > 2:  # !!! need to optimize how to search if this long seg is the only seg of this fn
          fpLongNameFileLog.write( string.encode('utf8') ) #print string # replace with log later
          fpLongNameFileLog.write( '\n' ) #print string # replace with log later
          continue
      a.extend( substr(s, min( len(s)/5, 2 ), maxlen=maxl) )
    #else:
    #  a = substr( tmp[0], min( len(tmp[0])/5, 2 ), maxlen=maxl )
    fpLongNameFileLog.close()
    return a
