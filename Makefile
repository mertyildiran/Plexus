dev:
	pip3 install -e .

py:
	python3 examples/classification_binary.py 1

cpp:
	python3 examples/classification_binary.py 1 -l cpp

all:
	python3 setup.py build_ext --inplace

clean:
	rm -rf *.out *.bin *.exe *.o *.a *.so test build
