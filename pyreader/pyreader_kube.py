import sysv_ipc
import json
import pycurl
from io import BytesIO
from textblob import TextBlob

def createTopic(brokerAddr, topicName, shmSize, msgSize):
  buffer = BytesIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(6969) + '/createTopic/' + topicName + '/' + str(shmSize) + '/' + str(msgSize)
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue().decode('UTF-8')
  if body.split(" ")[0] == '1':
    return int(body.split(" ")[1])
  else:
    return 0

def getShmId(brokerAddr, topicName):
  buffer = BytesIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(6969) + '/getTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue().decode('UTF-8')
  return int(body.split(" ")[0])

def delTopic(brokerAddr, topicName):
  shmid = getShmId(brokerAddr, topicName)
  shm =  sysv_ipc.SharedMemory(shmid)
  shm.detach()
  buffer = BytesIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(6969) + '/delTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue().decode('UTF-8')
  if body == '1':
    return 1
  else:
    return 0


#returns tupple with shmem,  
def subsTopic(brokerAddr, topicName, clientID):
  buffer = BytesIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(6969) + '/subsTopic/' + topicName + '/' + clientID
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue().decode('UTF-8')
  if body.split(" ")[0] == '1':
    shmid = int(body.split(" ")[1])
    shmSize = int(body.split(" ")[2])
    msgSize = int(body.split(" ")[3])
    shmem = sysv_ipc.SharedMemory(shmid)
    return shmem, shmSize, msgSize
  else:
    return 0,0,0



def main():
  subs = subsTopic("10.98.89.208", "perf100", "c1")
  shmem = subs[0]
  shmSize = subs[1]
  msgSize = subs[2]
  print("shmem id is %s" %shmem)
  offset = 0;
  i = 0
  total = 1000
  while True:
   mem_data = shmem.read(msgSize, offset).decode("utf-8")
   find_data=mem_data.find('\0')
   data=mem_data[:find_data]
   if (data != ""):
     print(data)
     print(TextBlob(data).sentiment)
     i += 1
   if i > total:
     break
   #print offset
   offset = (offset + msgSize) % shmSize    
   
main()
#memory = sysv_ipc.SharedMemory(123456)


#while True:
#  memory_value = memory.read()
#  i=memory_value.find('\0')
#  data=memory_value[:i]
#  print data

#memory.detach()

#memory.remove()
#print len(memory_value)
