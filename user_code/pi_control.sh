#!/bin/bash

action=$(whiptail --title "test" --inputbox "Would you like to:\n[1]\tAdd a new slideshow\n[2]\tUse an existing one\nEnter choice here: " 10 60 "" 3>&1 1>&2 2>&3)
echo "Hello, $action!"