pcore/pcore: src/pcore.main src/get_debuginfo.py
	@if [ ! -d pcore ]; then mkdir pcore; fi
	./embed.py < src/pcore.main > pcore/pcore
	chmod +x pcore/pcore
	zip pcore.zip -r pcore

all: pcore/pcore

clean:
	rm -fr pcore pcore.zip
