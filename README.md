<div align="center">
<h1>Wardriving Rig with Raspberry Pi 4
  &nbsp;
<br><a href="https://wigle.net">
<img border="0" src="https://wigle.net/bi/V_jgKO+KY6mUnLGeWqrXRw.png">
</a>
  </h1>
</div>

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

<h2>Project Walk-Through: Part 1 - Basic Install and Setup</h2>

<h3>~ Flashing the Raspberry Pi SD Card ~</h3>
<p> Start out by downloading the <a href="https://www.raspberrypi.com/software/">Raspberry Pi Imager</a>. Make sure your SD card is loaded and recognized by your computer. Select your device from the dropdown menu. To select operating system, select the Raspberry Pi OS Lite 32-bit by clicking "Raspberry Pi OS (Other). Under the storage dropdown choose your SD card from the list. **MAKE SURE YOU SELECT THE PROPER DISK TO ENSURE YOU DO NOT REFORMAT YOUR MAIN DRIVE** Lastly, agree to adding configurations, add in your home network, and give the pi a host and user name</p>
<p align="center"> <img src="https://i.imgur.com/8WkMQ25.png" height="60%" width="60%" alt="Raspberry Pi Imager"/>
</p>
&nbsp;

<h3>~ Booting and Connecting to the Pi ~</h3>
<p> At this point in the project I was using the ALFA Wireles Adapter: AWUS036NHA and the VFAN GPS Receiver. In the later stages of the build I switched to the other 2 adapters listed above. Initially I was using the first 2 because that is what I had on hand, but due to their longer usb cables I wanted a more streamlined, portable version so I switched to the other devices, which only had a small usb adapter and no cable. This had its pros and cons. The newer devices were in fact more streamline and created a neater build, but they were more underpowered compared to the first two devices so I had to adjust my settings accordingly, adding in delays to wait for them to fully initialize. If a smaller, streamlined build is not a top priority, I would recommend the first two adapters.</p>
<p> Insert the SD card into the pi, connect the WiFi and GPS adapters, then power it on. After the pi fully boots (this might take a while the first time) use the IP address listed in your routers web UI to SSH into the pi using the credentials set during the flashing.<br><code>ssh username@&ip-address</code> </p>
&nbsp;

<h3>~ Updating, Configuring Hardware, and Installing Dependencies ~</h3>
<p> Run Updates<br><code>sudo apt update &amp;&amp; sudo apt upgrade -y</code></p>
<p> Install GPS software<br><code>sudo apt install gpsd gpsd-clients gpsd-tools -y</code></p>
<p>At this point, we will update GPSD to its current version. I wish I had known about this sooner, as I spent days troubleshooting this. The version of GPSD that downloads from the repo is not the current version and will cause issues with Kismet. Without updating GPSD to v3.25 Kismet will not correctly log the GPS coodinates for your drives. My kismet was logging the initial location that the GPS logged for every single network found. If I restarted Kismet, it would then log the rest of those with the new location after the restart. So I would have a list of networks but all with the same GPS location.</p>
<p> To download the latest version, we will need to compile it from source code. Please enter the following commands to update:
<pre><code>
  
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

sudo apt install -y scons \ libncurses-dev python-dev-is-python3 pps-tools git-core asciidoctor \
python3-matplotlib \ build-essential manpages-dev pkg-config python3-distutils

wget http://download.savannah.gnu.org/releases/gpsd/gpsd-3.25.tar.gz
tar -xzf gpsd-3.25.tar.gz
cd gpsd-3.25/

