.PHONY: all download srpm rpm clean

all: rpm

download:
	./build.sh download

srpm:
	./build.sh srpm

rpm:
	./build.sh rpm

clean:
	./build.sh clean
