set nocompatible
syntax on
set background=dark
set tabstop=4
set ignorecase 
set smartcase
set incsearch
set nohlsearch
filetype plugin on
filetype indent on
filetype plugin indent on
let perl_fold = 0
let perl_fold_blocks = 0
set expandtab
set smartindent
set autoindent
set softtabstop=4
set shiftwidth=4
set foldmethod=indent
set number
set relativenumber
set fileformat=unix

set path+=**
set wildmenu

command! MakeTags !ctags -R . 
" ^] - tag
" g^] - globa tag
" ^t - jumba back up the tag stack
"
"auto compleat
"^n
"^x^n
"^x^]
"^x^f - file

"ctrl-R 0
"q/p enter

"netrw
let g:netrw_banner = 0
let g:netrw_browse_split = 4
let g:netrw_altv = 1
let g:netrw_liststyle=3
