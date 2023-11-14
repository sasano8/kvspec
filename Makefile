generate-grpc:
	@python -m grpc_tools.protoc -I. --python_out=kvspec/_grpc --grpc_python_out=kvspec/_grpc keyvalue.proto
	@sed -i 's/import keyvalue_pb2 as keyvalue__pb2/from . import keyvalue_pb2 as keyvalue__pb2/' kvspec/_grpc/keyvalue_pb2_grpc.py

generate-graphql:
	@strawberry export-schema kvspec.servers._graphql:schema --output schema.graphql
