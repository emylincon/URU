clear
echo 'Preparing your platform for URU. . .'
sleep 2
apt update -y
apt install python3-psutil -y
apt install python3-matplotlib -y
apt install python3-pip -y
pip3 install drawnow
clear
echo 'All done, Ready to Use!!'
