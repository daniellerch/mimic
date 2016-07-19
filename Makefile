

default:
	cython cli.py --embed
	gcc -Os -I /usr/include/python2.7 -o cli.bin cli.c -lpython2.7 -lpthread -lm -lutil -ldl
	cython learn.py --embed
	gcc -Os -I /usr/include/python2.7 -o learn.bin learn.c -lpython2.7 -lpthread -lm -lutil -ldl

clean:
	rm -f cli.c learn.c *.bin
	rm -f */*.pyc */*/*.pyc

