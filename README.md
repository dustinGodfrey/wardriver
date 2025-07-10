<div align="center">
<h1>Wardriving Rig with Raspberry Pi 4
  &nbsp;
<br><a href="https://wigle.net">
<img border="0" src="https://wigle.net/bi/V_jgKO+KY6mUnLGeWqrXRw.png">
</a>
  </h1>
</div>

## Project Overview
This project consists of using a Raspberry Pi 4, WiFi and GPS devices, and Wardriving software to create a fully headless, portable wardriving rig, with the ability after drives to export the data to another system to clean up and create an interactive map that can be locally hosted.

The build started as a final project for my Wireless Networking class for my cybersecurity degree but scope creep quickly set in, with the project ending on v3 or v4. I still need to model and print a case, as that will be the final part of the project for now.

This project not only strengthened my knowledge and skills when it comes to programming, configuration, and hardware-to-software integration, but also from a cybersecurity point of view it opened my eyes to how insecure public networks can be due to lack of knowledge, training, and proper configurations. I found many avoidable mistakes that if remedied, would instantly make a vast difference on personal security and protection.

## Hardware Used
- [Raspberry Pi 4 - 4GB](https://www.amazon.com/dp/B07VFCB192?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_7&th=1)
- [ALFA Wireless Adapter: AWUS036NHA](https://www.amazon.com/dp/B004Y6MIXS?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)
- [VFAN GPS Receiver](https://www.amazon.com/dp/B073P3Y48Q?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)
- [Tactile Switch Button](https://www.amazon.com/dp/B09R3ZPWJ7?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1&th=1)
- [Green, Red, and Blue LEDs](https://www.amazon.com/BOJACK-Lighting-Electronics-Components-Emitting/dp/B09XDMJ6KY/ref=sr_1_2_sspa?crid=2O8N6N8T9HZ52&dib=eyJ2IjoiMSJ9.RWh0DEjNizcNWw_JCHroKIlvXAt6z3brerKpmlSgKudhjgeyCY_5Z5YVsyV9tbO7jd7F0Wenv1KE9ICa3jPaK0AqbnvKN9tffchD623UBQ84F8uigsCpdxArfeC1vLO5dNwGMRBD4zzKd5PgVclMqw41SE7S8i1MCFvnKyigG_12cklAqvlOu-pFuuLUzJJQasJXSFnL_yqL14D0zyoFWEe4aE-gX97yRQEuIaEXw23uszMPfF1rlQJcV2U-zsGO4qbsxjkT1uWDWIP97aVWsoEzC_OQHgdcToOfLvm3_4g.SURVHyfu_vU6GdV9eIILqXcy8n4ONRVeC69N9OUM72Q&dib_tag=se&keywords=led%2Bkit&qid=1747777837&s=electronics&sprefix=led%2Bki%2Celectronics%2C151&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)
- [ALFA Wireless Adapter: AWUS036ACS](https://www.amazon.com/dp/B004Y6MIXS?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2)
- [WWZMDiB GPS Receiver: VK-172](https://www.amazon.com/dp/B0BVBLXVLQ?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)

## Software Used
- Raspberry Pi OS Lite 32-bit
- Kismet
- GPSD
- Aircrack-ng
- Python
- Pandas
- Folium
- systemd

## Project Walk-Through: Part 1 - Basic Install and Setup
Start out by downloading the [Raspberry Pi Imager](https://www.Raspberrypi.com/software/) Make sure your SD card is loaded and recognized by your computer. Select your device from the dropdown menu. To select operating system, select the Raspberry Pi OS Lite 32-bit by clicking "Raspberry Pi OS (Other). Under the storage dropdown choose your SD card from the list.  Lastly, agree to adding configurations, add in your home network, and give the Pi a host and user name.
> **MAKE SURE YOU SELECT THE PROPER DISK TO ENSURE YOU DO NOT REFORMAT YOUR MAIN DRIVE**

<p align="center"> <img src="https://i.imgur.com/8WkMQ25.png" width="60%" alt="Raspberry Pi Imager"/> </p>

&nbsp;
### ~ Booting and Connecting to the Pi ~
At this point in the project I was using the ALFA Wireless Adapter: AWUS036NHA and the VFAN GPS Receiver. In the later stages of the build I switched to the other 2 adapters listed above. Initially I was using the first 2 because that is what I had on hand, but due to their longer usb cables I wanted a more streamlined, portable version so I switched to the other devices, which only had a small usb adapter and no cable. This had its pros and cons. The newer devices were, in fact, more streamlined and created a neater build, but they were underpowered compared to the first two devices so I had to adjust my settings accordingly, adding in delays to wait for them to fully initialize. If a smaller, streamlined build is not a top priority, I would recommend the first two adapters.

Insert the SD card into the pi, connect the WiFi and GPS adapters, then power it on. After the Pi fully boots (this might take a while the first time) use the IP address listed in your routers web UI to SSH into the Pi using the credentials set during the flashing.
```bash
ssh username@ip_address
```

&nbsp;

### ~ Updating, Configuring Hardware, and Installing Dependencies ~
Run Updates
```bash
sudo apt update
sudo apt upgrade -y
```

Install GPS software
```bash
sudo apt instll gpsd gpsd-clients gpsd-tools -y
```

At this point, we will update GPSD to its current version. I wish I had known about this sooner, as I spent days troubleshooting this. The version of GPSD that downloads from the repo is not the current version and will cause issues with Kismet. Without updating GPSD to v3.25 Kismet will not correctly log the GPS coordinates for your drives. My kismet was logging the initial location that the GPS logged for every single network found. If I restarted Kismet, it would then log the rest of those with the new location after the restart. So I would have a list of networks but all with the same GPS location.

To download the latest version, we will need to compile it from source code. Please enter the following commands to update:

```bash
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
```

Huge thanks to [k-rku](https://github.com/kismetwireless/kismet/issues/426) on GitHub for this find!


List all devices to find your GPS module. If you are having trouble locating it, run the command with the module unplugged and once again with it plugged in, and find the one that appears. Mine is listed as `/dev/ttyACM0`
```bash
ls /dev/
```

Run the next series of commands to stop any current use of GPS sockets, disable them from starting on boot, then link your GPS module to that socket:
```bash
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/name_of_your_device -F /var/run/gpsd.sock
```
To check is the GPS module is running, run either ```gpsmon``` or ```cgps``` and check if there is any live data. If no data shows up, make sure you are starting the correct GPS module, and make sure you give the module time to fully boot up and connect to satellites. I prefer to use ```cgps``` because it will give you a neater, more human-readable version of the data, ```gpsmon``` will give you mostly raw data which is a little more difficult to parse.

Here is an example of the output from ```cgps```

**For privacy I have redacted my location, but you should see an active Latitude and Logitude for your current location**

<p align="center"> <img src="https://i.imgur.com/lNopkE2.png" width="60%" alt="cgps output"/>
</p>

Install ```aircrack-ng```, a suite of WiFi hacking tools. Specifically, we will be using airmon-ng for the setup of this wardriving rig 

```bash
sudo apt install aircrack-ng
```

Run the software to list all available WiFi cards connected to the pi.

```bash
sudo airmon-ng
```

Look for the Chipset that resembles your band of WiFi adapter. Anything related to "Broadcom" or "brcmdfmac" will be your Raspberry Pi onboard adapter, please do not use this. You will be disconnected from SSH. Run this command to place your WiFi adapter into monitor mode. Monitor mode allows it to gather data from all available surrounding networks.

```bash
sudo airmon-ng start <interface_name>
```

Run again to check the status of your adapter. If everything worked as it should, your device will not be listed with 'mon' after the interface name such as wlan1mon, or say 'monitor' or "monitor mode' at the end of your chipset name
```bash
sudo airmon-ng
```

Install this list of dependencies needed for Kismet:
```bash
sudo apt install build-essential git libwebsockets-dev pkg-config \
zlib1g-dev libnl-3-dev libnl-genl-3-dev libcap-dev libpcap-dev \
libnm-dev libdw-dev libsqlite3-dev libprotobuf-dev libprotobuf-c-dev \
protobuf-compiler protobuf-c-compiler libsensors4-dev libusb-1.0-0-dev \
python3 python3-setuptools python3-protobuf python3-requests \
python3-numpy python3-serial python3-usb python3-dev python3-websockets \
librtlsdr0 libubertooth-dev libbtbb-dev libmosquitto-dev
```

&nbsp;

### ~ Downloading, Compiling, and Configuring Kismet ~

All the guides and walkthroughs that I read while building this project would download Kismet from repos using `sudo apt install kismet`. Unfortunately, I could never get this to pull down so I resulted to having to download and compile kismet from source code. To download and compile from source, enter the following commands:

```bash
git clone https://www.kismetwireless.net/git/kismet.git
cd kismet
./configure
make
sudo make suidinstall
sudo usermod -aG kismet <your_user>
mkdir wardriving
cd wardriving
```

Now we need to update the Kismet configuration file located at `/usr/local/etc/kismet.conf`

<p align="center"> <img src="https://i.imgur.com/JQk1pM0.png" width="60%" alt="logging_enable"/></p>

Here you can customize exactly how kismet will name the log:
<p align="center"> <img src="https://i.imgur.com/6uKAHwu.png" width="60%" alt="logging_naming"/></p>


&nbsp;

### ~ Starting and Using Kismet ~

From here you can create a systemd service to start kismet every time the Pi is booted on. This is the simplest way to launch kismet from the headless system. I created a more custom and complex way to start kismet involving a tactile button and LEDs, which I will go over in Part 2.

```bash
sudo nano /etc/systemd/system/kismet.service
```

Paste in the configuration file from [kismet.service](https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet.service). Make sure to change the `user` and `group` to match your configurations.

>**IMPORTANT! If you plan on stopping with Part 1, you need to change
>`ExecStart=/usr/local/bin/kismet-autolog.sh`
>
> to
>
>`ExecStart=/usr/local/bin/kismet`
>
> The line is the config is for the advanced version if Part 2. If you plan on going that far leave the line as it is. 

<p align="center"> <img src="https://i.imgur.com/6Eq3Kj8.png" width="60%" alt="kismet.service"/></p>

Enable your service to start from boot:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable kismet.service
```

If you are having trouble with your GPS not getting a fix before Kismet fully launches, add a small delay in your Systemd service script under the [Service] heading. Add `ExecStartPre=/bin/sleep 15` BEFORE the `ExecStart` line. You can use any number you want, play around with different times to dial in your system. Maybe as little as 5 seconds could be enough for you, maybe you need a little longer.

##

This is a good stopping point for anyone that wants a less complicated setup. It is now fully set up to Wardrive each time the Pi is powered on.

When you are back at your home network, you can power on and SSH into your Pi to get the log files. Because Kismet will run on boot, if you do not want to log while transferring files just run `sudo systemctl stop kismet.service`. Move to the directory where your logs are saved and scp them over to your main computer.

```bash
scp log_file main_user@main_user_ip:path_on_computer_to_save_logs
```
>The scp syntax is: scp source destination

Kismet will log the following log types:

>.wiglecsv - This can be uploaded directly to Wigle.net, or duplicated as .csv to open in Excel. Shows all the good stuff: MAC addresses, SSID, GPS Coordinates, etc.
>
>.kismet - This is a SQL database with more info than the .wiglecsv log. Parsing SQL is out of the scope of this project but if you have experience you can pull a lot of data out of it. Contains a lot of specific data like manufacturer information for the devices logged
>
>.pcapng - A network capture file meant to be opened with Wireshark. Shows information about the communications between wireless devices and your wardriving rig
>
>.kml - Keyhole Markup Language. Meant to be opened in Google Earth, showing GPS coordinates of each data entry. NOTE: Extremely slow and buggy with a lot of data. The reason I created the Folium map later in the build.

For those who want the full final version, complete with tactile button, LEDs, custom startup scripts, and .csv to html mapping, please continue below.

&nbsp;

## Project Walk-Through: Part 2 - Advanced Setup

### ~ Setting up Hotspot Connection ~

We will start out Part 2 with setting up a connection to the hotspot on your phone. This is not 100% necessary, but if you want to be able to start and stop kismet at your convenience and use the Kismet Web UI I would suggest it.

I have included the [template](https://github.com/dustinGodfrey/WardrivingRig/blob/main/default_config.nmconnection) for this connection, which needs to be placed in `/etc/NetworkManager/system-connections`. You will need to edit this config to suit your personal connection.

Lines to edit are:

>id=  Name your connection, this can be anything.

>uuid=  You need to run uuidgen outside of the config to get a unique id. Paste that uuid here.

>autoconnect-priority=  Sets the priority for connections. If you set up multiple connections you can use this to ensure you are connecting to the correct one when both are present. The smaller the number the higher the priority.

>ssid=  This is the SSID of your hotspot.

>hidden=  Is your hotspot a hidden network? Use yes or no. Ex. hidden=yes.

>PSK=  This is the password for your hotspot connection. You can use plaintext if you like, or for added security run this outside of the config wpa_passphrase "your-ssid" "your-password" and add the PSK it generates into the config.

After editing the connection config, you need to set ownership and permissions then reload NetworkManager:

```bash
sudo chown root:root /etc/NetworkManager/system-connections/yourfile.nmconnection
sudo chmod 600 /etc/NetworkManager/system-connections/yourfile.nmconnection
sudo nmcli connection reload
```

When you are connected to the Pi over hotspot, go into your hotspot settings to find the IP address of your pi. You will use this for SSH and accessing the Web UI in the next step.

&nbsp;

### ~ Kismet Web UI ~

Kismet comes pre-configured with a Web UI that launches by default on `http://localhost:2501`. If you are accessing through your phone's browser while connected to the hotspot, the address will be `http://pi_ip:2501`. Accessing the Web UI the first time will prompt you to create a username and password. This will be stored at `~/.kismet/kismet_httpd.conf`

<p align="center"> <img src="https://i.imgur.com/iARidLG.png" width="75%" alt="kismet_webui"/></p>

Kismet waits until it has initialized the WiFi and GPS adapters to launch the Web UI, so if yours does not load keep reloading the page every few seconds until it loads. Monitor the messages at the bottom for any potential errors.

&nbsp;

### ~ Controlling Kismet with Tactile Button and LED Indicators ~

At this point in the build I wanted to be able to control the starting and stopping of kismet easier than having to do it over the command line. I decided to write a [python script](https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet.py) that runs every time the Pi boots which uses a tactile switch button to start and stop kismet, as well as controls 3 LEDs as status indicators. I used a blue LED to show when the python script was active and would stay illuminated the entire time the script was running, a green LED to illuminate when Kismet was running, and a red LED that would illuminate when Kismet was not running. The LEDs were soldered to resistors and were connected to the Pi through the GPIO pins, along with the button. The python script runs on boot due to [war_button.service](https://github.com/dustinGodfrey/WardrivingRig/blob/main/war_button.service), a systemd service that waits for the WiFi device to load before starting the python script every time the Pi is powered on. I had issues with it not wanting to start the script, hence the reason for the `User`,`Group`, and `WorkingDirectory` lines. `WorkingDirectory` needs to be the directory that you have the python script in. war_button.service needs to be placed in `/etc/systemd/system/`.

<p align="center"> <img src="https://i.imgur.com/fApoKgn.jpeg" width="75%" alt="LEDs"/></p>

The python script sets up the LEDs and Button based on their pin location. It initially sets the blue LED to turn on, with the red and green turned off. The script then runs a while loop to check for any processes running with the name 'kismet'. If it finds no process, it assumes that kismet is not running and illuminates the red LED. If it finds a process running named 'kismet' the green light will illuminate while the red light will turn off. This is all controlled with the tactile button. During the while loop, the button state is being monitored. If the button is clicked when the red LED is illuminated, a subprocess will run that triggers the [autolog script](https://github.com/dustinGodfrey/WardrivingRig/blob/main/kismet-autolog.sh), and if the button is clicked when the green LED is illuminated, a subprocess will run that kills the kismet process that is running.

This was my first time working with LEDs, a tactile button, and getting a python script to control them. I found my success referencing [this blog post for LED control](https://Raspberrypihq.com/making-a-led-blink-using-the-Raspberry-pi-and-python/) and [this blog post for button control](https://Raspberrypihq.com/use-a-push-button-with-Raspberry-pi-gpio/). Huge thanks for Soren for these writeups.

The autolog script is a multi-purpose troubleshooting and kismet starting script. During this build I ran into issues with the GPS not getting a full fix, so I added a pause in the system to wait until the GPS was locked on to satellites before continuing to start Kismet. I also wanted a more custom logging prefix and save function so I added that after the GPS fix. Due to issues I ran into later in the build with the underpowered WiFi and GPS adapters, I also have this script doing some of the legwork with fresh GPSD socket functions and starting monitor mode fresh on each start. This is a tad overkill, but I was having intermittent issues that this seemed to fix (like deleting the username and password for the Web UI so it essentially takes no real credentials. I don't recommend this from a security standpoint but it was a quick workaround for an issue I was having. If I remedy this issue I will update this repo). Please edit this file to match your use case, if you don't need as many fallbacks there is no need to have them. You can bypass this script all together by editing kismet.py and changing the subprocess on line 82 from

>subprocess.Popen(['/usr/local/bin/kismet-autolog.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
>
>to
>
>subprocess.Popen(['/usr/local/bin/kismet'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

&nbsp;

## WiFi Network Data Parsing & Mapping

### ~ Parsing and Compiling Network Data ~

My goal was to have one .csv file that would hold all of the networks from every drive that I made. Due to the .wiglecsv file that comes from Kismet having many blank SSID (due to APs with no name) and duplicate MAC (Kismet would sometimes log the same AP multiple times if it read the signal from more than one location) I decided to filter each .csv before adding it to a master list, `total_war.csv`, so that I would have one list with every network listed only one time and have one master file to create an interactive map with in the later steps.

Below is the list of steps taken to convert the .wiglecsv into a cleaned up master list. This is to be performed on every `.wiglecsv` file from the drives

1. Duplicate or make a copy of the `.wiglecsv` file
2. Change the file extension of the copy to `.csv`
3. Open the .csv file in Excel
4. Select the 'Data' tab, then click 'Filter'. Arrows shoud appear next to each label.
5. Click the arrow next to 'SSID' and scroll to the bottom of the list. Uncheck '(Blanks)'. Exit current window.
6. While still under the 'Data' tab, find 'Remove Duplicates'. Once inside, uncheck 'Select All' and only check 'MAC'. Press OK to confirm.
7. Click the first MAC address (usually line 3), then Ctrl + Shift + Right to select whole row, then Ctrl + Shift + Down to select all available data.
8. Create a new Excel spreadsheet named total_war.csv and paste in the data on the first available blank line. 
9. For every new block of entries added to `total_war.csv`, repeat steps 4 - 7 above to remove any duplicates from one drive to the other.

Now there is one file with all of the data from your drives on it. I know that this takes away some of the real devices (APs with no SSID) but for the sake of this project I just wanted real SSID that I could look through. This was for a school assignment like mentioned, so part of my presentation was to pick out my favorite SSID, so this was a way for me to filter and look for just valid names. This is optional depending on how you would want the data on the map. I found that the extra data on the map made it difficult to find real SSIDs.

&nbsp;


### ~ Locally Hosting an Interactive Network Map with Python, Pandas, and Folium ~

I wrote a [python script](https://github.com/dustinGodfrey/WardrivingRig/blob/main/csv_to_html.py) that will take the `total_war.csv` file and convert the data to an interactive map that you can host locally and access from the browser. Make sure that `total_war.csv` and `csv_to_html.py` are in the same directory, or add the full path for the .csv in the python code. If they are in the same directory, there is no need to edit the python script.

The script will open `total_war.csv` with Pandas to be able to accurately parse the .csv file. The script then initiates Folium to create a map and sets the starting location to an average of the Longitude and Latitude of all the locations in the file, as well as how far to set the zoom of the map. The script then creates an empty list, which validated networks will be put into, leaving out any that contain escape characters or fall outside of the scope of normal ASCII. (This just creates a cleaner view of the networks). We create a label that each network will have on the map, containing SSID, MAC, AuthMode, and the Current Longitude and Latitude. The script then saves the map to `total_war.html`.

>Note: This needs to be done each time `total_war.csv` is updated so your map can accurately represent your data.

After you have successfully converted your data to the Folium map, run `python3 -m http.server 8000` from the directory that `csv_to_html.py` resides. Navigate in your browser to `http://localhost:8000` and choose your `csv_to_html.py` file if needed. This will open up the interactive map for you to move around and locate networks. Clicking on each marker will bring up the info we set in the python script

&nbsp;

### ~ Wigle.net ~

[Wigle.net](https://wigle.net) is a gamified way to store all of your drives from Kismet in a central location with other users who want to upload their drives as well. This creates a huge ecosystem, filled with over 21 billion WiFi observations and over 83,000 users. After each successful upload, your data is added to the central repository and you are given a score based on the amount of networks you have discovered. You can compare your stats to other users and use their built in map to see how you stack against them. Kismet will automatically log `wiglecsv` which we duplicated and converted above to use with the Folium maps. This file is designed to be uploaded directly to Wigle.net without any manipulation to the data whatsoever.

Spending time on Wigle.net you will notice that it accepts networks in the form of WiFi, Bluetooth, and Cell Towers. Kismet itself will only log the WiFi connections, but if you build your own wardriving rig with ESP-32s or use the official Wigle.net Android app, you can successfully log WiFi, Bluetooth, and Cell Tower connections. The Wigle Android app gives you the ability to upload your drives straight from your phone.

<p align="center"> <img src="https://i.imgur.com/hPpu2mU.png" width="75%" alt="wigle1"/></p>
<p align="center"> <img src="https://i.imgur.com/dmZC7xH.png" width="75%" alt="wigle2"/></p>


&nbsp;

## Project Recap

### ~ Afterthoughts and What I Learned ~

I learned a lot from this project, both on a technical level and a social level. Technically, I learned and expanded my knowledge on a number of different tasks such as hardware-to-software integration, controlling hardware with python, creating efficient systemd services, and parsing data into useful information.

Socially, this is where the project took a turn and I became very concerned with the way the public uses and secures their networks. Due to my degree, I was trying to view this project through the lens of cybersecurity, so my initial goal was to sniff out the vulnerabilities associated with setting up wireless networks. Initially, I hypothesized that there would be many unsecure network protocols, such as WEP. What I found was primarily WPA2/3 networks, along with open networks for restaurants and businesses, but the most shocking thing was a huge percentage of the "secure" WPA2/3 networks were using default credentials set by the manufacturer.

16% of the networks that I found were using default credentials set by the manufacturer. This list included names like "Ring Setup", "Linksys", "Netgear", and "CenturyLink". It is quite easy to research online the default credentials that these companies use, or at the very least the naming convention they use if the credentials are randomized. This is opening yourself up to a very easy hack, giving the threat actor more than enough information to close in the scope of their attack.

In addition to default credentials, I found numerous networks that were using family names or email addresses as their SSID, such as "Wilson Family WiFi" or "janedoe76@gmail.com". This takes social engineering completely out of the equation, as there is no guesswork to who lives in that house anymore. Using an email is extremely unsecure, as the possibility of these addresses being correctly matched to data dumps is extremely high. It can easily be assumed that people who are using the default credentials, family names, or email addresses are not very tech savvy, leaving themselves as a very easy and vulnerable target.

<p align="center"> <img src="https://i.imgur.com/mQuqa7x.png" width="75%" alt="pie_chart"/></p>

&nbsp;
<h3>~ Build Photos ~</h3>
<p align="center"> <img src="https://i.imgur.com/T6S4byP.jpeg" width="75%" alt="image1"/></p>
<p align="center"> <img src="https://i.imgur.com/893Z0KK.jpeg" width="75%" alt="image2"/></p>
<p align="center"> <img src="https://i.imgur.com/r67DIve.jpeg" width="75%" alt="image3"/></p>
<p align="center"> <img src="https://i.imgur.com/BubwhB3.jpeg" width="75%" alt="image4"/></p>
<p align="center"> <img src="https://i.imgur.com/MLVe1FQ.jpeg" width="75%" alt="image5"/></p>
<p align="center"> <img src="https://i.imgur.com/YixkNqc.jpeg" width="75%" alt="image6"/></p>
<p align="center"> <img src="https://i.imgur.com/bOY9GHr.jpeg" width="75%" alt="image7"/></p>
<p align="center"> <img src="https://i.imgur.com/fApoKgn.jpeg" width="75%" alt="image8"/></p>
<p align="center"> <img src="https://i.imgur.com/3qHKyOz.jpeg" width="75%" alt="image10"/></p>
<p align="center"> <img src="https://i.imgur.com/qarIzor.jpeg" width="75%" alt="image9"/></p>
<p align="center"> <img src="https://i.imgur.com/GOPqOXW.jpeg" width="75%" alt="image11"/></p>
<p align="center"> <img src="https://i.imgur.com/FjGlYeR.jpeg" width="75%" alt="image12"/></p>
<p align="center"> <img src="https://i.imgur.com/T5Ta86Z.jpeg" width="75%" alt="image13"/></p>
