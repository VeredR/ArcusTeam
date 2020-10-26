
import json
import re
import os.path
from os import path
import binascii
import time


class returnType:
   {'range' : None,'size' : None,'repeating_byte' : None}

   def __init__(self,range,size,repeating):
      self.range = range
      self.size = size
      self.repeating_byte = repeating


def match_maker(path:str,expr:dict)->json:
   result :dict = {}#my JSON result will be inserted here
   if not expr or len(expr) == 0: #checking if the expressions exist or not
      print("no expr")
      return json.dumps(result)
   if not os.path.exists(path):
      print("no file")
      return json.dumps(result)
   if os.path.exists(path):#checking if the file exists or not
      ind = 0 # the general index from which we read from
      if os.path.isdir(path):
         print("given a directory, not a file")
         return json.dumps(result)   
      myByte = None
      regex = re.compile('')
      with open(path,'rb') as f:
         if os.path.isfile(path): #checking if it is a file 
            if not myByte:
               myByte =  f.read(16)
               if not myByte:
                  print("empty file")
                  return json.dumps(result)
               while myByte:  
                  myByte = binascii.hexlify(myByte)
                  for exp in expr.keys():
                     if str(exp) != str(expr[exp]):# hex string
                        exp = bytes(exp,encoding='utf8')
                        if myByte == binascii.hexlify(exp) or binascii.hexlify(exp) in myByte:
                           
                           rec = returnType((str(myByte).index(binascii.unhexlify(exp))+ind,ind+len(str(exp))),len(str(exp)),binascii.unhexlify(exp.decode('utf8')))
                           result[ind]=rec.__dict__
                           ind += len(exp)
                     elif  str(exp) == str(expr[exp]) or [r'\\','.','?','*','+','[]','^','$'] in str(binascii.unhexlify(exp.decode('ascii'))):# regex
                        exp = binascii.hexlify(bytes(exp,encoding='utf8'))
                        regex = re.compile(exp)
                        for match_obj in regex.findall(myByte):
                           if match_obj != None:
                             
                              rec = returnType((ind,ind+len(match_obj)),len(match_obj),str(binascii.unhexlify(exp.decode('ascii'))))

                              result[ind] = rec.__dict__
                              ind += len(match_obj)                 
                              myByte =  f.read(16)
                  myByte = f.read(16)
                  ind += 16
              
   elif not os.path.exists(path):
      print("file does not exit")
   
                           

   if result:
      myResult = '['
      for i in result:
         myResult+=json.dumps({'range': result[i]['range'],'size':result[i]['size'],'repeating_byte':result[i]['repeating_byte']})+','
      myResult= myResult[0:len(myResult)-1]
      myResult +=']'
      return json.dumps(myResult)
   else:
      return json.dumps(('not found'))





if __name__ == '__main__':
   myFile = "redfin-rd1a.200810.020/bootloader-redfin-r3-0.3-6776358.img"
   myExp = {r"\x00":r"\x00",'^[01]+':'^[01]+','01+':'01+',"\\x00":"\\x00","\X00":"\X00","34":"34","\\x00":"\x00"}
  
   match = json.loads(match_maker(myFile,myExp))
   print(match)
  
   
   myExp ={'5D00008000': 'lzma','27051956': 'uImage','18286F01': 'zImage','1F8B0800': 'gzip','303730373031': 'cpio',
   '303730373032': 'cpio','303730373033': 'cpio','894C5A4F000D0A1A0A': 'lzo','5D00000004': 'lzma',
   'FD377A585A00': 'xz','314159265359': 'bzip2','425A6839314159265359': 'bzip2','04224D18': 'lz4',
   '02214C18': 'lz4','1F9E08': 'gzip','71736873': 'squashfs','68737173': 'squashfs','51434454': 'dt','D00DFEED': 'fit','7F454C46': 'elf'}
   
   
   print(match_maker(myFile,myExp))
   
   
  
   
