First, start your kubectl

```
cd k8s
kubectl apply -f fastapi-deployment.yaml
kubectl apply -f fastapi-service.yaml
kubectl apply -f fastapi-ingress.yaml
```

If no public address is given, you can use the command to test it locally:

```
curl --resolve demo.localdev.me:8080:127.0.0.1 http://demo.localdev.me:8080/heartbeat
```

It should return:

```
{"message": "Hello World"}
```