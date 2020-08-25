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
set hls

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


" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'vim-syntastic/syntastic'
Plugin 'nvie/vim-flake8'
Plugin 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
Plugin 'kien/ctrlp.vim'

" add all your plugins here (note older versions of Vundle
" used Bundle instead of Plugin)

" ...

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

let python_highlight_all=1
set laststatus=2
set t_Co=256

:nmap <F5> <Esc>:w<cr>:!python %<cr>
:imap <F5> <Esc>:w<cr>:!python %<cr>
