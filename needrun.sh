#!/bin/sh
source /etc/profile
source /home/nemo/.bash_profile
source /home/nemo/.bashrc

if [ -e "urllist.txt" ]; then
  new=$(md5sum urllist.txt | awk '{print $1}')
  old=$(cat md5.txt | awk '{print $1}')
  if [ $new == $old ]; then
    echo $old "no changed"
  else
    if [ `ps ux | grep "python difimage.py" | grep "grep" -vc` -eq 0 ]; then
      python difimage.py >> diff.log &
      echo $new >md5.txt
    fi
  fi
fi
