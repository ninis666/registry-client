# registry-client
Docker registry client

#
# registry server side configuration
#

generate self signed certificate :

1/ Update san.cnf to match hostname in [ alternate_names ] section

2/ Generate private key and ther certificate
   Make sure that commonName will match the hostname added in san.cnf

openssl req -newkey rsa && openssl rsa -in privkey.pem self_signed.key
openssl req -new -x509 -key self_signed.key -sha256 -out self_signed.crt -days 3650 -config san.cnf

3/ Install the key and certificate into registry directory

sudo cp self_signed.key self_signed.crt /etc/docker/registry/cert
sudo chown docker-registry:docker-registry /etc/docker/registry/cert/self_signed.key
sudo chmod 0600 /etc/docker/registry/cert/self_signed.key
sudo chmod 0644 /etc/docker/registry/cert/self_signed.crt

4/ Update docker-registry systemd unit file (/etc/systemd/system/multi-user.target.wants/docker-registry.service) to load certificate/ key

[Service]
User=docker-registry
Environment="REGISTRY_HTTP_TLS_CERTIFICATE=/etc/docker/registry/cert/self_signed.crt"
Environment="REGISTRY_HTTP_TLS_KEY=/etc/docker/registry/cert/self_signed.key"
ExecStart=/usr/bin/docker-registry serve /etc/docker/registry/config.yml

5/ restart docker-registry

sudo systemctl daemon-reload
sudo systemctl restart docker-registry.service

#
# Client side configuration
#

1/ Add the certificate file into certificate directory

sudo cp self_signed.crt /usr/share/ca-certificates/perso/docker-registry.crt

2/ Update certificate cache

sudo dpkg-reconfigure ca-certificates

3/ Enjoy
