# BME_twitter

once algos are developed:

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

help for docker
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```