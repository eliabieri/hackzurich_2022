raspi setup

1. enable pi camera in ``` raspi-config ```
2. ``` sudo apt-get upgrade ```
3. ``` sudo apt-get update ```
4. install vlc ``` sudo apt-get install vlc ```
5. start stream

    ``` /opt/vc/bin/raspivid -o - -t 0 -w 1280 -h 720 -fps 25 -b 1500000 -rot 180 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264 ```
    
6. stream available at --> ``` http://{IP}:8090 ```

