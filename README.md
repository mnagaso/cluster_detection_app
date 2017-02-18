# Project ENOT #

Project ENOT:cat: is a code
dedicated for clustering using "random walker" or "Map Equation".

## code description here ##
* python base
* csv in/output support

-------
#Requirements:
scipy  
numpy   
cython (optional)  
ete3 (for tree visualization)  


##supported python version = 3.5.2
we suggest to use pyenv for switching your python version.

installation  
`$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv`

write pathes on ~/.bash_profile or .bashrc
add three lines by using your favorite text editor  
`export PYENV_ROOT=$HOME/.pyenv`  
`export PATH=$PYENV_ROOT/bin:$PATH`  
`eval "$(pyenv init -)"`

reload your .bash_profile (or bashrc)  
`$source ~/.bash_profile`  
(or `$source ~/.bashrc`)

install python version 3.5.2  
`$pyenv install 3.5.2`

switch your python version  
`$pyenv global 3.5.2`

you may verify the version now using  
`$pyenv versions`