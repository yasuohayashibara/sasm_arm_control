# sasm_arm_control

### Requirement
kondo_driver  
https://github.com/citbrains/kondo_driver

### KondoのRS486アダプタを認識させるための処理

以下のファイルを　/etc/udev/rules.d　に保存，再起動

ファイル名：80-kondo-ics.rules

```
# set permission to all Kondo device
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="165c", MODE="0666"
KERNEL=="ttyUSB*", MODE="0666", ATTRS{product}=="RS485 USB/Serial Converter", ATTRS{serial}=="KOUSB485" SYMLINK+="ttyUSBKondo"
```

以下に従い，/etc/modulesと/etc/rc.localを変更  
参考にしたサイト  
https://hirooka.pro/?p=6577

/etc/modules

```
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.
# Parameters can be specified after the module name.
 
lp
rtc
ftdi_sio
 
#
```

/etc/rc.local

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
 
modprobe ftdi-sio
echo "165C 0009" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
 
exit 0
```
