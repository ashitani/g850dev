SOURCE = test.xsm
BIN = test.bin
IHX = test.ihx

XSM_JAR_PATH = "../../../xsm/xsm/xsm.jar"
XSM_LIB_PATH = "../../../xsm/xsm/library"

.PHONY: all run
all: $(IHX)

$(BIN): $(SOURCE)
	java -jar $(XSM_JAR_PATH) $(SOURCE) -library $(XSM_LIB_PATH) -addressmap -optimize off -optimizejump off $(BIN)

$(IHX): $(BIN)
	python ../../tools/bin2ihx.py $(BIN) 0x100

clean:
	rm -rf $(IHX) $(BIN)

dump:
	od -tx1 $(BIN)

dis:
	z88dk-dis $(BIN)

run:
	g800 $(IHX)