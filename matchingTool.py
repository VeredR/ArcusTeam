import json
import re
import os.path
from os import path


def match_maker(path,*expr):

   result = json.dumps({})#my JSON result will be inserted here
   if not expr or len(expr) == 0: #checking if the expressions exist or not
      print("no expr")
      return result
   if os.path.exists(path):#checking if the file exists or not
      firmwareTypes = ["bin", "zip", "gzip","img","squashfs","cramfs","JFFS2","yaffs2","ext2","LZMA","zlib","ARJ"]
      ind = 0 # the general index from which we read from
      with open(path,'rb') as f:
         if os.path.splitext(f)[1] in firmwareTypes: #checking if it is a firmware file
            byte = f.read(1)
            while byte: #looping through the file byte by byte and finding the matches and adding them to the result json
               for exp in expr.keys():
                  if exp not in expr.values() and exp in byte: #specific non regular expression
                     result.append({'range':(hex(byte.index(exp))+ind,hex(byte.index(exp)+len(exp))+ind),"size": len(exp),'repeating_byte':expr[exp]})
                     ind += len(exp) - 1
                  elif exp in expr.values() and exp in byte: #regular expression
                     if 'x' in exp and exp.index('x') == 0 or 'X' in exp and exp.index('X') == 0 :
                        pattern = re.compile(b"{expr}")
                        expList = pattern.findall(pattern,byte)
                        if expList and not len(expList) == 0:
                           for exp in expList:
                              if exp:
                                 result.append({'range':(hex(byte.index(exp))+ind,hex(byte.index(exp)+len(exp))+ind),"size": len(exp),'repeating_byte':expr[exp]})
                                 ind += len(exp) - 1
               byte = f.read(1)         
      
            return result
         elif os.path.splitext(f)[1] not in firmwareTypes:
            print("not a binary file ")
            return result
   elif not os.path.exists(path):
      print("no path")
      return result



if __name__ == '__main__':
    print(match_maker("", dict()))