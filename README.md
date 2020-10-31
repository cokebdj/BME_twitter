# BME_twitter

Este repositorio contiene los recursos necesarios para desarrollar la primera parte de la práctica de cloud del máster de BME.

Para generar las capas necesarias que subir a AWS se debe ejecutar:

```
chmod +x get_layer_packages.sh 
sudo ./get_layer_packages.sh 
zip -r blockchain.zip python
aws lambda publish-layer-version --layer-name blockchain --zip-file fileb://blockchain.zip --region us-east-2 --compatible-runtimes python3.7 
```

```
chmod +x get_layer_packages.sh 
sudo ./get_layer_packages.sh 
zip -r twitter.zip python
aws lambda publish-layer-version --layer-name twitter --zip-file fileb://twitter.zip --region us-east-2 --compatible-runtimes python3.7 
```

https://blog.alloy.co/deploying-aws-lambda-layers-with-pandas-for-data-science-38fe37a44a81

Para limpiar los contenedores de Docker:
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```
