

default:
	cython cli.py --embed
	gcc -Os -I /usr/include/python2.7 -o cli cli.c -lpython2.7 -lpthread -lm -lutil -ldl

clean:
	rm -f cli cli.c

