#!/usr/bin/env bash
# This script check ethN is working
# no news is good news, or say nolink devs

no_link=''

function _say_err () {
  if [ x"$no_link" == x"" ]; then
    no_link=$DEV
  else
    no_link="$no_link "$DEV
  fi
}

function _status_check () {
  if [ ! -d /sys/class/net/$DEV ]; then
    _say_err
    link=0
    return
  fi
  up=$(ip link show dev $DEV | grep 'DOWN' | wc -l)
  if [ x"$up" != x"0" ]; then
    link=0
    _say_err
    return
  fi
}

function _check_is_bonding () {
  if [ $link -eq 0 ]; then
    return
  fi

  if [ -f /sys/class/net/${DEV}/bonding/slaves ] ;then
    slaves=$(cat /sys/class/net/${DEV}/bonding/slaves)
  else
    slaves=$DEV
  fi
}

function check_ethN_online () {
  # ip link show check interface up
  _status_check
  # check bonding mode
  _check_is_bonding

  # no pass, return
  if [ $link -eq 0 ]; then
    return
  fi

  # physical link check
  link=0
  for dev in $slaves
  do
    ethtool $dev | grep 'Link detected: yes' > /dev/null
    if [ x"$?" == x"0" ]; then
      link=1
    fi
  done

  if [ $link -eq 0 ]; then
    _say_err
  fi
  #echo "link ok"
}

function link_check () {
  for DEV in $*
  do
    link=1
    check_ethN_online 
  done

  if [ x"$no_link" != x"" ]; then
    echo "no_link | $no_link"
  fi
}

# Only for GNU/Linux
os_=$(uname -o)
if [ $os_ != 'GNU/Linux' ]; then
  echo "OS Type check failed: Not GNU/Linux!"
  exit 1
fi

if [ x"$1" == x"" ]; then
  echo "Usage: $0 ethN ethM ..."
  exit 1
fi


link_check $*
