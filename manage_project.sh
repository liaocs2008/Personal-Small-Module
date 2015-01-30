#!/bin/bash
if [ $# -gt 0 ]
then
  # caution: shift will take effect and won't change value of $0

  if [ $1 == "c" ] || [ $1 == "create" ];
  then
    shift
    if [ $# -gt 0 ] 
    then
      PROJECT_NAME=$1
      echo "CREATING PROJECT ..." ${PROJECT_NAME}
      mkdir code/${PROJECT_NAME}
      touch code/${PROJECT_NAME}/README
      mkdir data/${PROJECT_NAME}
      mkdir doc/${PROJECT_NAME}
      if [ $# -gt 1 ] && [ $2 -eq 1 ];
      then
        git init code/${PROJECT_NAME}
      fi
      echo "DONE!"
    else
      echo "bash $0 [c|create] [project_name] [git_initial]"
      echo "git_initial: 0 (default) for no, 1 for yes"
    fi
  elif [ $1 == "r" ] || [ $1 == "remove" ];
  then
    shift
    if [ $# -eq 1 ] 
    then
      PROJECT_NAME=$1
      echo "REMOVING PROJECT ..." ${PROJECT_NAME}
      rm -rf code/${PROJECT_NAME}
      rm -rf data/${PROJECT_NAME}
      rm -rf doc/${PROJECT_NAME}
      echo "DONE!"
    else
      echo "bash $0 [r|remove] [project_name]"
    fi
  fi
else
  echo "Leo's project management script."
  echo "Usage:"
  echo "     CREATE PROJECT: bash $0 [c|create] [project_name] [git_initial]"
  echo "        git_initial: 0 (default) for no, 1 for yes"
  echo "     REMOVE PROJECT: bash $0 [r|remove] [project_name]"
  echo ""
  echo "Data and code are seperated."
  echo "This be placed in the same dir as where you create 'code' and 'data' dir." 
fi
