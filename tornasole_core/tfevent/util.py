from .tensor_pb2 import TensorProto
from .tensor_shape_pb2 import TensorShapeProto
import numpy as np


_NP_DATATYPE_TO_PROTO_DATATYPE = {
    np.float16: "DT_FLOAT16",
    np.float32:"DT_FLOAT",
    np.float64:"DT_DOUBLE",
    #float64:"DT_DOUBLE",
    np.int32:"DT_INT32",
    np.int64:"DT_INT64",
    np.uint8:"DT_UINT8",
    np.uint16:"DT_UINT16",
    np.uint32:"DT_UINT32",
    np.uint64:"DT_UINT64",
    np.int8:"DT_INT8",
    np.int16:"DT_INT16",
    np.complex64:"DT_COMPLEX64",
    np.complex128:"DT_COMPLEX128",
    np.bool:"DT_BOOL"
}

def _get_proto_dtype(npdtype):
    if npdtype.kind == 'U':
        return (False, "DT_STRING")
    if npdtype == np.float64:
        return (True, "DT_DOUBLE")
    if npdtype == np.float32:
        return (True, "DT_FLOAT")
    if npdtype == np.int32:
        return (True, "DT_INT32")
    if npdtype == np.int64:
        return (True, "DT_INT64")
    return (True, _NP_DATATYPE_TO_PROTO_DATATYPE[npdtype])

def make_tensor_proto(nparray_data, tag):
    (isnum, dtype) = _get_proto_dtype(nparray_data.dtype)
    dimensions = [TensorShapeProto.Dim(size=d, name="{0}_{1}".format(tag, d)) for d in nparray_data.shape]
    tps = TensorShapeProto(dim=dimensions)
    if isnum:
        tensor_proto = TensorProto(dtype=dtype,
                                   tensor_content=nparray_data.tostring(),
                                   tensor_shape=TensorShapeProto(dim=dimensions))
    else:
        tensor_proto = TensorProto(tensor_shape=tps)
        for s in nparray_data:
            sb = bytes(s,encoding='utf-8')
            tensor_proto.string_val.append(sb)
    return tensor_proto