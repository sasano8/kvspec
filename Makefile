generate-grpc:
	@python -m grpc_tools.protoc -I. --python_out=camera/_grpc --grpc_python_out=camera/_grpc keyvalue.proto
	@sed -i 's/import keyvalue_pb2 as keyvalue__pb2/from . import keyvalue_pb2 as keyvalue__pb2/' camera/_grpc/keyvalue_pb2_grpc.py
