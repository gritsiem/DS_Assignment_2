# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: products.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='products.proto',
  package='products',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eproducts.proto\x12\x08products\"f\n\x10SelectOneMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0e\n\x06\x63olumn\x18\x02 \x01(\t\x12\x14\n\x0csearch_value\x18\x03 \x01(\t\x12\x18\n\x10selected_columns\x18\x04 \x01(\t\"e\n\x11SelectManyMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0f\n\x07\x63olumns\x18\x02 \x01(\t\x12\x15\n\rsearch_values\x18\x03 \x01(\t\x12\x14\n\x0creturn_index\x18\x04 \x01(\x05\"D\n\rInsertMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0f\n\x07\x63olumns\x18\x02 \x01(\t\x12\x0e\n\x06values\x18\x03 \x01(\t\"r\n\rUpdateMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0f\n\x07\x63olumns\x18\x02 \x01(\t\x12\x0e\n\x06values\x18\x03 \x01(\t\x12\x15\n\rcondition_col\x18\x04 \x01(\t\x12\x15\n\rcondition_val\x18\x05 \x01(\x05\"x\n\x11UpdateManyMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0f\n\x07\x63olumns\x18\x02 \x01(\t\x12\x0e\n\x06values\x18\x03 \x01(\t\x12\x16\n\x0e\x63ondition_cols\x18\x04 \x01(\t\x12\x16\n\x0e\x63ondition_vals\x18\x05 \x01(\t\"S\n\rDeleteMessage\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x16\n\x0e\x63ondition_cols\x18\x04 \x01(\t\x12\x16\n\x0e\x63ondition_vals\x18\x05 \x01(\t\"\x1e\n\x0fgeneralResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t2\xcb\x03\n\x08Products\x12J\n\x0fGetRowsByColumn\x12\x1a.products.SelectOneMessage\x1a\x19.products.generalResponse\"\x00\x12P\n\x14GetRowByMultiColumns\x12\x1b.products.SelectManyMessage\x1a\x19.products.generalResponse\"\x00\x12\x45\n\rInsertProduct\x12\x17.products.InsertMessage\x1a\x19.products.generalResponse\"\x00\x12I\n\x11UpdateRowByColumn\x12\x17.products.UpdateMessage\x1a\x19.products.generalResponse\"\x00\x12L\n\x10UpdateRowByMulti\x12\x1b.products.UpdateManyMessage\x1a\x19.products.generalResponse\"\x00\x12\x41\n\tDeleteRow\x12\x17.products.DeleteMessage\x1a\x19.products.generalResponse\"\x00\x62\x06proto3'
)




_SELECTONEMESSAGE = _descriptor.Descriptor(
  name='SelectOneMessage',
  full_name='products.SelectOneMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.SelectOneMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='column', full_name='products.SelectOneMessage.column', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='search_value', full_name='products.SelectOneMessage.search_value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='selected_columns', full_name='products.SelectOneMessage.selected_columns', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=130,
)


_SELECTMANYMESSAGE = _descriptor.Descriptor(
  name='SelectManyMessage',
  full_name='products.SelectManyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.SelectManyMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='columns', full_name='products.SelectManyMessage.columns', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='search_values', full_name='products.SelectManyMessage.search_values', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='return_index', full_name='products.SelectManyMessage.return_index', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=132,
  serialized_end=233,
)


_INSERTMESSAGE = _descriptor.Descriptor(
  name='InsertMessage',
  full_name='products.InsertMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.InsertMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='columns', full_name='products.InsertMessage.columns', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='values', full_name='products.InsertMessage.values', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=235,
  serialized_end=303,
)


_UPDATEMESSAGE = _descriptor.Descriptor(
  name='UpdateMessage',
  full_name='products.UpdateMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.UpdateMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='columns', full_name='products.UpdateMessage.columns', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='values', full_name='products.UpdateMessage.values', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_col', full_name='products.UpdateMessage.condition_col', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_val', full_name='products.UpdateMessage.condition_val', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=305,
  serialized_end=419,
)


_UPDATEMANYMESSAGE = _descriptor.Descriptor(
  name='UpdateManyMessage',
  full_name='products.UpdateManyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.UpdateManyMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='columns', full_name='products.UpdateManyMessage.columns', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='values', full_name='products.UpdateManyMessage.values', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_cols', full_name='products.UpdateManyMessage.condition_cols', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_vals', full_name='products.UpdateManyMessage.condition_vals', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=421,
  serialized_end=541,
)


