#!/bin/bash                                                                     
if [ $# -eq 1 ]                                                                 
then                                                                            
  PROJECT_NAME=$1                                                               
  echo "REMOVING PROJECT ..." ${PROJECT_NAME}                                   
  rm -rf code/${PROJECT_NAME}                                                   
  rm -rf data/${PROJECT_NAME}                                                   
  echo "DONE!"                                                                  
else                                                                            
  echo "bash $0 [project_name]"                                                 
fi
