import sysv_ipc
import json
import pycurl
from io import BytesIO
from kubernetes import client, config
from kubernetes.client.rest import ApiException



def createTopic(brokerAddr, topicName, shmSize, msgSize):
  # buffer = StringIO()
  # c = pycurl.Curl()
  # url = 'http://' + brokerAddr + ':' + str(5000) + '/createTopic/' + topicName + '/' + str(shmSize) + '/' + str(msgSize)
  # c.setopt(c.URL, url)
  # c.setopt(c.WRITEDATA, buffer)
  # c.perform()
  # c.close()
  # body = buffer.getvalue()
  # if body.split(" ")[0] == '1':
  #   return int(body.split(" ")[1])
  # else:
  #   return 0
  my_resource = {
    "apiVersion": "is.github.com/v1alpha1",
    "kind": "Sharedmemory",
    "metadata": {
      "name": "sharedmemory-programmatic"
    },
    "spec": {
      # Add fields here
      "foo": "bar",
      "topicname": "programmatic",
      "shmsize": 10,
      "msgsize": 10
    }
  }
  config.load_incluster_config()

  my_resource['metadata']['name'] = "sharedmemory-" + topicName
  my_resource['spec']['topicname'] = topicName
  my_resource['spec']['shmsize'] = shmSize
  my_resource['spec']['msgsize'] = msgSize
  api = client.CustomObjectsApi()
  try:
    api.create_namespaced_custom_object(
      group="is.github.com",
      version="v1alpha1",
      namespace="is",
      plural="sharedmemories",
      body=my_resource,
    )
  except ApiException as e:
    print("already exists %s" %e)

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


def initTopic(brokerAddr, topicName):
  buffer = BytesIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(6969) + '/getTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue().decode('UTF-8')
  shmid = int(body.split(" ")[0])
  shmSize = int(body.split(" ")[1])
  msgSize = int(body.split(" ")[2])
  shmem = sysv_ipc.SharedMemory(shmid)
  return shmem, shmSize, msgSize  

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
  createTopic('10.98.89.208', 'perf100', 1024, 16)
  pub = initTopic("10.98.89.208", "perf100")
  shmem = pub[0]
  shmSize = pub[1]
  msgSize = pub[2]
  offset = 0
  data = "Hello World"
  i = 0
#  while True:
  while i < 1000:
#    data = str(i)
    shmem.write(data, offset)
    offset = (offset + msgSize) % shmSize    
    i += 1
#       data = data + str(i)
  return 0
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
