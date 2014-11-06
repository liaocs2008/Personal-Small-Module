"Instructions for setup
"git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
":PluginInstall

set nocompatible
syntax on
filetype off  "vundle setting required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/vundle'

"vim-scripts repos
"git
Plugin 'scrooloose/nerdtree'
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
let NERDTreeChDirMode=1


Plugin 'jcf/vim-latex'
let g:tex_flavor='latex'

call vundle#end()

filetype plugin indent on

set number


"Automatically change the current directory
autocmd BufEnter * silent! lcd %:p:h

"Tab
set smartindent
set shiftwidth=2
set tabstop=2
set expandtab

"Vectical matching line
set colorcolumn=80
highlight ColorColumn ctermbg=lightgrey guibg=lightgrey

"Folding
set foldmethod=indent
set foldlevel=1

"latex setting
set grepprg=grep\ -nH\ $*
set sw=2
set iskeyword+=:

" Highlight all instances of word under cursor, when idle.
" Useful when studying strange source code.
" Type z/ to toggle highlighting on/off.
nnoremap z/ :if AutoHighlightToggle()<Bar>set hls<Bar>endif<CR>
function! AutoHighlightToggle()
  let @/ = ''
  if exists('#auto_highlight')
    au! auto_highlight
    augroup! auto_highlight
    setl updatetime=4000
    echo 'Highlight current word: off'
    return 0
  else
    augroup auto_highlight
      au!
      au CursorHold * let @/ = '\V\<'.escape(expand('<cword>'), '\').'\>'
    augroup end
    setl updatetime=500
    echo 'Highlight current word: ON'
    return 1
  endif
endfunction
