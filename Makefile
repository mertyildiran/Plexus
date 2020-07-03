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

clang-dev-sanitizer-memory:
	clang -fsanitize=memory -fsanitize-memory-track-origins=2 -O1 -fno-optimize-sibling-calls -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -std=c++17
	clang -fsanitize=memory -fsanitize-memory-track-origins=2 -O1 -fno-optimize-sibling-calls -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/wrapper.cpp -o build/temp.linux-x86_64-3.8/plexus/wrapper.o -std=c++17
	clang -fsanitize=memory -fsanitize-memory-track-origins=2 -O1 -fno-optimize-sibling-calls -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 build/temp.linux-x86_64-3.8/plexus/plexus.o build/temp.linux-x86_64-3.8/plexus/wrapper.o -o build/lib.linux-x86_64-3.8/cplexus.cpython-38-x86_64-linux-gnu.so
	cp build/lib.linux-x86_64-3.8/cplexus.cpython-38-x86_64-linux-gnu.so /home/mertyildiran/.local/lib/python3.8/site-packages/plexus.egg-link

clang-dev-sanitizer-address:
	clang -fsanitize=address -fno-omit-frame-pointer -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -std=c++17

clang-dev-sanitizer-undefined_behavior:
	clang -fsanitize=undefined -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -std=c++17

clang-dev-sanitizer-thread:
	clang -fsanitize=thread -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -std=c++17

build:
	x86_64-linux-gnu-gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/plexus.cpp -o build/temp.linux-x86_64-3.8/plexus/plexus.o -w -std=c++17
	x86_64-linux-gnu-gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.8 -c plexus/wrapper.cpp -o build/temp.linux-x86_64-3.8/plexus/wrapper.o -w -std=c++17
	x86_64-linux-gnu-g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 build/temp.linux-x86_64-3.8/plexus/plexus.o build/temp.linux-x86_64-3.8/plexus/wrapper.o -o build/lib.linux-x86_64-3.8/cplexus.cpython-38-x86_64-linux-gnu.so

