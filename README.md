# About
The goal of this project was to augment the work done for the research project [Shimmy](https://www.usenix.org/system/files/hotedge19-paper-abranches.pdf) by adding the feature to be able to specify creation of shared memory as a native Kubernetes object, i.e. using yaml files. This project accomplished that by using [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and Custom Controllers. The Custom Controller was built using [kubebuilder](https://book.kubebuilder.io/).

## Current Flow
When a user creates a shared memory object (for eg. using kubectl apply -f example-sharedmemory.yml) the controller gets notified. The controller in turn contacts each broker service (currently only one but in the future one per host) to create
the shared memory on the host it resides on. The broker service exposes an endpoint /createTopic for this purpose. Once the shared memory is created, the publisher can get info about the topic (shared memory id) using the /getTopic endpoint and write to the shared memory. Subscribers can subscribe to the topic using /substopic endpoint and start reading from the shared memory. The responsibility of maintaining the offset in the shared memory resides on the subscribers. All the publisher and subscriber pods need to set hostIPC to true to be able to use shared memory.

## Shared Memory object
The shared memory json should have 3 fields
- topicname
- shmsize 
- msgsize
all of which are self explanatory. See sharedmemory-kubebuilder/config/samples/is_v1alpha1_sharedmemory.yaml for an example

## Future work.
The current status is that shared memory works with kubernetes as long as there is a single host. To support multiple hosts, we need multiple broker services one on each host. The shared memories on these hosts should be synced by using [RDMA](https://github.com/goodarzysepideh/RDMA). Other issue that needs to be tackled is how to schedule the creation of publishers and subscriber pods so they mostly reside on the same host to avoid using RDMA.

## Resources
1. https://learning.oreilly.com/library/view/programming-kubernetes/9781492047094/

# Setup
## Create redis pod
kubectl apply -f redis-master.yml

## Create shimmy pod, shimmy service and the pub sub pods
kubectl apply -f pod.yaml

## Create a directory inside GOPATH
cd ~/go/src && mkdir sharedmemory-kubebuilder

## kubebuilder init
kubebuilder init --domain github.com --license apache2 --owner "Biljith Thadichi"

## Create api
kubebuilder create api --group is --version v1alpha1 --kind Sharedmemory

## Create dedicated namespace and set it as default
kubectl create ns is && kubectl config set-context $(kubectl config current-context) --namespace=is

## Install CRD
make install

## Run the custom controller
make run

## Configure CRD
kubectl apply -f config/crd/bases/is.github.com_sharedmemories.yaml
kubectl get crds

## Create a sample CRD. Look for the example CRD in this repo under config/samples
kubectl apply -f config/samples/is_v1alpha1_sharedmemory.yaml

## Now the controller should show an output related to the custom resource you tried to create.
## Now we need to package this controller into an image
1. docker login
2. make docker-build IMG={username}/sharedmemory-controller
3. make docker-push IMG={username}/sharedmemory-controller
4. Open config/default/kustomization.yaml and change the namespace to is
5. make deploy will deploy your controller

## Now to install the reader and writer. Run the build commands in the respective directory of the reader and writer
1. eval $(minikube docker-env)
2. docker build -t kubernetes/writer .
3. docker build -t kubernetes/reader .
4. kubectl apply -f pod.yaml


## Other helpful commands
## Change default namespace
1. kubectl config set-context --current --namespace=<insert-namespace-name-here>

## Run an alpine container
kubectl run -it --rm --restart=Never alpine --image=alpine sh

## Build containers on minikube's docker env and not local. Run the following before building your docker env and don't use sudo
eval $(minikube docker-env)

## Get the IP address of the broker service
kubectl describe services/broker-service