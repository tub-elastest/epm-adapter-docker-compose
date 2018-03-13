# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import client_pb2 as client__pb2


class OperationHandlerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Create = channel.unary_unary(
        '/OperationHandler/Create',
        request_serializer=client__pb2.FileMessage.SerializeToString,
        response_deserializer=client__pb2.ResourceGroupProto.FromString,
        )
    self.Remove = channel.unary_unary(
        '/OperationHandler/Remove',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.StopContainer = channel.unary_unary(
        '/OperationHandler/StopContainer',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.CheckIfContainerExists = channel.unary_unary(
        '/OperationHandler/CheckIfContainerExists',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.CheckIfContainerRunning = channel.unary_unary(
        '/OperationHandler/CheckIfContainerRunning',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.StartContainer = channel.unary_unary(
        '/OperationHandler/StartContainer',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.ExecuteCommand = channel.unary_unary(
        '/OperationHandler/ExecuteCommand',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.DownloadFile = channel.unary_unary(
        '/OperationHandler/DownloadFile',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.FileMessage.FromString,
        )
    self.UploadFile = channel.unary_unary(
        '/OperationHandler/UploadFile',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.CheckStatus = channel.unary_unary(
        '/OperationHandler/CheckStatus',
        request_serializer=client__pb2.Empty.SerializeToString,
        response_deserializer=client__pb2.Status.FromString,
        )


class OperationHandlerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Create(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Remove(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopContainer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckIfContainerExists(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckIfContainerRunning(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StartContainer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ExecuteCommand(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DownloadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UploadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperationHandlerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=client__pb2.FileMessage.FromString,
          response_serializer=client__pb2.ResourceGroupProto.SerializeToString,
      ),
      'Remove': grpc.unary_unary_rpc_method_handler(
          servicer.Remove,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'StopContainer': grpc.unary_unary_rpc_method_handler(
          servicer.StopContainer,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'CheckIfContainerExists': grpc.unary_unary_rpc_method_handler(
          servicer.CheckIfContainerExists,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'CheckIfContainerRunning': grpc.unary_unary_rpc_method_handler(
          servicer.CheckIfContainerRunning,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'StartContainer': grpc.unary_unary_rpc_method_handler(
          servicer.StartContainer,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'ExecuteCommand': grpc.unary_unary_rpc_method_handler(
          servicer.ExecuteCommand,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'DownloadFile': grpc.unary_unary_rpc_method_handler(
          servicer.DownloadFile,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.FileMessage.SerializeToString,
      ),
      'UploadFile': grpc.unary_unary_rpc_method_handler(
          servicer.UploadFile,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'CheckStatus': grpc.unary_unary_rpc_method_handler(
          servicer.CheckStatus,
          request_deserializer=client__pb2.Empty.FromString,
          response_serializer=client__pb2.Status.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'OperationHandler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
