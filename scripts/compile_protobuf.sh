#!/bin/sh
python3 -m grpc_tools.protoc -I=src/libdots/io/message_definitions --python_out=src/libdots/io/messages --pyi_out=./src/libdots/io/messages  src/libdots/io/message_definitions/*.proto
