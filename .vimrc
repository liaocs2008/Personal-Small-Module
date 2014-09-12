set nocompatible
syntax on
filetype off  "vundle setting required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/vundle'

"vim-scripts repos
"git
Plugin 'scrooloose/nerdtree'
let NERDTreeWinPos='right'
let NERDTreeWinSize=31
let NERDTreeChDirMode=1

Plugin 'jcf/vim-latex'
let g:tex_flavor='latex'

call vundle#end()
filetype plugin indent on

set number

set cindent

"Automatically change the current directory
autocmd BufEnter * silent! lcd %:p:h

"Tab
set shiftwidth=4
set tabstop=4
set expandtab

"latex setting
set grepprg=grep\ -nH\ $*
set sw=2
set iskeyword+=:
