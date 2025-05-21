<h1>Wardriving Rig with Raspberry Pi 4</h1>


<h2>Project Overview</h2>
<p>This project consists of using a Raspberry Pi 4, WiFi and GPS devices, and Wardriving software to create a fully headless, portable wardriving rig, with the ability after drives to export the data to another system to clean up and create an interactive map that can be locally hosted.</p>
<p>The build started as a final project for my Wireless Networking class for my Cybersecurity degree but scope creep quickly set in and ended up on v3 or v4. I still need to model and print a case, as that will be the final part of the project for now. </p>
<p>This project not only strengthened my knowledge and skills when it comes to programming, configuration, and hardware to software integration, but also from a cybersecurity point of view it opened my eyes to how insecure public networks can be due to lack of knowledge, training, and proper configurations. I found many avoidable mistakes that if remedied, would instantly make a vast difference on personal security and protection. </p>


<h2>Hardware Used</h2>

- <b>[Raspberry Pi 4 - 4GB](https://www.amazon.com/dp/B07VFCB192?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_7&th=1)</b>
- <b>[ALFA Wireles Adapter: AWUS036NHA](https://www.amazon.com/dp/B004Y6MIXS?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)</b>
- <b>[VFAN GPS Receiver](https://www.amazon.com/dp/B073P3Y48Q?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)</b>
- <b>[Tactile Switch Button](https://www.amazon.com/dp/B09R3ZPWJ7?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1&th=1)</b>
- <b>[Green, Red, and Blue LEDs](https://www.amazon.com/BOJACK-Lighting-Electronics-Components-Emitting/dp/B09XDMJ6KY/ref=sr_1_2_sspa?crid=2O8N6N8T9HZ52&dib=eyJ2IjoiMSJ9.RWh0DEjNizcNWw_JCHroKIlvXAt6z3brerKpmlSgKudhjgeyCY_5Z5YVsyV9tbO7jd7F0Wenv1KE9ICa3jPaK0AqbnvKN9tffchD623UBQ84F8uigsCpdxArfeC1vLO5dNwGMRBD4zzKd5PgVclMqw41SE7S8i1MCFvnKyigG_12cklAqvlOu-pFuuLUzJJQasJXSFnL_yqL14D0zyoFWEe4aE-gX97yRQEuIaEXw23uszMPfF1rlQJcV2U-zsGO4qbsxjkT1uWDWIP97aVWsoEzC_OQHgdcToOfLvm3_4g.SURVHyfu_vU6GdV9eIILqXcy8n4ONRVeC69N9OUM72Q&dib_tag=se&keywords=led%2Bkit&qid=1747777837&s=electronics&sprefix=led%2Bki%2Celectronics%2C151&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)</b>
- <b>[ALFA Wireles Adapter: AWUS036ACS](https://www.amazon.com/dp/B004Y6MIXS?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)</b>
- <b>[WWZMDiB GPS Receiver: VK-172](https://www.amazon.com/dp/B0BVBLXVLQ?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)</b>
  

<h2>Software Used </h2>

- <b>Raspberry Pi OS Lite 32-bit</b>
- <b>Kismet</b>
- <b>GPSD</b>
- <b>Aircrack-ng</b>
- <b>Python</b>
- <b>Pandas</b>
- <b>Folium</b>
- <b>systemd</b>

<h2>Project walk-through:</h2>


<p>
<b>~Flashing the Raspberry Pi SD Card~</b> <br/></p>
<p> Start out by downloading the <a href="https://i.imgur.com/8WkMQ25.png">Raspberry Pi Imager</a>. Make sure your SD card is loaded and recognized by your computer. Select your device from the dropdown menu. To select operating system, select the Raspberry Pi OS Lite 32-bit by clicking "Raspberry Pi OS (Other). Under the storage dropdown choose your SD card from the list. **MAKE SURE YOU SELECT THE PROPER DISK TO ENSURE YOU DO NOT REFORMAT YOUR MAIN DRIVE** Lastly, agree to adding configurations, add in your home network, and give the pi a host and user name</p>
<p align="center"> <img src="https://i.imgur.com/8WkMQ25.png" height="60%" width="60%" alt="Raspberry Pi Imager"/>
</p>
&nbsp;
<p>
<b>~Booting and Connecting to the Pi~</b> <br/></p>
<p> Insert the SD card into the pi, connect the WiFi and GPS adapters, then power it on. After the pi fully boots (this might take a while the first time) use the IP address listed in your routers web UI to SSH into the pi using the credentials set during the flashing.<br><code>ssh &lt;username&gt;@&lt;ip-address&gt;</code></b> </p>
&nbsp;
<p>
<b>~Updating, Configuring Hardware, and Installing Dependencies~</b></p>
<p> Run Updates<br><code>sudo apt update &amp;&amp; sudo apt upgrade -y</code></b></p>
<p> Install GPS software<br><code>sudo apt install gpsd gpsd-clients gpsd-tools -y</code></b></p>
<p> List all devices to find your GPS module. If you are having trouble locating it, run the command with the module unplugged then plugged in, and find the one that appears. Mine is listed as <code>/dev/ttyACM0</code>.<br><code>ls /dev/</code></b></p>
<p> Run the next series of commands to stop any current use of GPS sockets, disable them from starting on boot, then link your GPS module to that socket<br><code>sudo systemctl stop gpsd.socket</code></b><br><code>sudo systemctl disable gpsd.socket</code></b><br><code>sudo gpsd /dev/name_of_your_device -F /var/run/gpsd.sock</code></b></p>
<p>To check if the GPS module is running, run either <code>gpsmon</code> or <code>cgps</code> and check if there is any live data. If no data shows up, make sure you are starting the correct GPS module, and make sure you give the module time to fully boot up and connect to satellites</p>
<br>!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</br>
<p> Install aircrack-ng, a suite of wifi hacking tools. Specifically, we will be using airmon-ng for the setup of this wardriving rig<br><code>sudo apt install aircrack-ng</code></b></p>
<p> Run the software to list all available wifi cards connected to the pi.<br><code>sudo airmon-ng</code></b></p>
<p> Look for the Chipset that resembles your band of WiFi adapter. Anything related to "Broadcom" or "brcmdfmac" will be your raspberry pi onboard adapter, please do not use this. You will be disconnected from SSH. Run this command to place your WiFi adapter into monitor mode. Monitor mode allows it to gather data from all available surrounding networks.<br><code>sudo airmon-ng start &lt;interface_name&gt;</code></b></p>
<p> Run again to check the status of your adapter. If everything worked as it should, your device will not be listed with 'mon' after the interface name such as wlan1mon, or say 'monitor' or "monitor mode' at the end of your chipset name<br><code>sudo airmon-ng</code></b></p>
<p> Install this list of dependencies needed for Kismet<br><code>sudo apt install build-essential git libwebsockets-dev pkg-config \
zlib1g-dev libnl-3-dev libnl-genl-3-dev libcap-dev libpcap-dev \
libnm-dev libdw-dev libsqlite3-dev libprotobuf-dev libprotobuf-c-dev \
protobuf-compiler protobuf-c-compiler libsensors4-dev libusb-1.0-0-dev \
python3 python3-setuptools python3-protobuf python3-requests \
python3-numpy python3-serial python3-usb python3-dev python3-websockets \
librtlsdr0 libubertooth-dev libbtbb-dev libmosquitto-dev</code></b></p>
&nbsp;
<p>
<b>~Downloading, Compiling, and Configuring Kismet~</b></p>


<p> Start<br><code></code></b></p>
