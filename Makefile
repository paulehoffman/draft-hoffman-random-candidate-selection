all: draft-hoffman-random-candidate-selection.xml draft-hoffman-random-candidate-selection.txt draft-hoffman-random-candidate-selection.html
	./candidate-selection.py namelist >namedisplay.out
	./candidate-selection.py namelist selectioninfo >selection.out
	kdrfc -c -t -h draft-hoffman-random-candidate-selection.mkd 2>/tmp/kram-errors.txt
	grep --regexp=Ignoring --invert-match /tmp/kram-errors.txt || true
	mv draft-hoffman-random-candidate-selection.xml draft-hoffman-random-candidate-selection.v2xml
	mv draft-hoffman-random-candidate-selection.v2v3.xml draft-hoffman-random-candidate-selection.xml

.PRECIOUS: %.xml
