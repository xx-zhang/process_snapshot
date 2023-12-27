# instal lsplunk 

```bash

docker run -itd -p 8000:8000 --restart=always --name=sp \
    -e "SPLUNK_PASSWORD=string123." \
    e "SPLUNK_START_ARGS=--accept-license" \
    -it --name so1 splunk/splunk:8.2.12

```

## dvt server 
```


```

## docker-compose 

```yaml


version: "2"

services:
   splunk
      container_name: so1
      restart: always
      image: 'splunk/splunk:8.2.12'
      ports:
        - 8000:8000
        - 8088:8088
        - 10514 :10514
      environment:
        - MYSQL_USER=admin007
      depends_on:
        - dvt 
      volumes:
        - /etc/localtime:/etc/localtime:ro
        - /splunk_data:/opt/splunk/var/lib/splunk
      networks:
        customize_net:
          ipv4_address: 192.168.77.20

   dvt:
      container_name: dvt
      image: 'actanble/dvt-splunk'
      restart: always
      ports:
        - "7777:7777"
      networks:
        customize_net:
          ipv4_address: 192.168.77.77

networks:
  customize_net:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 192.168.77.0/24


```

## splunk systemd unit

1. `splunk.service`

```
[Unit]
Description=Splunk
Requires=splunk-license.service
After=syslog.target network.target splunk-license.service

[Service]
Type=forking
ExecStart=/opt/splunk/splunk/bin/splunk start
ExecStop=/opt/splunk/splunk/bin/splunk stop
Restart=always

[Install]
WantedBy=multi-user.target
```

2. `splunk-license.service`

```
[Unit]
Description=Splunk licence server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/splunk/
ExecStart=/opt/splunk/dvt-splunk_licsrv.1.0.linux.amd64
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Tags:
```
#splunk #systemd 
```