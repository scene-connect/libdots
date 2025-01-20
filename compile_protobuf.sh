#!/bin/sh
python3 -m grpc_tools.protoc -I=src/dots_utilities/io/message_definitions --python_out=src/dots_utilities/io/messages --pyi_out=./src/dots_utilities/io/messages  src/dots_utilities/io/message_definitions/*.proto
