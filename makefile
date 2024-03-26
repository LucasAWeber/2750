CC=clang
CFLAGS=-Wall -pedantic -std=c99

all: libphylib.so _phylib.so
	export LD_LIBRARY_PATH=`pwd`

libphylib.so: phylib.o
	$(CC) $(CFLAGS) -shared phylib.o -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c -fPIC phylib.c -o phylib.o

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

clean:
	rm -f *.o *.so