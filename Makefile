1: all
#all : main.pdf view github
all : main.pdf view
main.pdf : 
	bibtex frontiers 
	latexmk
	dvipdfm frontiers.dvi
view :
	open -a Preview frontiers.pdf -g
github:
	git commit -a -m "`whoami` edit"
	git push origin master

watch:
	while sleep 1 ; do find . -name '*.tex' -o -name '*.svg' \
	| entr -d make all -f ./Makefile ; done
