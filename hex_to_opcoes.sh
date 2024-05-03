!#/bin/bash

#teste.txt = arquivo #python com keystone #engine que gera os #opcodes do shellcode

cat teste.txt | grep ';"' | cut -f2 -d'"' | cut -f1 -d';' > teste2.txt

#teste2.txt = arquivo com #apenas as instruções #para o nasm-shell

cat teste2.txt | while read line ; do echo $line | msf-nasm_shell ; done 2>/dev/null | tee soopcodes.txt
