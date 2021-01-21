# PiCamera Docker

A dockerized python raspberry pi camera server with basic security in mind

## Features
- Multiple clients can visit the stream
- The camera auto stops if no one is viewing (5 sec)
- Http basic auth
- Nginx Reverse Proxy to handle SSL
- SSL Only

### Tested on
- Raspberry Pi 4, Raspberry Pi OS 32bit, Docker-CE
- Linux pi2 5.4.83-v7l+ #1379 SMP Mon Dec 14 13:11:54 GMT 2020 armv7l GNU/Linux

#### Project Valid Lifetime
roughly 2 months from last commit before it stops working, and needs some updating

## Getting Started

#### Prerequisites
- Raspberry Pi OS 32bit (or 64 if the camera works on it)
- `raspistill -o test.jpg` works
- Docker installed
- Docker compose installed
- Stable local internet connection

#### SSL Certificate
To generate a self signed certificate, go look for updated openssl self signed certificate guides with `subject alternate name` support

I'm up late, so won't be including it here :P

After you have the certificate

Put the Certificate in

`/nginx/certs/camera.home.crt`

Put the Certificate Key in

`/nginx/certs/camera.home.key`

#### Auth Password
create a `/.env` file in the same directory as `docker-compose.yml` (the root of this project) 

Fill out `.env` with the below
```
PICAMERA_USER=admin
PICAMERA_PASSWORD=whatever you want # default is admin
```

#### Deploy

To start the application, run
`docker-compose up -d --build`

### Changing Domain

Default domain is `https://camera.home`
to change domain, modify the config file in `/nginx/camera.home.conf`

You can also visit the site via ip `https://X.X.X.X`

