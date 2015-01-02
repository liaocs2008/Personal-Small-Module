#!/bin/bash
git clone https://github.com/mli/third_party parameter_thirdparty                  
cd parameter_thirdparty && bash install.sh                                         
cd ..                                                                              
git clone https://github.com/mli/parameter_server.git                              
cd parameter_server                                                                
ln -s ../parameter_thirdparty third_party                                          
make -j8                                                                           
                                                                                   
### test                                                                           
cd data && bash rcv1_small.sh                                                      
cd ../script                                                                       
./local.sh 1 4 ../config/rcv1/batch_l1lr.conf
