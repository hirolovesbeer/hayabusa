.SUFFIXES: .tex .dvi .aux .log .toc .lof .lot .pdf .ps
F=was
TEX=platex

all: pdf

pdf: dvi
	dvipdfmx $F.dvi

dvi:
	extractbb pictures/*.pdf
	extractbb pictures/*.png
	platex $F.tex
	platex $F.tex

clean:
	rm -f *~ *.{dvi,aux,lof,toc,lot,log,pdf,ps}
