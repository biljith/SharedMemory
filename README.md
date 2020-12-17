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


# Other helpful commands
## Change default namespace
kubectl config set-context --current --namespace=<insert-namespace-name-here>

## Run an alpine container
kubectl run -it --rm --restart=Never alpine --image=alpine sh

## Build containers on minikube's docker env and not local. Run the following before building your docker env and don't use sudo
eval $(minikube docker-env)

## Get the IP address of the broker service
kubectl describe services/broker-service
