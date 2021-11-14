```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/

curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/

curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

Minikube 也支持 --vm-driver=none 选项来在本机运行 Kubernetes 组件，这时候需要本机安装了 Docker。

---
## 000

```bash
minikube start --vm-driver=none

kubectl get nodes

kubectl create namespace my-namespace

kubectl config set-context $(kubectl config current-context) --namespace=my-namespace

kubectl get pods -n default

kubectl config get-contexts
```

---
## 001
`kubectl create deployment multitool --image=praqma/network-multitool`

creates a deployment named multitool, which creates a replicaset, which starts a pod using the docker image
创建一个名为multitool的部署，它创建一个复制集，使用docker映像启动一个pod

`kubectl get deployment,replicaset,pod`

`kubectl expose deployment multitool --port 80 --type NodePort`

`kubectl get service multitool`

`kubectl get nodes -o wide  `

`kubectl create -f support-files/nginx-simple-deployment.yaml`


> ServiceMesh Envoy Istio FaaS

---
问题：

In Kubernetes 1.16 some api has been changed.

[apiVersion](https://stackoverflow.com/questions/58481850/no-matches-for-kind-deployment-in-version-extensions-v1beta1)
