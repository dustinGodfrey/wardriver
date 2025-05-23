#!/bin/bash
rm ~/.kismet/kismet_httpd.conf
rm -r /tmp/gpsfix
#Stop any instance of gpsd, restart and link to correct socket. Failover included
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sleep 1
sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
pgrep gpsd || echo "â[!] GPSD failed to start!"

echo "[+] Waiting for GPS fix..."

# Wait until GPS reports 3D fix (mode 3)
until gpspipe -w | grep -m1 '"mode":3'; do
    echo "[+] GPS not fixed yet, waiting..."
    sleep 5
done

echo "[+] GPS fix acquired, starting Kismet..."
touch /tmp/gpsfix

# Generate dated log directory
LOGDIR="/home/warpig/wardriving/$(date +%Y-%m-%d)/$(date +%H-%M-%S)"
mkdir -p "$LOGDIR"

# Start Kismet with dynamic log path
sudo airmon-ng start realtek0
exec /usr/local/bin/kismet -c realtek0 --no-nc --log-prefix "$LOGDIR/" 
