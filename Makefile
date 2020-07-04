dev:
	${MAKE} clean
	pip3 install -e . -v

py:
	python3 examples/classification_binary.py 1

cpp:
	python3 examples/classification_binary.py 1 -l cpp

all:
	python3 setup.py build_ext --inplace

clean:
	rm -rf *.out *.bin *.exe *.o *.a *.so test build

clang:
	CXX="clang" CC="clang" pip3 install -e . -v

clang-dev-sanitizer-memory:
	CXX="clang" LDFLAGS="-fsanitize=memory -fsanitize-memory-track-origins=2 -O1 -fno-optimize-sibling-calls" CC="clang -fsanitize=memory -fsanitize-memory-track-origins=2 -O1 -fno-optimize-sibling-calls" pip3 install -e . -v

clang-dev-sanitizer-address:
	CXX="clang" LDFLAGS="-fsanitize=address -fno-omit-frame-pointer" CC="clang -fsanitize=address -fno-omit-frame-pointer" pip3 install -e . -v

clang-dev-sanitizer-undefined_behavior:
	CXX="clang" LDFLAGS="-fsanitize=undefined" CC="clang -fsanitize=undefined" pip3 install -e . -v

clang-dev-sanitizer-thread:
	CXX="clang" LDFLAGS="-fsanitize=thread" CC="clang -fsanitize=thread" pip3 install -e . -v

build:
	x86_64-linux-gnu-gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -w -std=c++17
	x86_64-linux-gnu-gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/wrapper.cpp -o build/temp.linux-x86_64-3.8/plexus/wrapper.o -w -std=c++17
	x86_64-linux-gnu-g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 build/temp.linux-x86_64-3.8/plexus/plexus.o build/temp.linux-x86_64-3.8/plexus/wrapper.o -o build/lib.linux-x86_64-3.8/cplexus.cpython-38-x86_64-linux-gnu.so

gdb:
	gdb -ex run --args /usr/bin/python3 examples/classification_binary.py 1 -l cpp
