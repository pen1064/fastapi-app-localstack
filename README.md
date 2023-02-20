# Fastapi App using localstack aws infra and pytest
This is for my own practice
Why localstack?

It can be expensive to perform integration test on AWS platform.

1. Install requirements
```
pip install -r requirements.txt
```

2. Set up the container

```
docker-compose up
```

3. Run any sort of tests
```
make unit-test
make integration-test
```

4. In this simple project, authentication is the first step, first verify the user identity. 

5. The second goal is to go through authorization, to verify they actually have access to the resources. (WIP)

Regardless, Auth0 requires you to create your own private and public keys for the private endpoint

5.1 Clone the openssl directory
```
git clone git://git.openssl.org/openssl.git
```
5.2 Generate private key, create `.private` directory and put the key inside such that it's `.private/jwtRSA256-private.pem`
```
openssl genrsa -out jwtRSA256-private.pem 2048
```
5.3 Extract public key and replace the file `jwtRSA256-public.pem`
```
openssl rsa -in jwtRSA256-private.pem -pubout -outform PEM -out jwtRSA256-public.pem
```
