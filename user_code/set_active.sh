#!/bin/bash
#get file to add from cmdline
filepath=$2
filename=$(basename "$filepath")
#shortcut
base="~/PiSlideshow"

#operations to format the slideshow
remove_old="rm -r $base/active_slideshow;"
make_active="cp -r $base/stored_slideshows/$filename $base/active_slideshow;"

if [ $1 -eq '1' ]; then
    #send a file to the pi
    scp -r $filepath user@10.0.0.153:PiSlideshow/stored_slideshows/
fi

#use ssh to format new slideshow then reboot
ssh user@10.0.0.153 "$remove_old $make_active sudo reboot"