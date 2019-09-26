node {
  name: "ranking/feature"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 46
        }
      }
    }
  }
}
node {
  name: "ranking/training"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_BOOL
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
}
node {
  name: "ranking/label"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 1
        }
      }
    }
  }
}
node {
  name: "ranking/sorted_label"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 1
        }
      }
    }
  }
}
node {
  name: "ranking/qid"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 1
        }
      }
    }
  }
}
node {
  name: "ranking/Variable/initial_value"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
        }
        int_val: 0
      }
    }
  }
}
node {
  name: "ranking/Variable"
  op: "VariableV2"
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "ranking/Variable/Assign"
  op: "Assign"
  input: "ranking/Variable"
  input: "ranking/Variable/initial_value"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking/Variable"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "ranking/Variable/read"
  op: "Identity"
  input: "ranking/Variable"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking/Variable"
      }
    }
  }
}
node {
  name: "ranking/ExponentialDecay/initial_learning_rate"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0010000000474974513
      }
    }
  }
}
node {
  name: "ranking/ExponentialDecay/Cast/x"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
        }
        int_val: 1000
      }
    }
  }
}
node {
  name: "ranking/ExponentialDecay/Cast"
  op: "Cast"
  input: "ranking/ExponentialDecay/Cast/x"
  attr {
    key: "DstT"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "SrcT"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "Truncate"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/ExponentialDecay/Cast_1/x"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.8999999761581421
      }
    }
  }
}
node {
  name: "ranking/ExponentialDecay/Cast_2"
  op: "Cast"
  input: "ranking/Variable/read"
  attr {
    key: "DstT"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "SrcT"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "Truncate"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/ExponentialDecay/truediv"
  op: "RealDiv"
  input: "ranking/ExponentialDecay/Cast_2"
  input: "ranking/ExponentialDecay/Cast"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking/ExponentialDecay/Pow"
  op: "Pow"
  input: "ranking/ExponentialDecay/Cast_1/x"
  input: "ranking/ExponentialDecay/truediv"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking/ExponentialDecay"
  op: "Mul"
  input: "ranking/ExponentialDecay/initial_learning_rate"
  input: "ranking/ExponentialDecay/Pow"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking/batch_size"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/shape"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: ".\000\000\000\200\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/min"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: -0.1856953352689743
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/max"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.1856953352689743
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/RandomUniform"
  op: "RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/shape"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "seed"
    value {
      i: 87654321
    }
  }
  attr {
    key: "seed2"
    value {
      i: 0
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/sub"
  op: "Sub"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/max"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/mul"
  op: "Mul"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/sub"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform"
  op: "Add"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/mul"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 46
        }
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Initializer/random_uniform"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 128
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/bias"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
}
node {
  name: "ranking/dense_block/dense_block-dense_block_mode1-0/MatMul"
  op: "MatMul"
  input: "ranking/feature"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd"
  op: "BiasAdd"
  input: "ranking/dense_block/dense_block-dense_block_mode1-0/MatMul"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "ranking/dense_block/Relu"
  op: "Relu"
  input: "ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/shape"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "\200\000\000\000@\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/min"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: -0.1767766922712326
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/max"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.1767766922712326
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/RandomUniform"
  op: "RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/shape"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "seed"
    value {
      i: 87654321
    }
  }
  attr {
    key: "seed2"
    value {
      i: 2018
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/sub"
  op: "Sub"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/max"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/mul"
  op: "Mul"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/sub"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform"
  op: "Add"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/mul"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Initializer/random_uniform"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 64
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/bias"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
}
node {
  name: "ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul"
  op: "MatMul"
  input: "ranking/dense_block/Relu"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd"
  op: "BiasAdd"
  input: "ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "ranking/dense_block_1/Relu"
  op: "Relu"
  input: "ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/shape"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "@\000\000\000 \000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/min"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: -0.25
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/max"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.25
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/RandomUniform"
  op: "RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/shape"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "seed"
    value {
      i: 87654321
    }
  }
  attr {
    key: "seed2"
    value {
      i: 4036
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/sub"
  op: "Sub"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/max"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/mul"
  op: "Mul"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/RandomUniform"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/sub"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform"
  op: "Add"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/mul"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Initializer/random_uniform"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 32
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/bias"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
}
node {
  name: "ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul"
  op: "MatMul"
  input: "ranking/dense_block_1/Relu"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd"
  op: "BiasAdd"
  input: "ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "ranking/dense_block_2/Relu"
  op: "Relu"
  input: "ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/shape"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: " \000\000\000\001\000\000\000"
      }
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/min"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: -0.42640143632888794
      }
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/max"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.42640143632888794
      }
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/RandomUniform"
  op: "RandomUniform"
  input: "dense/kernel/Initializer/random_uniform/shape"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "seed"
    value {
      i: 87654321
    }
  }
  attr {
    key: "seed2"
    value {
      i: 2018
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/sub"
  op: "Sub"
  input: "dense/kernel/Initializer/random_uniform/max"
  input: "dense/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform/mul"
  op: "Mul"
  input: "dense/kernel/Initializer/random_uniform/RandomUniform"
  input: "dense/kernel/Initializer/random_uniform/sub"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/kernel/Initializer/random_uniform"
  op: "Add"
  input: "dense/kernel/Initializer/random_uniform/mul"
  input: "dense/kernel/Initializer/random_uniform/min"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/kernel"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/kernel/Assign"
  op: "Assign"
  input: "dense/kernel"
  input: "dense/kernel/Initializer/random_uniform"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/kernel/read"
  op: "Identity"
  input: "dense/kernel"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/bias/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 1
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense/bias"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/bias/Assign"
  op: "Assign"
  input: "dense/bias"
  input: "dense/bias/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/bias/read"
  op: "Identity"
  input: "dense/bias"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "ranking/dense/MatMul"
  op: "MatMul"
  input: "ranking/dense_block_2/Relu"
  input: "dense/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "ranking/dense/BiasAdd"
  op: "BiasAdd"
  input: "ranking/dense/MatMul"
  input: "dense/bias/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "ranking/score"
  op: "Identity"
  input: "ranking/dense/BiasAdd"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/zeros_like"
  op: "ZerosLike"
  input: "ranking/score"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/GreaterEqual"
  op: "GreaterEqual"
  input: "ranking/score"
  input: "logistic_loss/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/Select"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "ranking/score"
  input: "logistic_loss/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/Neg"
  op: "Neg"
  input: "ranking/score"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/Select_1"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "logistic_loss/Neg"
  input: "ranking/score"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/mul"
  op: "Mul"
  input: "ranking/score"
  input: "ranking/label"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/sub"
  op: "Sub"
  input: "logistic_loss/Select"
  input: "logistic_loss/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/Exp"
  op: "Exp"
  input: "logistic_loss/Select_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss/Log1p"
  op: "Log1p"
  input: "logistic_loss/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss"
  op: "Add"
  input: "logistic_loss/sub"
  input: "logistic_loss/Log1p"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "Const"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "\000\000\000\000\001\000\000\000"
      }
    }
  }
}
node {
  name: "Mean"
  op: "Mean"
  input: "logistic_loss"
  input: "Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "Shape"
  op: "Shape"
  input: "ranking/feature"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "strided_slice/stack"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 1
          }
        }
        int_val: 0
      }
    }
  }
}
node {
  name: "strided_slice/stack_1"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 1
          }
        }
        int_val: 1
      }
    }
  }
}
node {
  name: "strided_slice/stack_2"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 1
          }
        }
        int_val: 1
      }
    }
  }
}
node {
  name: "strided_slice"
  op: "StridedSlice"
  input: "Shape"
  input: "strided_slice/stack"
  input: "strided_slice/stack_1"
  input: "strided_slice/stack_2"
  attr {
    key: "Index"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "begin_mask"
    value {
      i: 0
    }
  }
  attr {
    key: "ellipsis_mask"
    value {
      i: 0
    }
  }
  attr {
    key: "end_mask"
    value {
      i: 0
    }
  }
  attr {
    key: "new_axis_mask"
    value {
      i: 0
    }
  }
  attr {
    key: "shrink_axis_mask"
    value {
      i: 1
    }
  }
}
node {
  name: "optimization/gradients/Shape"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
          }
        }
      }
    }
  }
}
node {
  name: "optimization/gradients/grad_ys_0"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 1.0
      }
    }
  }
}
node {
  name: "optimization/gradients/Fill"
  op: "Fill"
  input: "optimization/gradients/Shape"
  input: "optimization/gradients/grad_ys_0"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Reshape/shape"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "\001\000\000\000\001\000\000\000"
      }
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Reshape"
  op: "Reshape"
  input: "optimization/gradients/Fill"
  input: "optimization/gradients/Mean_grad/Reshape/shape"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Shape"
  op: "Shape"
  input: "logistic_loss"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Tile"
  op: "Tile"
  input: "optimization/gradients/Mean_grad/Reshape"
  input: "optimization/gradients/Mean_grad/Shape"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tmultiples"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Shape_2"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
          }
        }
      }
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Const"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 1
          }
        }
        int_val: 0
      }
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Prod"
  op: "Prod"
  input: "optimization/gradients/Mean_grad/Shape_1"
  input: "optimization/gradients/Mean_grad/Const"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Const_1"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 1
          }
        }
        int_val: 0
      }
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Prod_1"
  op: "Prod"
  input: "optimization/gradients/Mean_grad/Shape_2"
  input: "optimization/gradients/Mean_grad/Const_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Maximum/y"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
        }
        int_val: 1
      }
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Maximum"
  op: "Maximum"
  input: "optimization/gradients/Mean_grad/Prod_1"
  input: "optimization/gradients/Mean_grad/Maximum/y"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/floordiv"
  op: "FloorDiv"
  input: "optimization/gradients/Mean_grad/Prod"
  input: "optimization/gradients/Mean_grad/Maximum"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/Cast"
  op: "Cast"
  input: "optimization/gradients/Mean_grad/floordiv"
  attr {
    key: "DstT"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "SrcT"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "Truncate"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/Mean_grad/truediv"
  op: "RealDiv"
  input: "optimization/gradients/Mean_grad/Tile"
  input: "optimization/gradients/Mean_grad/Cast"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Shape"
  op: "Shape"
  input: "logistic_loss/sub"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss/Log1p"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization/gradients/logistic_loss_grad/Shape"
  input: "optimization/gradients/logistic_loss_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Sum"
  op: "Sum"
  input: "optimization/gradients/Mean_grad/truediv"
  input: "optimization/gradients/logistic_loss_grad/BroadcastGradientArgs"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Reshape"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss_grad/Sum"
  input: "optimization/gradients/logistic_loss_grad/Shape"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Sum_1"
  op: "Sum"
  input: "optimization/gradients/Mean_grad/truediv"
  input: "optimization/gradients/logistic_loss_grad/BroadcastGradientArgs:1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/Reshape_1"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss_grad/Sum_1"
  input: "optimization/gradients/logistic_loss_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/logistic_loss_grad/Reshape"
  input: "^optimization/gradients/logistic_loss_grad/Reshape_1"
}
node {
  name: "optimization/gradients/logistic_loss_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/logistic_loss_grad/Reshape"
  input: "^optimization/gradients/logistic_loss_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/logistic_loss_grad/Reshape_1"
  input: "^optimization/gradients/logistic_loss_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Shape"
  op: "Shape"
  input: "logistic_loss/Select"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization/gradients/logistic_loss/sub_grad/Shape"
  input: "optimization/gradients/logistic_loss/sub_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Sum"
  op: "Sum"
  input: "optimization/gradients/logistic_loss_grad/tuple/control_dependency"
  input: "optimization/gradients/logistic_loss/sub_grad/BroadcastGradientArgs"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Reshape"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss/sub_grad/Sum"
  input: "optimization/gradients/logistic_loss/sub_grad/Shape"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Sum_1"
  op: "Sum"
  input: "optimization/gradients/logistic_loss_grad/tuple/control_dependency"
  input: "optimization/gradients/logistic_loss/sub_grad/BroadcastGradientArgs:1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Neg"
  op: "Neg"
  input: "optimization/gradients/logistic_loss/sub_grad/Sum_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/Reshape_1"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss/sub_grad/Neg"
  input: "optimization/gradients/logistic_loss/sub_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/logistic_loss/sub_grad/Reshape"
  input: "^optimization/gradients/logistic_loss/sub_grad/Reshape_1"
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/sub_grad/Reshape"
  input: "^optimization/gradients/logistic_loss/sub_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/sub_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/sub_grad/Reshape_1"
  input: "^optimization/gradients/logistic_loss/sub_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/sub_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Log1p_grad/add/x"
  op: "Const"
  input: "^optimization/gradients/logistic_loss_grad/tuple/control_dependency_1"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 1.0
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Log1p_grad/add"
  op: "Add"
  input: "optimization/gradients/logistic_loss/Log1p_grad/add/x"
  input: "logistic_loss/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Log1p_grad/Reciprocal"
  op: "Reciprocal"
  input: "optimization/gradients/logistic_loss/Log1p_grad/add"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Log1p_grad/mul"
  op: "Mul"
  input: "optimization/gradients/logistic_loss_grad/tuple/control_dependency_1"
  input: "optimization/gradients/logistic_loss/Log1p_grad/Reciprocal"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/zeros_like"
  op: "ZerosLike"
  input: "ranking/score"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/Select"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency"
  input: "optimization/gradients/logistic_loss/Select_grad/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/Select_1"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "optimization/gradients/logistic_loss/Select_grad/zeros_like"
  input: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/logistic_loss/Select_grad/Select"
  input: "^optimization/gradients/logistic_loss/Select_grad/Select_1"
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/Select_grad/Select"
  input: "^optimization/gradients/logistic_loss/Select_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/Select_grad/Select_1"
  input: "^optimization/gradients/logistic_loss/Select_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_grad/Select_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Shape"
  op: "Shape"
  input: "ranking/score"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Shape_1"
  op: "Shape"
  input: "ranking/label"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "out_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization/gradients/logistic_loss/mul_grad/Shape"
  input: "optimization/gradients/logistic_loss/mul_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Mul"
  op: "Mul"
  input: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency_1"
  input: "ranking/label"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Sum"
  op: "Sum"
  input: "optimization/gradients/logistic_loss/mul_grad/Mul"
  input: "optimization/gradients/logistic_loss/mul_grad/BroadcastGradientArgs"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Reshape"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss/mul_grad/Sum"
  input: "optimization/gradients/logistic_loss/mul_grad/Shape"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Mul_1"
  op: "Mul"
  input: "ranking/score"
  input: "optimization/gradients/logistic_loss/sub_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Sum_1"
  op: "Sum"
  input: "optimization/gradients/logistic_loss/mul_grad/Mul_1"
  input: "optimization/gradients/logistic_loss/mul_grad/BroadcastGradientArgs:1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tidx"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "keep_dims"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/Reshape_1"
  op: "Reshape"
  input: "optimization/gradients/logistic_loss/mul_grad/Sum_1"
  input: "optimization/gradients/logistic_loss/mul_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "Tshape"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/logistic_loss/mul_grad/Reshape"
  input: "^optimization/gradients/logistic_loss/mul_grad/Reshape_1"
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/mul_grad/Reshape"
  input: "^optimization/gradients/logistic_loss/mul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/mul_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/mul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/mul_grad/Reshape_1"
  input: "^optimization/gradients/logistic_loss/mul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/mul_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Exp_grad/mul"
  op: "Mul"
  input: "optimization/gradients/logistic_loss/Log1p_grad/mul"
  input: "logistic_loss/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/zeros_like"
  op: "ZerosLike"
  input: "logistic_loss/Neg"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/Select"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "optimization/gradients/logistic_loss/Exp_grad/mul"
  input: "optimization/gradients/logistic_loss/Select_1_grad/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/Select_1"
  op: "Select"
  input: "logistic_loss/GreaterEqual"
  input: "optimization/gradients/logistic_loss/Select_1_grad/zeros_like"
  input: "optimization/gradients/logistic_loss/Exp_grad/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/logistic_loss/Select_1_grad/Select"
  input: "^optimization/gradients/logistic_loss/Select_1_grad/Select_1"
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/Select_1_grad/Select"
  input: "^optimization/gradients/logistic_loss/Select_1_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_1_grad/Select"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Select_1_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/logistic_loss/Select_1_grad/Select_1"
  input: "^optimization/gradients/logistic_loss/Select_1_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_1_grad/Select_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/logistic_loss/Neg_grad/Neg"
  op: "Neg"
  input: "optimization/gradients/logistic_loss/Select_1_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/AddN"
  op: "AddN"
  input: "optimization/gradients/logistic_loss/Select_grad/tuple/control_dependency"
  input: "optimization/gradients/logistic_loss/mul_grad/tuple/control_dependency"
  input: "optimization/gradients/logistic_loss/Select_1_grad/tuple/control_dependency_1"
  input: "optimization/gradients/logistic_loss/Neg_grad/Neg"
  attr {
    key: "N"
    value {
      i: 4
    }
  }
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/BiasAdd_grad/BiasAddGrad"
  op: "BiasAddGrad"
  input: "optimization/gradients/AddN"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/AddN"
  input: "^optimization/gradients/ranking/dense/BiasAdd_grad/BiasAddGrad"
}
node {
  name: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/AddN"
  input: "^optimization/gradients/ranking/dense/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/logistic_loss/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense/BiasAdd_grad/BiasAddGrad"
  input: "^optimization/gradients/ranking/dense/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense/BiasAdd_grad/BiasAddGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/MatMul_grad/MatMul"
  op: "MatMul"
  input: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/control_dependency"
  input: "dense/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/MatMul_grad/MatMul_1"
  op: "MatMul"
  input: "ranking/dense_block_2/Relu"
  input: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: true
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/MatMul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense/MatMul_grad/MatMul_1"
}
node {
  name: "optimization/gradients/ranking/dense/MatMul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense/MatMul_grad/MatMul"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense/MatMul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense/MatMul_grad/MatMul_1"
  input: "^optimization/gradients/ranking/dense/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense/MatMul_grad/MatMul_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/Relu_grad/ReluGrad"
  op: "ReluGrad"
  input: "optimization/gradients/ranking/dense/MatMul_grad/tuple/control_dependency"
  input: "ranking/dense_block_2/Relu"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/BiasAddGrad"
  op: "BiasAddGrad"
  input: "optimization/gradients/ranking/dense_block_2/Relu_grad/ReluGrad"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block_2/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/BiasAddGrad"
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_2/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_2/Relu_grad/ReluGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/BiasAddGrad"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/BiasAddGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul"
  op: "MatMul"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/control_dependency"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul_1"
  op: "MatMul"
  input: "ranking/dense_block_1/Relu"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: true
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul_1"
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul_1"
  input: "^optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/MatMul_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/Relu_grad/ReluGrad"
  op: "ReluGrad"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/control_dependency"
  input: "ranking/dense_block_1/Relu"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/BiasAddGrad"
  op: "BiasAddGrad"
  input: "optimization/gradients/ranking/dense_block_1/Relu_grad/ReluGrad"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block_1/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/BiasAddGrad"
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_1/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_1/Relu_grad/ReluGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/BiasAddGrad"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/BiasAddGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul"
  op: "MatMul"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/control_dependency"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul_1"
  op: "MatMul"
  input: "ranking/dense_block/Relu"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: true
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul_1"
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul_1"
  input: "^optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/MatMul_1"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/Relu_grad/ReluGrad"
  op: "ReluGrad"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/control_dependency"
  input: "ranking/dense_block/Relu"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/BiasAddGrad"
  op: "BiasAddGrad"
  input: "optimization/gradients/ranking/dense_block/Relu_grad/ReluGrad"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "data_format"
    value {
      s: "NHWC"
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/BiasAddGrad"
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block/Relu_grad/ReluGrad"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block/Relu_grad/ReluGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/BiasAddGrad"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/BiasAddGrad"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul"
  op: "MatMul"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/control_dependency"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/read"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: false
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul_1"
  op: "MatMul"
  input: "ranking/feature"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "transpose_a"
    value {
      b: true
    }
  }
  attr {
    key: "transpose_b"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul_1"
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul"
      }
    }
  }
}
node {
  name: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul_1"
  input: "^optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/group_deps"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/MatMul_1"
      }
    }
  }
}
node {
  name: "optimization/beta1_power/initial_value"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.9750000238418579
      }
    }
  }
}
node {
  name: "optimization/beta1_power"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "optimization/beta1_power/Assign"
  op: "Assign"
  input: "optimization/beta1_power"
  input: "optimization/beta1_power/initial_value"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/beta1_power/read"
  op: "Identity"
  input: "optimization/beta1_power"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "optimization/beta2_power/initial_value"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.9990000128746033
      }
    }
  }
}
node {
  name: "optimization/beta2_power"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "optimization/beta2_power/Assign"
  op: "Assign"
  input: "optimization/beta2_power"
  input: "optimization/beta2_power/initial_value"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/beta2_power/read"
  op: "Identity"
  input: "optimization/beta2_power"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: ".\000\000\000\200\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 46
        }
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: ".\000\000\000\200\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 46
        }
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 128
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 128
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "\200\000\000\000@\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "\200\000\000\000@\000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 128
        }
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 64
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 64
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "@\000\000\000 \000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
          dim {
            size: 2
          }
        }
        tensor_content: "@\000\000\000 \000\000\000"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros/Const"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros"
  op: "Fill"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros/shape_as_tensor"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros/Const"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "index_type"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 64
        }
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 32
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 32
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1/Assign"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1/read"
  op: "Identity"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
}
node {
  name: "dense/kernel/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 32
          }
          dim {
            size: 1
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense/kernel/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/kernel/Adam/Assign"
  op: "Assign"
  input: "dense/kernel/Adam"
  input: "dense/kernel/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/kernel/Adam/read"
  op: "Identity"
  input: "dense/kernel/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/kernel/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 32
          }
          dim {
            size: 1
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense/kernel/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 32
        }
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/kernel/Adam_1/Assign"
  op: "Assign"
  input: "dense/kernel/Adam_1"
  input: "dense/kernel/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/kernel/Adam_1/read"
  op: "Identity"
  input: "dense/kernel/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
}
node {
  name: "dense/bias/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 1
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense/bias/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/bias/Adam/Assign"
  op: "Assign"
  input: "dense/bias/Adam"
  input: "dense/bias/Adam/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/bias/Adam/read"
  op: "Identity"
  input: "dense/bias/Adam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "dense/bias/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
          dim {
            size: 1
          }
        }
        float_val: 0.0
      }
    }
  }
}
node {
  name: "dense/bias/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "container"
    value {
      s: ""
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: 1
        }
      }
    }
  }
  attr {
    key: "shared_name"
    value {
      s: ""
    }
  }
}
node {
  name: "dense/bias/Adam_1/Assign"
  op: "Assign"
  input: "dense/bias/Adam_1"
  input: "dense/bias/Adam_1/Initializer/zeros"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "dense/bias/Adam_1/read"
  op: "Identity"
  input: "dense/bias/Adam_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "optimization/Adam/beta1"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.9750000238418579
      }
    }
  }
}
node {
  name: "optimization/Adam/beta2"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 0.9990000128746033
      }
    }
  }
}
node {
  name: "optimization/Adam/epsilon"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_FLOAT
        tensor_shape {
        }
        float_val: 9.99999993922529e-09
      }
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/kernel/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/MatMul_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/bias/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-0/bias"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block/dense_block-dense_block_mode1-0/BiasAdd_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/kernel/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/MatMul_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/bias/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-1/bias"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block_1/dense_block-dense_block_mode1-1/BiasAdd_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/kernel/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/MatMul_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/bias/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_block/dense_block-dense_block_mode1-2/bias"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense_block_2/dense_block-dense_block_mode1-2/BiasAdd_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense/kernel/ApplyAdam"
  op: "ApplyAdam"
  input: "dense/kernel"
  input: "dense/kernel/Adam"
  input: "dense/kernel/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense/MatMul_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/update_dense/bias/ApplyAdam"
  op: "ApplyAdam"
  input: "dense/bias"
  input: "dense/bias/Adam"
  input: "dense/bias/Adam_1"
  input: "optimization/beta1_power/read"
  input: "optimization/beta2_power/read"
  input: "ranking/ExponentialDecay"
  input: "optimization/Adam/beta1"
  input: "optimization/Adam/beta2"
  input: "optimization/Adam/epsilon"
  input: "optimization/gradients/ranking/dense/BiasAdd_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "use_nesterov"
    value {
      b: false
    }
  }
}
node {
  name: "optimization/Adam/mul"
  op: "Mul"
  input: "optimization/beta1_power/read"
  input: "optimization/Adam/beta1"
  input: "^optimization/Adam/update_dense/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/kernel/ApplyAdam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "optimization/Adam/Assign"
  op: "Assign"
  input: "optimization/beta1_power"
  input: "optimization/Adam/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/Adam/mul_1"
  op: "Mul"
  input: "optimization/beta2_power/read"
  input: "optimization/Adam/beta2"
  input: "^optimization/Adam/update_dense/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/kernel/ApplyAdam"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
}
node {
  name: "optimization/Adam/Assign_1"
  op: "Assign"
  input: "optimization/beta2_power"
  input: "optimization/Adam/mul_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "optimization/Adam/update"
  op: "NoOp"
  input: "^optimization/Adam/Assign"
  input: "^optimization/Adam/Assign_1"
  input: "^optimization/Adam/update_dense/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-0/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-1/kernel/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/bias/ApplyAdam"
  input: "^optimization/Adam/update_dense_block/dense_block-dense_block_mode1-2/kernel/ApplyAdam"
}
node {
  name: "optimization/Adam/value"
  op: "Const"
  input: "^optimization/Adam/update"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking/Variable"
      }
    }
  }
  attr {
    key: "dtype"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_INT32
        tensor_shape {
        }
        int_val: 1
      }
    }
  }
}
node {
  name: "optimization/Adam"
  op: "AssignAdd"
  input: "ranking/Variable"
  input: "optimization/Adam/value"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking/Variable"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: false
    }
  }
}
node {
  name: "init"
  op: "NoOp"
  input: "^dense/bias/Adam/Assign"
  input: "^dense/bias/Adam_1/Assign"
  input: "^dense/bias/Assign"
  input: "^dense/kernel/Adam/Assign"
  input: "^dense/kernel/Adam_1/Assign"
  input: "^dense/kernel/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/bias/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/bias/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/bias/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/kernel/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-0/kernel/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/bias/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/bias/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/bias/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/kernel/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-1/kernel/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/bias/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/bias/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/bias/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/kernel/Adam/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1/Assign"
  input: "^dense_block/dense_block-dense_block_mode1-2/kernel/Assign"
  input: "^optimization/beta1_power/Assign"
  input: "^optimization/beta2_power/Assign"
  input: "^ranking/Variable/Assign"
}
node {
  name: "save/filename/input"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_STRING
        tensor_shape {
        }
        string_val: "model"
      }
    }
  }
}
node {
  name: "save/filename"
  op: "PlaceholderWithDefault"
  input: "save/filename/input"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
}
node {
  name: "save/Const"
  op: "PlaceholderWithDefault"
  input: "save/filename"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "shape"
    value {
      shape {
      }
    }
  }
}
node {
  name: "save/SaveV2/tensor_names"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_STRING
        tensor_shape {
          dim {
            size: 27
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
        string_val: "optimization/beta1_power"
        string_val: "optimization/beta2_power"
        string_val: "ranking/Variable"
      }
    }
  }
}
node {
  name: "save/SaveV2/shape_and_slices"
  op: "Const"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_STRING
        tensor_shape {
          dim {
            size: 27
          }
        }
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
      }
    }
  }
}
node {
  name: "save/SaveV2"
  op: "SaveV2"
  input: "save/Const"
  input: "save/SaveV2/tensor_names"
  input: "save/SaveV2/shape_and_slices"
  input: "dense/bias"
  input: "dense/bias/Adam"
  input: "dense/bias/Adam_1"
  input: "dense/kernel"
  input: "dense/kernel/Adam"
  input: "dense/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-0/bias"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-1/bias"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-2/bias"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  input: "optimization/beta1_power"
  input: "optimization/beta2_power"
  input: "ranking/Variable"
  attr {
    key: "dtypes"
    value {
      list {
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_INT32
      }
    }
  }
}
node {
  name: "save/control_dependency"
  op: "Identity"
  input: "save/Const"
  input: "^save/SaveV2"
  attr {
    key: "T"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@save/Const"
      }
    }
  }
}
node {
  name: "save/RestoreV2/tensor_names"
  op: "Const"
  device: "/device:CPU:0"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_STRING
        tensor_shape {
          dim {
            size: 27
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
        string_val: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
        string_val: "optimization/beta1_power"
        string_val: "optimization/beta2_power"
        string_val: "ranking/Variable"
      }
    }
  }
}
node {
  name: "save/RestoreV2/shape_and_slices"
  op: "Const"
  device: "/device:CPU:0"
  attr {
    key: "dtype"
    value {
      type: DT_STRING
    }
  }
  attr {
    key: "value"
    value {
      tensor {
        dtype: DT_STRING
        tensor_shape {
          dim {
            size: 27
          }
        }
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
        string_val: ""
      }
    }
  }
}
node {
  name: "save/RestoreV2"
  op: "RestoreV2"
  input: "save/Const"
  input: "save/RestoreV2/tensor_names"
  input: "save/RestoreV2/shape_and_slices"
  device: "/device:CPU:0"
  attr {
    key: "dtypes"
    value {
      list {
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_FLOAT
        type: DT_INT32
      }
    }
  }
}
node {
  name: "save/Assign"
  op: "Assign"
  input: "dense/bias"
  input: "save/RestoreV2"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_1"
  op: "Assign"
  input: "dense/bias/Adam"
  input: "save/RestoreV2:1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_2"
  op: "Assign"
  input: "dense/bias/Adam_1"
  input: "save/RestoreV2:2"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_3"
  op: "Assign"
  input: "dense/kernel"
  input: "save/RestoreV2:3"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_4"
  op: "Assign"
  input: "dense/kernel/Adam"
  input: "save/RestoreV2:4"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_5"
  op: "Assign"
  input: "dense/kernel/Adam_1"
  input: "save/RestoreV2:5"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_6"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias"
  input: "save/RestoreV2:6"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_7"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam"
  input: "save/RestoreV2:7"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_8"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/bias/Adam_1"
  input: "save/RestoreV2:8"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_9"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel"
  input: "save/RestoreV2:9"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_10"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam"
  input: "save/RestoreV2:10"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_11"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-0/kernel/Adam_1"
  input: "save/RestoreV2:11"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-0/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_12"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias"
  input: "save/RestoreV2:12"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_13"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam"
  input: "save/RestoreV2:13"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_14"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/bias/Adam_1"
  input: "save/RestoreV2:14"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_15"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel"
  input: "save/RestoreV2:15"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_16"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam"
  input: "save/RestoreV2:16"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_17"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-1/kernel/Adam_1"
  input: "save/RestoreV2:17"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-1/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_18"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias"
  input: "save/RestoreV2:18"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_19"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam"
  input: "save/RestoreV2:19"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_20"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/bias/Adam_1"
  input: "save/RestoreV2:20"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_21"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel"
  input: "save/RestoreV2:21"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_22"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam"
  input: "save/RestoreV2:22"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_23"
  op: "Assign"
  input: "dense_block/dense_block-dense_block_mode1-2/kernel/Adam_1"
  input: "save/RestoreV2:23"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_block/dense_block-dense_block_mode1-2/kernel"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_24"
  op: "Assign"
  input: "optimization/beta1_power"
  input: "save/RestoreV2:24"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_25"
  op: "Assign"
  input: "optimization/beta2_power"
  input: "save/RestoreV2:25"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense/bias"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/Assign_26"
  op: "Assign"
  input: "ranking/Variable"
  input: "save/RestoreV2:26"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking/Variable"
      }
    }
  }
  attr {
    key: "use_locking"
    value {
      b: true
    }
  }
  attr {
    key: "validate_shape"
    value {
      b: true
    }
  }
}
node {
  name: "save/restore_all"
  op: "NoOp"
  input: "^save/Assign"
  input: "^save/Assign_1"
  input: "^save/Assign_10"
  input: "^save/Assign_11"
  input: "^save/Assign_12"
  input: "^save/Assign_13"
  input: "^save/Assign_14"
  input: "^save/Assign_15"
  input: "^save/Assign_16"
  input: "^save/Assign_17"
  input: "^save/Assign_18"
  input: "^save/Assign_19"
  input: "^save/Assign_2"
  input: "^save/Assign_20"
  input: "^save/Assign_21"
  input: "^save/Assign_22"
  input: "^save/Assign_23"
  input: "^save/Assign_24"
  input: "^save/Assign_25"
  input: "^save/Assign_26"
  input: "^save/Assign_3"
  input: "^save/Assign_4"
  input: "^save/Assign_5"
  input: "^save/Assign_6"
  input: "^save/Assign_7"
  input: "^save/Assign_8"
  input: "^save/Assign_9"
}
versions {
  producer: 38
}