sudo scons
sudo scons udev-install
sudo reboot
</code></pre>
Huge thanks to <a href="https://github.com/kismetwireless/kismet/issues/426">k-rku</a> on GitHub for this find.
<p> List all devices to find your GPS module. If you are having trouble locating it, run the command with the module unplugged and once again with it plugged in, and find the one that appears. Mine is listed as <code>/dev/ttyACM0</code>.<br><code>ls /dev/</code></p>
<p> Run the next series of commands to stop any current use of GPS sockets, disable them from starting on boot, then link your GPS module to that socket:<pre><code>sudo systemctl stop gpsd.socket</code></b><br><code>sudo systemctl disable gpsd.socket</code><br><code>sudo gpsd /dev/name_of_your_device -F /var/run/gpsd.sock</code></pre></p>
<p>To check if the GPS module is running, run either <code>gpsmon</code> or <code>cgps</code> and check if there is any live data. If no data shows up, make sure you are starting the correct GPS module, and make sure you give the module time to fully boot up and connect to satellites. I prefer to use <code>cgps</code> becuause it will give you a neater, more human-readable version of the data, <code>gpsmon</code> will give you mostly raw data which is a little more difficult to parse.</p>
<p>Here is an example of the output from <code>cgps</code>. NOTE: For privacy I have redacted my location, but you should see an active Latitude and Longitude for your current location.</p>
<p align="center"> <img src="https://i.imgur.com/lNopkE2.png" height="60%" width="60%" alt="cgps output"/>
</p>
<p> Install aircrack-ng, a suite of wifi hacking tools. Specifically, we will be using airmon-ng for the setup of this wardriving rig<br><code>sudo apt install aircrack-ng</code></p>
<p> Run the software to list all available wifi cards connected to the pi.<br><code>sudo airmon-ng</code></p>
<p> Look for the Chipset that resembles your band of WiFi adapter. Anything related to "Broadcom" or "brcmdfmac" will be your raspberry pi onboard adapter, please do not use this. You will be disconnected from SSH. Run this command to place your WiFi adapter into monitor mode. Monitor mode allows it to gather data from all available surrounding networks.<br><code>sudo airmon-ng start &lt;interface_name&gt;</code></p>
<p> Run again to check the status of your adapter. If everything worked as it should, your device will not be listed with 'mon' after the interface name such as wlan1mon, or say 'monitor' or "monitor mode' at the end of your chipset name<br><code>sudo airmon-ng</code></p>
<p> Install this list of dependencies needed for Kismet:<pre><code>sudo apt install build-essential git libwebsockets-dev pkg-config \
zlib1g-dev libnl-3-dev libnl-genl-3-dev libcap-dev libpcap-dev \
libnm-dev libdw-dev libsqlite3-dev libprotobuf-dev libprotobuf-c-dev \
protobuf-compiler protobuf-c-compiler libsensors4-dev libusb-1.0-0-dev \
python3 python3-setuptools python3-protobuf python3-requests \
python3-numpy python3-serial python3-usb python3-dev python3-websockets \
librtlsdr0 libubertooth-dev libbtbb-dev libmosquitto-dev</code></pre>
&nbsp;
<h3>~ Downloading, Compiling, and Configuring Kismet ~</h3>
<p>All the guides and walkthroughs that I read while building this project would download Kismet from repos using <code>sudo apt install kismet</code>. Unfortunately, I could never get this to pull down so I resulted to having to download and compile kismet from source code. To download and compile from source, enter the following commands:
<pre><code>git clone https://www.kismetwireless.net/git/kismet.git
cd kismet
./configure
make
sudo make suidinstall
sudo usermod -aG kismet &lt;your_user&gt;
mkdir wardriving
cd wardriving</code></pre>
<p>
Now we need to update the Kismet configuration file located at <code>/usr/local/etc/kismet.conf</code>
  <br><code>sudo nano /usr/local/etc/kismet.conf</code>
  <br>Scroll and look for this line:
  <p align="center"> <img src="https://i.imgur.com/A0VMZPZ.png" height="60%" width="60%" alt="wifi config"/>
</p>
  <p>And change the source to the interface name you are using for your WiFi adapter</p>

<br>Scroll more until you find this line:
  <p align="center"> <img src="https://i.imgur.com/hIe9isz.png" height="60%" width="60%" alt="gps config"/></p>
