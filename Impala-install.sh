#!/bin/bash                                                                     
                                                                                
# define highlight function                                                     
color()(set -o pipefail;"$@" 2>&1>&3|sed $'s,.*,\e[31m&\e[m,'>&2)3>&1           
                                                                                
for package in gcc g++ make automake cmake libtool git libboost-all-dev libbz2-dev libzip-dev libsasl2-dev subversion maven bison flex clang-3.3 python-setuptools libevent1-dev libtbb-dev libgdal-dev
do                                                                              
  color dpkg-query -l $package || sudo aptitutde -y install $package > /dev/null
done                                                                            
                                                                                
# By 12-4-2014, libdb4.8-dev is removed from repo, search from http://packages.ubuntu.com/
#color dpkg-query -l libdb4.8-dev || wget http://mirrors.kernel.org/ubuntu/pool/main/d/db/libdb4.8-dev_4.8.24-1ubuntu1_amd64.deb && sudo dpkg -i libdb4.8-dev_4.8.24-1ubuntu1_amd64.deb
# https://github.com/litecoin-project/litecoin/issues/47                        
color dpkg-query -l libdb5.1-dev || sudo aptitude -y install libdb5.1-dev > /dev/null
                                                                                
                                                                                
# link to version 3.3, we seem to get llvm installed when installing clang-3.3  
sudo update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-3.3 33
sudo update-alternatives --install /usr/bin/opt opt /usr/bin/opt-3.3 33         
                                                                                
# adjust gdal location                                                          
color sudo ln -s /usr/lib/libgdal.so /usr/local/lib/libgdal.so || ls -l /usr/local/lib/libgdal.so
                                                                                
                                                                                
IMPALA="Impala"                                                                 
BRANCH=cdh5-trunk                                                               
if [ -d "$IMPALA" ]; then                                                       
  cd $IMPALA && git show-ref --verify --quiet refs/heads/$BRANCH && echo "Already got branch $BRANCH" || echo -e "\033[0;31mBranch $BRANCH not found"
else                                                                            
  # impala not found                                                            
  git clone https://github.com/cloudera/Impala.git && cd $IMPALA && git checkout $BRANCH                             
fi
