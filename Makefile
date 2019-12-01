pcore/pcore: src/pcore.main src/getdebuginfo
	@if [ ! -d pcore ]; then mkdir pcore; fi
	./embed.py src/getdebuginfo < src/pcore.main > pcore/pcore
	chmod +x pcore/pcore
	zip pcore.zip -r pcore

pcore.rhel8/pcore: src/pcore.main src/getdebuginfo
	@if [ ! -d pcore.rhel8 ]; then mkdir pcore.rhel8; fi
	./rhel8.sh < src/pcore.main > pcore.rhel8/pcore.main.rhel8
	./rhel8.sh < src/getdebuginfo > pcore.rhel8/getdebuginfo.rhel8
	./embed.py pcore.rhel8/getdebuginfo.rhel8 < pcore.rhel8/pcore.main.rhel8 > pcore.rhel8/pcore
	rm pcore.rhel8/pcore.main.rhel8 pcore.rhel8/getdebuginfo.rhel8
	chmod +x pcore.rhel8/pcore
	zip pcore.rhel8.zip -r pcore.rhel8

all: pcore/pcore

pcore.rhel8: pcore.rhel8/pcore

clean:
	rm -fr pcore pcore.zip pcore.rhel8 pcore.rhel8.zip
