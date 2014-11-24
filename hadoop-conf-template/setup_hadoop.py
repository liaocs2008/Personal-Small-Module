#!/usr/bin/python
import os
import sys
def setup_hadoop(root_dir, template_vars):
  for path, dirs, files in os.walk(root_dir):
    if path.find(".svn") == -1:
      #print path, dirs, files
      for filename in files:
        if filename.endswith(".template"):
          new_filename = filename.replace(".template", "")
          dest_file = os.path.join(path, new_filename)
          with open(os.path.join(path, filename)) as src:
            with open(dest_file, "w") as dest:
              text = src.read()
              for key in template_vars:
                text = text.replace("{{" + key + "}}", template_vars[key])
              dest.write(text)
              dest.close()

def main():
  template_vars = {
    "master": "localhost",
    "hive_metastore_db":"leo_metastore",
    "hive_metastore_db_user":"leo",
    "hive_metastore_db_pwd":"mypassword",
    "hadoop_proxyuser":"leo",
    "hdfs_namenode_path":"/home/leo/Hadoop/NameNode/",
    "hdfs_datanode_path":"/home/leo/Hadoop/DataNode/"
  }
  current_dir = os.getcwd()
  if (len(sys.argv) > 1):
    current_dir = sys.argv[1]
  setup_hadoop(current_dir, template_vars);

if __name__ == "__main__":
  main()
