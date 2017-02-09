#!/bin/sh

list_cythonize=(
                "calc_p_alpha"
                "cluster_core"
                "cluster_two_level"
                "module"
                "mapequation"
                "modularity"
                "quality"
                "cluster_tree")
lib="./lib/"
ext_from=".py"
ext_to=".pyx"

echo "files below with be changed from *.pyx to *.py"
echo ${list_cythonize[*]}

for((i=0;i<${#list_cythonize[@]};++i))
do
    mv $lib${list_cythonize[$i]}$ext_from  $lib${list_cythonize[$i]}$ext_to 
done