_DELETEMESSAGE = _descriptor.Descriptor(
  name='DeleteMessage',
  full_name='products.DeleteMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='products.DeleteMessage.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_cols', full_name='products.DeleteMessage.condition_cols', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition_vals', full_name='products.DeleteMessage.condition_vals', index=2,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=543,
  serialized_end=626,
)


_GENERALRESPONSE = _descriptor.Descriptor(
  name='generalResponse',
  full_name='products.generalResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='products.generalResponse.msg', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=628,
  serialized_end=658,
)

DESCRIPTOR.message_types_by_name['SelectOneMessage'] = _SELECTONEMESSAGE
DESCRIPTOR.message_types_by_name['SelectManyMessage'] = _SELECTMANYMESSAGE
DESCRIPTOR.message_types_by_name['InsertMessage'] = _INSERTMESSAGE
DESCRIPTOR.message_types_by_name['UpdateMessage'] = _UPDATEMESSAGE
DESCRIPTOR.message_types_by_name['UpdateManyMessage'] = _UPDATEMANYMESSAGE
DESCRIPTOR.message_types_by_name['DeleteMessage'] = _DELETEMESSAGE
DESCRIPTOR.message_types_by_name['generalResponse'] = _GENERALRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SelectOneMessage = _reflection.GeneratedProtocolMessageType('SelectOneMessage', (_message.Message,), {
  'DESCRIPTOR' : _SELECTONEMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.SelectOneMessage)
  })
_sym_db.RegisterMessage(SelectOneMessage)

SelectManyMessage = _reflection.GeneratedProtocolMessageType('SelectManyMessage', (_message.Message,), {
  'DESCRIPTOR' : _SELECTMANYMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.SelectManyMessage)
  })
_sym_db.RegisterMessage(SelectManyMessage)

InsertMessage = _reflection.GeneratedProtocolMessageType('InsertMessage', (_message.Message,), {
  'DESCRIPTOR' : _INSERTMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.InsertMessage)
  })
_sym_db.RegisterMessage(InsertMessage)

UpdateMessage = _reflection.GeneratedProtocolMessageType('UpdateMessage', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.UpdateMessage)
  })
_sym_db.RegisterMessage(UpdateMessage)

UpdateManyMessage = _reflection.GeneratedProtocolMessageType('UpdateManyMessage', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEMANYMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.UpdateManyMessage)
  })
_sym_db.RegisterMessage(UpdateManyMessage)

DeleteMessage = _reflection.GeneratedProtocolMessageType('DeleteMessage', (_message.Message,), {
  'DESCRIPTOR' : _DELETEMESSAGE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.DeleteMessage)
  })
_sym_db.RegisterMessage(DeleteMessage)

generalResponse = _reflection.GeneratedProtocolMessageType('generalResponse', (_message.Message,), {
  'DESCRIPTOR' : _GENERALRESPONSE,
  '__module__' : 'products_pb2'
  # @@protoc_insertion_point(class_scope:products.generalResponse)
  })
_sym_db.RegisterMessage(generalResponse)



_PRODUCTS = _descriptor.ServiceDescriptor(
  name='Products',
  full_name='products.Products',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=661,
  serialized_end=1120,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetRowsByColumn',
    full_name='products.Products.GetRowsByColumn',
    index=0,
    containing_service=None,
    input_type=_SELECTONEMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetRowByMultiColumns',
    full_name='products.Products.GetRowByMultiColumns',
    index=1,
    containing_service=None,
    input_type=_SELECTMANYMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='InsertProduct',
    full_name='products.Products.InsertProduct',
    index=2,
    containing_service=None,
    input_type=_INSERTMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateRowByColumn',
    full_name='products.Products.UpdateRowByColumn',
    index=3,
    containing_service=None,
    input_type=_UPDATEMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateRowByMulti',
    full_name='products.Products.UpdateRowByMulti',
    index=4,
    containing_service=None,
    input_type=_UPDATEMANYMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteRow',
    full_name='products.Products.DeleteRow',
    index=5,
    containing_service=None,
    input_type=_DELETEMESSAGE,
    output_type=_GENERALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PRODUCTS)

DESCRIPTOR.services_by_name['Products'] = _PRODUCTS

# @@protoc_insertion_point(module_scope)
