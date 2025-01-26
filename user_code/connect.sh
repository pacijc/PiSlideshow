to_add="/Users/joepaci/Downloads/Mosaic_Template"
active="Mosaic_Template"
base="~/PiSlideshow"
set_active_line="rm -r $base/active_slideshow; cp -r $base/stored_slideshows/$active $base/active_slideshow;"

#send a file to the pi, then reboot
scp -r $to_add user@10.0.0.153:PiSlideshow/stored_slideshows/

ssh user@10.0.0.153 "$set_active_line"