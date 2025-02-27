# 1. Installer Kind si ce n'est pas déjà fait
```shell
brew install kind

```

# 2. Créer le cluster Kind
```shell
kind create cluster --config kind-config.yaml

```

# 3. Construire vos images Docker localement
```shell
docker build -t auth-image ../auth/
docker build -t product-image ../product/
docker build -t workers-image ../workers/
```


# 4. Charger les images dans Kind
```shell
kind load docker-image auth-image
kind load docker-image product-image
kind load docker-image workers-image
```


# 5. Appliquer les manifests
```shell
kubectl apply -f namespace.yaml
kubectl apply -f postgres-auth.yaml
kubectl apply -f auth.yaml
kubectl apply -f redis.yaml
kubectl apply -f kong.yaml
```
