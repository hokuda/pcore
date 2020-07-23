all: pcore/pcore pcore.zip

pcore.rhel8: pcore.rhel8/pcore pcore.rhel8.zip

pcore/pcore: src/pcore.main src/getdebuginfo
	@if [ ! -d pcore_tmp ]; then mkdir pcore_tmp; fi
	./embed.py src/getdebuginfo < src/pcore.main > pcore_tmp/pcore
	mv pcore_tmp pcore
	chmod +x pcore/pcore

pcore.zip: pcore/pcore
	zip pcore.zip -r pcore

pcore.rhel8/pcore: src/pcore.main src/getdebuginfo
	@if [ ! -d pcore.rhel8_tmp ]; then mkdir pcore.rhel8_tmp; fi
	./rhel8.sh < src/pcore.main > pcore.rhel8_tmp/pcore.main.rhel8
	./rhel8.sh < src/getdebuginfo > pcore.rhel8_tmp/getdebuginfo.rhel8
	./embed.py pcore.rhel8_tmp/getdebuginfo.rhel8 < pcore.rhel8_tmp/pcore.main.rhel8 > pcore.rhel8_tmp/pcore
	mv pcore.rhel8_tmp pcore.rhel8
	rm pcore.rhel8/pcore.main.rhel8 pcore.rhel8/getdebuginfo.rhel8
	chmod +x pcore.rhel8/pcore

pcore.rhel8.zip: pcore.rhel8/pcore
	zip pcore.rhel8.zip -r pcore.rhel8

clean:
	rm -fr pcore pcore_tmp pcore.zip pcore.rhel8 pcore.rhel8_tmp pcore.rhel8.zip
