1: all
all : main.pdf view github
#all : main.pdf view
main.pdf : 
	#bibtex frontiers 
	latex -halt-on-error --shell-escape frontiers.tex
	dvipdfm frontiers.dvi
view :
	open -a Preview frontiers.pdf -g
github:
	git commit -a -m "`whoami` edit"
	git push origin master