<p>And change yours to match the one in the image.<br>Save and Exit the configuration file.</p>
<p>Kismet comes with a logging config that you can edit to customize where and how you want your logs handled. This configuration can be located at <code>/usr/local/etc/kismet_logging.conf</code></p>
<p>Here you can enable logging and select which log types you would like kismet to use. Edit the log_prefix section to point where you want your logs saved. Ex: <code>log_prefix=/home/wardriver/kismet_logs/</code>. But make sure that this directory exists before you start kismet for the first time. You will receive errors and it will not log. Kismet will not create this directory for you.</p>
<p align="center"> <img src="https://i.imgur.com/JQk1pM0.png" height="60%" width="60%" alt="logging_enable"/></p>
<p>Here you can customize exactly how kismet will name the log:</p>
<p align="center"> <img src="https://i.imgur.com/6uKAHwu.png" height="60%" width="60%" alt="logging_naming"/></p>
&nbsp;
<h3>~ Starting and Using Kismet ~</h3>
<p>From here you can create a systemd service to start kismet everytime the Pi is booted on. This is the simplest way to launch kismet from the headless system. I created a more custom and complex way to start kismet involving a tactile button and LEDS which I will go over in Part 2.
</p>
<p><code>sudo nano /etc/systemd/system/kismet.service</code></p>
<p>Paste in the configuration file from <a href="https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet.service">kismet.service</a>. Make sure to change the 'user' and 'group' to match your configurations.</p><b>!IMPORTANT! If you plan on stopping with Part 1, you need to change </b><code>ExecStart=/usr/local/bin/kismet-autolog.sh</code> to <code>ExecStart=/usr/local/bin/kismet</code>.<b> The line in the config is for the advanced version in part 2. If you plan on going that far, leave the line as it is</b>
<p align="center"> <img src="https://i.imgur.com/6Eq3Kj8.png" height="60%" width="60%" alt="kismet.service"/></p>
<p>Enable your service to start from boot:</p>
<pre><code>sudo systemctl daemon-reexec
sudo systemctl enable kismet.service</code></pre>
<p>If you are having trouble with your GPS not getting a fix before Kismet fully launches, add a small delay in your Systemd service script under the [Service] heading. Add <code>ExecStartPre=/bin/sleep 15</code> BEFORE the <code>ExecStart</code> line. You can use any number you want, play around with different times to dial in your system. Maybe as little as 5 seconds could be enough for you, maybe you need a little longer.</p>
<h2></h2>
<p>This is a good stopping point for anyone that wants a less complicated setup. It is now fully set up to Wardrive each time the Pi is powered on.</p>
<p>When you are back at your home network, you can power on and ssh into your pi to get the log files. Because Kismet will run on boot, if you do not want to log while transfering files just run <code>sudo systemctl stop kismet.service</code>. Move to the directory where you logs are saved and scp them over to your main computer.</p>
<p><code>scp log_file main_user@main_user_ip:path_on_computer_to_save_logs</code></p>
<p>Kismet will log the following log types:</p>
<p>.wiglecsv - This can be uploaded directly to Wigle.net, or duplicated as .csv to open in Excel. Shows all the good stuff: MAC addresses, SSID, GPS Coordinates, etc.</p>
<p>.kismet - This is a SQL database with more info than the .wiglecsv log. Parsing SQL is out of the scope of this project but if you have experience you can pull a lot of data out of it. Contains a lot of specific data like manufacturer information for the devices logged</p>
<p>.pcapng - A network capture file meant to be opened with Wireshark. Shows information about the communications between wireless devices and your wardriving rig</p>
<br>
<p>For those who want the full final version, complete with tactile button, LEDs, custom startup scripts, and .csv to html mapping, please continue below.</p>
&nbsp;
<h2>Project Walk-Through: Part 2 - Advanced Setup</h2>
<h3>~ Setting up Hotspot Connection ~</h3>
<p> We will start out Part 2 with setting up a connection to the hotspot on your phone. This is not 100% necessary, but if you want to be able to start and stop kismet at your conviencence and use the Kismet Web UI I would suggest it.<p>
<p>I have included the <a href="https://github.com/dustinGodfrey/WardrivingRig/blob/main/default_config.nmconnection">template</a> for this connection, which needs to be placed in <code>/etc/NetworkManager/system-connections/</code>. You will need to edit this config to suit your connection.</p>
<p> Lines to edit are:</p>
<p>
<code>id=</code> - Name your connection, this can be anything.<br>
<code>uuid=</code> - You need to run <code>uuidgen</code> outside of the config to get a unique id. Paste that uuid here.<br>
<code>autoconnect-priority=</code> - Sets the priority for connections. If you set up multiple connections you can use this to ensure you are connecting to the correct one when both are present. The smaller the number the higher the priority.<br>
<code>ssid=</code> - This is the SSID of your hotspot.<br>
<code>hidden=</code> - Is your hotspot a hidden network? Use yes or no. Ex. <code>hidden=yes</code>.<br>
<code>psk=</code> - This is the password for your hotspot connection. You can use plaintext if you like, or for added security run this outside of the config <code>wpa_passphrase "your-ssid" "your-password"</code> and add the psk it generates into the config.
</p>
<p>After editing the connection config, you need to set ownership and permissions then reload NetworkManager:</p>
<pre>sudo chown root:root /etc/NetworkManager/system-connections/yourfile.nmconnection
sudo chmod 600 /etc/NetworkManager/system-connections/yourfile.nmconnection
sudo nmcli connection reload</pre>
<p>When you are connected to the pi over hotspot, go into your hotspot settings to find the IP address of your pi. You will use this for ssh and accessing the Web UI in the next step.</p>
&nbsp;
<h3>~ Kismet Web UI ~</h3>
<p>Kismet comes pre-configured with a Web UI that launches by default on <code>http://localhost:2501</code>. If you are accessing through your phone's browser while connected to the hotspot, the address will be <code>http://pi_ip:2501</code>. Accessing the Web UI the first time will prompt you to create a username and password. This will be stored at <code>~/.kismet/kismet_httpd.conf</code></p>
<p align="center"> <img src="https://i.imgur.com/iARidLG.png" height="75%" width="75%" alt="kismet_webui"/></p>
<p>Kismet waits until it has initialized the WiFI and GPS adapters to launch the Web UI, so if yours does not load keep reloading the page every few seconds until it loads. Monitor the messages at the bottom for any potential errors.</p>
&nbsp;
<h3>~ Controlling Kismet with Tactile Button and LED indicators ~</h3>

