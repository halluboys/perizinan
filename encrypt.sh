#!/bin/bash

#Install SHC
apt-get install build-essential -y
wget -q -c https://github.com/neurobin/shc/archive/4.0.2.tar.gz
tar xzvf 4.0.2.tar.gz > /dev/null
cd shc-4.0.2/
./configure > /dev/null
make
make install > /dev/null

#Masuk Direktori
cd
#Encrypt File
shc -r -f menu-shadowsocks
shc -r -f menu
shc -r -f ipsec
shc -r -f ins-xray
shc -r -f sodosok
shc -r -f ssr
shc -r -f sstp
shc -r -f wg
shc -r -f addtrgo
shc -r -f cektrgo
shc -r -f deltrgo
shc -r -f renewtrgo
shc -r -f addhost 
shc -r -f addl2tp
shc -r -f addpptp
shc -r -f addss
shc -r -f addssh
shc -r -f addssr
shc -r -f addsstp
shc -r -f addtrojan
shc -r -f addvless
shc -r -f addwg
shc -r -f addv2ray
shc -r -f autobackup
shc -r -f autokill
shc -r -f backup
shc -r -f cekpptp
shc -r -f cekss
shc -r -f cekssh
shc -r -f ceksstp
shc -r -f cektrojan
shc -r -f cekvless
shc -r -f cekwg
shc -r -f cekv2ray
shc -r -f certv2ray
shc -r -f changeport
shc -r -f dell2tp
shc -r -f delpptp
shc -r -f delss
shc -r -f delssh
shc -r -f delssr
shc -r -f delsstp
shc -r -f deltrojan
shc -r -f delvless
shc -r -f delwg
shc -r -f delv2ray
shc -r -f delete
shc -r -f info
shc -r -f izin
shc -r -f menu-domain
shc -r -f ceklim
shc -r -f menu-vpn
shc -r -f menu-ssh
shc -r -f menu-tools
shc -r -f menu-trojan
shc -r -f menu-v2ray
shc -r -f menu-wireguard
shc -r -f menu-l2tp
shc -r -f member
shc -r -f portovpn
shc -r -f portsquid
shc -r -f portssl
shc -r -f portsstp
shc -r -f porttrojan
shc -r -f portvless
shc -r -f portwg
shc -r -f portv2ray
shc -r -f ssh-vpn
shc -r -f renewl2tp
shc -r -f renewpptp
shc -r -f renewss
shc -r -f renewssh
shc -r -f renewssr
shc -r -f renewsstp
shc -r -f renewtrojan
shc -r -f renewvless
shc -r -f renewwg
shc -r -f renewv2ray
shc -r -f restart
shc -r -f restore
shc -r -f strt
shc -r -f swapkvm
shc -r -f tendang
shc -r -f trialssh
shc -r -f xp
shc -r -f cf
shc -r -f restart
shc -r -f vpn
shc -r -f setup
shc -r -f trialv2ray
shc -r -f trialwg
shc -r -f trialvless
shc -r -f trialtrgo
shc -r -f trialtrojan
shc -r -f triall2tp
shc -r -f trialpptp
shc -r -f trialsstp
shc -r -f trialss
shc -r -f trialssr
shc -r -f status
shc -r -f running
shc -r -f trialssr
shc -r -f ohp
shc -r -f edu
shc -r -f set-br
shc -r -f strt
shc -r -f limitspeed
shc -r -f menu-pptp
shc -r -f menu-sstp
shc -r -f menu-trial
shc -r -f menu-backup
shc -r -f about
shc -r -f autoreboot
shc -r -f bbr
shc -r -f ceklim
shc -r -f cekssh
shc -r -f clearlog
shc -r -f delexp
shc -r -f portsshnontls
shc -r -f portsshws
shc -r -f webmin
shc -r -f ws-nontls.py
shc -r -f ws-ovpn.py
shc -r -f ws-tls.py


#Move file
mv portsshws.x portsshws
mv portsshnontls.x portsshnontls
mv portsquid.x portsquid
mv portsquid.x portsquid
mv portovpn.x portovpn
mv member.x member
mv info.x info
mv delssh.x delssh
mv delexp.x delexp
mv clearlog.x clearlog
mv changeport.x changeport
mv cekssh.x cekssh
mv ceklim.x ceklim
mv bbr.x bbr
mv autoreboot.x autoreboot
mv autokill.x autokill
mv addssh.x addssh
mv addhost.x addhost
mv renewss.x renewss
mv about.x about
mv delss.x delss
mv cekss.x cekss
mv addss.x addss
mv menu-wireguard.x menu-wireguard
mv menu-vpn.x menu-vpn
mv menu-v2ray.x menu-v2ray
mv menu-trojan.x menu-trojan
mv menu-tools.x menu-tools
mv menu-ssh.x menu-ssh
mv menu-domain.x menu-domain
mv menu-backup.x menu-backup
mv strt.x strt
mv menu-trial.x menu-trial
mv menu-sstp.x menu-sstp
mv menu-pptp.x menu-pptp
mv menu-shadowsocks.x menu-shadowsocks
mv menu.x menu
mv ipsec.x ipsec
mv ins-xray.x ins-xray
mv sodosok.x sodosok
mv ssr.x ssr
mv sstp.x sstp
mv wg.x wg
mv deltrgo.x deltrgo
mv addtrgo.x addtrgo
mv renewtrgo.x renewtrgo
mv cektrgo.x cektrgo
mv ssh-vpn.x ssh-vpn
mv setup.x setup
mv limitspeed.x limitspeed
mv set-br.x set-br
mv trialv2ray.x trialv2ray
mv trialwg.x trialwg
mv trialvless.x trialvless
mv trialtrgo.x trialtrgo
mv trialtrgo.x trialtrojan
mv triall2tp.x triall2tp
mv trialpptp.x trialpptp
mv trialsstp.x trialsstp
mv trialss.x trialss
mv trialssr.x trialssr
mv status.x status
mv running.x running
mv trialssr.x trialssr
mv ohp.x ohp
mv edu.x edu
mv setup.x setup
mv cf.x cf
mv vpn.x vpn

#Remove Extension
rm -r -f *.x.c
clear
echo -e "Encrypt Successfull..." | lolcat 
rm -r -f encrypt
cd
rm -rf shc-4.0.2
rm -rf 4.0.2.tar.gz
rm -rf master.zip
rm -rf encrypt.sh
