
```shell
kind get clusters
```
1- 
## kind config
* dc1
```shell
kind delete cluster --name dc1
kind create cluster --config k8s/kind-config-dc1.yaml
```

* dc2
```shell
kind delete cluster --name dc2
kind create cluster --config kind-config-dc2.yaml
```


2. build et chargement des images  


```shell
docker build -t auth:latest ../auth
kind load docker-image auth:latest --name dc1
kind load docker-image auth:latest --name dc2
```

- product
```shell
docker build -t product:latest ../product
kind load docker-image product:latest --name dc1
kind load docker-image product:latest --name dc2
```

- workers
```shell
docker build -t workers:latest ../workers
kind load docker-image workers:latest --name dc1
kind load docker-image workers:latest --name dc2
```

3- deployment des manifests

## dc1

```shell
kubectl --context kind-dc1 apply -f k8s/database/auth
kubectl --context kind-dc1 apply -f k8s/database/product
kubectl --context kind-dc1 apply -f k8s/database/couchdb
kubectl --context kind-dc1 apply -f k8s/database/redis
kubectl --context kind-dc1 apply -f k8s/auth/
kubectl --context kind-dc1 apply -f k8s/product/
kubectl --context kind-dc1 apply -f k8s/rabbitmq/
kubectl --context kind-dc1 apply -f k8s/workers/
kubectl --context kind-dc1 apply -f k8s/kong/
```

## dc2
```shell
kubectl --context kind-dc2 apply -f k8s/database/auth
kubectl --context kind-dc2 apply -f k8s/database/product
kubectl --context kind-dc2 apply -f k8s/database/couchdb
kubectl --context kind-dc2 apply -f k8s/database/redis
kubectl --context kind-dc2 apply -f k8s/auth/
kubectl --context kind-dc2 apply -f k8s/product/
kubectl --context kind-dc2 apply -f k8s/rabbitmq/
kubectl --context kind-dc2 apply -f k8s/workers/
kubectl --context kind-dc2 apply -f k8s/kong/
```

4. Vérifier vos déploiements et tester l’accès
```shell
kubectl --context kind-dc1 get pods
kubectl --context kind-dc1 get svc
kubectl --context kind-dc2 get pods
kubectl --context kind-dc2 get svc

```

5. Tester Kong dans dc1 et dc2 :
* dc1
```shell
curl http://localhost:8000/auth/health
curl http://localhost:8000/product/health/redis
curl http://localhost:8000/status
```

* dc2
```shell
http://localhost:8002 & http://localhost:8003
```

## Debug me
* kong
```shell
kubectl --context kind-dc1 get services kong
```

### Fix me  port-forward sur localhost ❤️
```shell
kubectl port-forward service/kong 8000:8000
```

## 5 nodes 
```shell
kind create cluster --name dc-5-nodes --config k8s/kind-config-dc-5-nodes.yaml
```
* GET NODES
```shell
kubectl --context kind-dc-5-nodes get nodes
```
```shell
kubectl --context kind-dc-5-nodes apply -f k8s/kong/
```

* LOAD les images
```shell
kind load docker-image auth:latest --name dc-5-nodes
kind load docker-image product:latest --name dc-5-nodes
kind load docker-image kong:latest --name dc-5-nodes


kubectl --context kind-dc-5-nodes apply -f k8s/database/auth
kubectl --context kind-dc-5-nodes apply -f k8s/database/product
kubectl --context kind-dc-5-nodes apply -f k8s/database/couchdb
kubectl --context kind-dc-5-nodes apply -f k8s/database/redis
kubectl --context kind-dc-5-nodes apply -f k8s/auth/
kubectl --context kind-dc-5-nodes apply -f k8s/product/
kubectl --context kind-dc-5-nodes apply -f k8s/rabbitmq/
kubectl --context kind-dc-5-nodes apply -f k8s/workers/
kubectl --context kind-dc-5-nodes apply -f k8s/kong/

kubectl --context kind-dc-5-nodes get services
```
* delete it (trop loud)
```shell
kind delete cluster --name dc-5-nodes
kind get clusters
```

## appache
```shell
sudo apachectl stop
```

### les  Migrations et exec
* un coup de get pods deja 
```shell
kubectl --context kind-dc1 get pods
```
* et puis 
```shell
kubectl describe pod <product-pod-name>
kubectl describe pod auth-7fdf8fb949-bfk7f
```
* acces conteneur 
```shell
kubectl exec -it auth-7fdf8fb949-bfk7f -- /bin/bash
```
* un coup de make migration
```shell
php bin/console doctrine:migrations:migrate --no-interaction
```
* fixture 
```shell
 php bin/console doctrine:fixtures:load
```