<p>At this point in the build I wanted to be able to control the starting and stopping of kismet easier than having to do it over the command line. I decided to write a <a href="https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet.py">python script</a> that runs everytime the pi boots which uses a tactile switch button to start and stop kismet, as well as controls 3 LEDs as status indicators. I used a blue LED to show when the python script was active and would stay illumated the entire time the script was running, a green LED to illuminate when Kismet was running, and a red LED that would illuminate when Kismet was not running. The LEDs were soldered to resistors and were connected to the pi through the GPIO pins, along with the button. The python script runs on boot due to <a href="https://github.com/dustinGodfrey/WardrivingRig/blob/main/war_button.service">war_button.service</a>, a systemd service that waits for the WiFi device to load before starting the python script every time the pi is powered on. I had issues with it not wanting to start the script, hence the reason for the <code>User</code>,<code>Group</code>, and <code>WorkingDirectory</code> lines. <code>WorkingDirectory</code> needs to be the directory that you have the python script in. war_button.service needs to be placed in <code>/etc/systemd/system/</code>.</p>

<p>The python script sets up the LEDs and Button based on their pin location. It initially sets the blue LED to turn on, with the red and green turned off. The scrip then runs a while loop to check for any processes running with the name 'kismet'. If it finds no process, it assumes that kismet is not running and illuminates the red LED. If it finds a process running named 'kismet' the green light will illuminate while the red light will turn off. This is all controlled with the tactile button. During the while loop, the button state is being monitored. If the button is clicked when the red LED is illuminated, a subprocess will run that triggers the <a href="https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet-autolog.sh">autolog script</a>, and if the button is clicked when the green LED is illuminated, a subprocess will run that kills the kismet process that is running.</p>

<p>This was my first time working with LEDs, a tactile button, and getting a python script to control them. I found my success referencing <a href="https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/">this blog post for LED control</a> and <a href="https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/">this blog post for button control</a>. Huge thanks for Soren for these writeups.

<p>The autolog script is a multi-purpose troubleshooting and kismet starting script. During this build I ran into issues with the GPS not getting a full fix, so I added a pause in the system to wait until the GPS was locked on to satellites before continuing to start Kismet. I also wanted a more custom logging prefix and save function so I added that after the GPS fix. Due to issues I ran into later in the build with the underpowered WiFi and GPS adapters, I also have this script doing some of the legwork with fresh GPSD socket functions and starting monitor mode fresh on each start. This is a tad overkill, but I was having intermittent issues that this seemed to fix (like deleting the username and password for the Web UI so it essentially takes no real credentials. I don't recommend this from a security standpoint but it was a quick workaround for an issue I was having. If I remedy this issue I will update this repo). Please edit this file to match your use case, if you don't need as many fallbacks there is no need to have them. You can bypass this script all together by editing <code>kismet.py</code> and changing the subprocess on line 82 from<br><br><code>subprocess.Popen(['/usr/local/bin/kismet-autolog.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)</code><br>to<br><code>subprocess.Popen(['/usr/local/bin/kismet'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)</code></p>

&nbsp;
<h3>~ Parsing Logs, Cleaning Data, and Compiling All Networks to One File ~</h3>
<p>

&nbsp;
<h3>~ Locally Hosting an Interactive Network Map with Python, Pandas, and Folium ~</h3>
<p>

&nbsp;
<h3>~ Wigle.net ~</h3>
<p>

&nbsp;
<h3>~ Afterthoughts and What I Learned ~</h3>
<p>

&nbsp;
<h3>~ Build Photos ~</h3>
<p>
