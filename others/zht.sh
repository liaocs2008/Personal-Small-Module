#!/bin/bash
# install C++ protobuf first, then C version
tar -zxvf protobuf-2.4.1.tar.gz                                                    
cd protobuf-2.4.1                                                                  
./configure                                                                        
make                                                                               
make install

cd ..

export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
tar -zxvf protobuf-c-0.15.tar.gz                                                
cd protobuf-c-0.15                                                              
./configure CXXFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib              
make                                                                            
make install

# If it reports:
# This program was compiled against version 2.4.1 of the Protocol Buffer runtime library, which is not compatible with the installed version (2.5.0).
# ...
# libprotoc.so.7: cannot open shared object file: no such file or directory

# Try "sudo apt-get remove protobuf-compiler"
