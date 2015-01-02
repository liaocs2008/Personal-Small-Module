#!/bin/bash                                                                     
if [ $# -gt 0 ]                                                                 
then                                                                            
  PROJECT_NAME=$1                                                               
  echo "CREATING PROJECT ..." ${PROJECT_NAME}                                   
  mkdir code/${PROJECT_NAME}                                                    
  mkdir data/${PROJECT_NAME}                                                    
  if [ $# -gt 1 ] && [ $2 -eq 1 ];                                              
  then                                                                          
    git init code/${PROJECT_NAME}                                               
  fi                                                                            
  echo "DONE!"                                                                  
else                                                                            
  echo "bash $0 [project_name] [git_initial]"                                   
  echo "git_initial: 0 (default) for no, 1 for yes"                             
fi
