# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: keyvalue.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ekeyvalue.proto\x12\rkeyvaluestore\"\x1d\n\x0b\x45xistsReply\x12\x0e\n\x06result\x18\x01 \x01(\x08\"-\n\x0fPutBytesRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"\x1c\n\rPutBytesReply\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1e\n\x0fGetBytesRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1e\n\rGetBytesReply\x12\r\n\x05value\x18\x01 \x01(\x0c\"\'\n\tFileChunk\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05\x63hunk\x18\x02 \x01(\x0c\x32\xd5\x03\n\rKeyValueStore\x12\x46\n\x06\x45xists\x12\x1e.keyvaluestore.GetBytesRequest\x1a\x1a.keyvaluestore.ExistsReply\"\x00\x12\x46\n\x06\x44\x65lete\x12\x1e.keyvaluestore.GetBytesRequest\x1a\x1a.keyvaluestore.ExistsReply\"\x00\x12J\n\x08PutBytes\x12\x1e.keyvaluestore.PutBytesRequest\x1a\x1c.keyvaluestore.PutBytesReply\"\x00\x12J\n\x08GetBytes\x12\x1e.keyvaluestore.GetBytesRequest\x1a\x1c.keyvaluestore.GetBytesReply\"\x00\x12L\n\x0ePutBytesStream\x12\x18.keyvaluestore.FileChunk\x1a\x1c.keyvaluestore.PutBytesReply\"\x00(\x01\x12N\n\x0eGetBytesStream\x12\x1e.keyvaluestore.GetBytesRequest\x1a\x18.keyvaluestore.FileChunk\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'keyvalue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_EXISTSREPLY']._serialized_start=33
  _globals['_EXISTSREPLY']._serialized_end=62
  _globals['_PUTBYTESREQUEST']._serialized_start=64
  _globals['_PUTBYTESREQUEST']._serialized_end=109
  _globals['_PUTBYTESREPLY']._serialized_start=111
  _globals['_PUTBYTESREPLY']._serialized_end=139
  _globals['_GETBYTESREQUEST']._serialized_start=141
  _globals['_GETBYTESREQUEST']._serialized_end=171
  _globals['_GETBYTESREPLY']._serialized_start=173
  _globals['_GETBYTESREPLY']._serialized_end=203
  _globals['_FILECHUNK']._serialized_start=205
  _globals['_FILECHUNK']._serialized_end=244
  _globals['_KEYVALUESTORE']._serialized_start=247
  _globals['_KEYVALUESTORE']._serialized_end=716
# @@protoc_insertion_point(module_scope)
