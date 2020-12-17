import sysv_ipc
import json
from flask import Flask
import random
import redis

max_key = 10000
redis_host = 'redis-master'

r = redis.Redis(
                host=redis_host,
                port=6379,
                password='')


def write_into_kvs(shmid, size, topic, msgsize):
	r.rpush(topic, shmid, size, msgsize)
	for i in range(0,r.llen(topic)):
	 	print "[dbg] the list created: ", r.lindex(topic, i)

app = Flask(__name__)
#create shared memory
#save shmid, topic name 
#returns shmid
@app.route("/createTopic/<string:topicName>/<int:shmSize>/<int:msgSize>")
def createTopic(topicName, shmSize, msgSize):
  shmid = random.randint(0, max_key)
  topics = r.keys()
  if topicName in topics:
    error_msg = str(0) + " " + "Topic Already exists. Will not recreate."
    return error_msg
  try:
    sysv_ipc.SharedMemory(shmid, sysv_ipc.IPC_CREAT, 0666, shmSize, ' ') 
  except:
     error_msg = "Could not create shm because ...\n"
     return str(0) + " " + error_msg
  write_into_kvs(shmid, shmSize, topicName, msgSize)
  return "1" + " " + str(shmid)

#registers subscriber at topic in kv store
@app.route("/subsTopic/<string:topicName>/<string:clientID>")
def subsTopic(topicName, clientID):
  try:
    r.rpush(topicName, clientID)
  except:
    error_msg = "Could not subscribe to topic because ...\n"
    return str(0) + " " + error_msg
  shmid = r.lindex(topicName, 0)
  shmSize = r.lindex(topicName, 1)
  msgSize = r.lindex(topicName, 2)
  return "1" + " " + str(shmid) + " " + str(shmSize) + " " + str(msgSize) 

#
def unsubsTopic(topicName, clientID, detached):
  #client code must have executed sysv_ipc.detach from shm before
  if detached == False:
    error_msg = "Please detach shm in client first"
    return "0" + " " + error_msg 
  try:
    r.lrem(topicName, clientID)
  except:
    error_msg = "Could not unsubscribe because ...\n"
    return "0" + " " + error_msg
  return "1"

#deletes shared memory
#deletes related data in kv store
@app.route("/delTopic/<string:topicName>")
def delTopic(topicName):
  shmid = int(r.lindex(topicName, 0))
  # shm can only be removed after all clients detachs 
  try:
    shm =  sysv_ipc.SharedMemory(shmid)
    shm.detach()
    shm.remove()
    r.delete(topicName)          
  except:
    error_msg = "Could not remove topic because..."  
    return "0" + " " + error_msg
  return "1"

#lists current topics. who is the publiser, subscribers
@app.route("/listTopics")
def listTopics():
  return str(r.keys())

#gets insformation about a specific topic
@app.route("/getTopic/<string:topicName>")
def getTopic(topicName):
  topicInfo = ""
  for i in range(0,r.llen(topicName)):
    topicInfo += str(r.lindex(topicName, i)) + " "
  return topicInfo  

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000) 
