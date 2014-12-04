#!/bin/bash                                                                        
                                                                                   
# -p makes 'mkdir' not caring about if .vim exists.                                
mkdir -p ~/.vim                                                                    
                                                                                   
git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim        
                                                                                   
# -q is to overwrite, -P is to specify output directory                            
wget -q -P ~ https://raw.githubusercontent.com/liaocs2008/Personal-Small-Module/master/.vimrc
                                                                                   
# -c is to run command after loading vim                                           
vim -c :PluginInstall
