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
        tensor_content: ".\000\000\000\001\000\000\000"
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
        float_val: -0.35729479789733887
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
        float_val: 0.35729479789733887
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
          size: 46
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
  input: "ranking/feature"
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
  input: "ranking/feature"
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
            size: 46
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
          size: 46
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
            size: 46
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
          size: 46
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
            size: 9
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
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
            size: 9
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
            size: 9
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
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
            size: 9
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
  input: "optimization/beta1_power"
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
  name: "save/Assign_7"
  op: "Assign"
  input: "optimization/beta2_power"
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
  name: "save/Assign_8"
  op: "Assign"
  input: "ranking/Variable"
  input: "save/RestoreV2:8"
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
  input: "^save/Assign_2"
  input: "^save/Assign_3"
  input: "^save/Assign_4"
  input: "^save/Assign_5"
  input: "^save/Assign_6"
  input: "^save/Assign_7"
  input: "^save/Assign_8"
}
node {
  name: "ranking_1/feature"
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
  name: "ranking_1/training"
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
  name: "ranking_1/label"
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
  name: "ranking_1/sorted_label"
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
  name: "ranking_1/qid"
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
  name: "ranking_1/Variable/initial_value"
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
  name: "ranking_1/Variable"
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
  name: "ranking_1/Variable/Assign"
  op: "Assign"
  input: "ranking_1/Variable"
  input: "ranking_1/Variable/initial_value"
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
        s: "loc:@ranking_1/Variable"
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
  name: "ranking_1/Variable/read"
  op: "Identity"
  input: "ranking_1/Variable"
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
        s: "loc:@ranking_1/Variable"
      }
    }
  }
}
node {
  name: "ranking_1/ExponentialDecay/initial_learning_rate"
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
  name: "ranking_1/ExponentialDecay/Cast/x"
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
  name: "ranking_1/ExponentialDecay/Cast"
  op: "Cast"
  input: "ranking_1/ExponentialDecay/Cast/x"
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
  name: "ranking_1/ExponentialDecay/Cast_1/x"
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
  name: "ranking_1/ExponentialDecay/Cast_2"
  op: "Cast"
  input: "ranking_1/Variable/read"
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
  name: "ranking_1/ExponentialDecay/truediv"
  op: "RealDiv"
  input: "ranking_1/ExponentialDecay/Cast_2"
  input: "ranking_1/ExponentialDecay/Cast"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking_1/ExponentialDecay/Pow"
  op: "Pow"
  input: "ranking_1/ExponentialDecay/Cast_1/x"
  input: "ranking_1/ExponentialDecay/truediv"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking_1/ExponentialDecay"
  op: "Mul"
  input: "ranking_1/ExponentialDecay/initial_learning_rate"
  input: "ranking_1/ExponentialDecay/Pow"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "ranking_1/batch_size"
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
  name: "dense_1/kernel/Initializer/random_uniform/shape"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
        tensor_content: ".\000\000\000\001\000\000\000"
      }
    }
  }
}
node {
  name: "dense_1/kernel/Initializer/random_uniform/min"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
        float_val: -0.35729479789733887
      }
    }
  }
}
node {
  name: "dense_1/kernel/Initializer/random_uniform/max"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
        float_val: 0.35729479789733887
      }
    }
  }
}
node {
  name: "dense_1/kernel/Initializer/random_uniform/RandomUniform"
  op: "RandomUniform"
  input: "dense_1/kernel/Initializer/random_uniform/shape"
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
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Initializer/random_uniform/sub"
  op: "Sub"
  input: "dense_1/kernel/Initializer/random_uniform/max"
  input: "dense_1/kernel/Initializer/random_uniform/min"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/kernel/Initializer/random_uniform/mul"
  op: "Mul"
  input: "dense_1/kernel/Initializer/random_uniform/RandomUniform"
  input: "dense_1/kernel/Initializer/random_uniform/sub"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/kernel/Initializer/random_uniform"
  op: "Add"
  input: "dense_1/kernel/Initializer/random_uniform/mul"
  input: "dense_1/kernel/Initializer/random_uniform/min"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/kernel"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Assign"
  op: "Assign"
  input: "dense_1/kernel"
  input: "dense_1/kernel/Initializer/random_uniform"
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
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/read"
  op: "Identity"
  input: "dense_1/kernel"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/bias/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Assign"
  op: "Assign"
  input: "dense_1/bias"
  input: "dense_1/bias/Initializer/zeros"
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
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/read"
  op: "Identity"
  input: "dense_1/bias"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "ranking/dense_1/MatMul"
  op: "MatMul"
  input: "ranking_1/feature"
  input: "dense_1/kernel/read"
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
  name: "ranking/dense_1/BiasAdd"
  op: "BiasAdd"
  input: "ranking/dense_1/MatMul"
  input: "dense_1/bias/read"
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
  name: "ranking/score_1"
  op: "Identity"
  input: "ranking/dense_1/BiasAdd"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/zeros_like"
  op: "ZerosLike"
  input: "ranking/score_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/GreaterEqual"
  op: "GreaterEqual"
  input: "ranking/score_1"
  input: "logistic_loss_1/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/Select"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "ranking/score_1"
  input: "logistic_loss_1/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/Neg"
  op: "Neg"
  input: "ranking/score_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/Select_1"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "logistic_loss_1/Neg"
  input: "ranking/score_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/mul"
  op: "Mul"
  input: "ranking/score_1"
  input: "ranking_1/label"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/sub"
  op: "Sub"
  input: "logistic_loss_1/Select"
  input: "logistic_loss_1/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/Exp"
  op: "Exp"
  input: "logistic_loss_1/Select_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1/Log1p"
  op: "Log1p"
  input: "logistic_loss_1/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "logistic_loss_1"
  op: "Add"
  input: "logistic_loss_1/sub"
  input: "logistic_loss_1/Log1p"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "Const_1"
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
  name: "Mean_1"
  op: "Mean"
  input: "logistic_loss_1"
  input: "Const_1"
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
  name: "Shape_1"
  op: "Shape"
  input: "ranking_1/feature"
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
  name: "strided_slice_1/stack"
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
  name: "strided_slice_1/stack_1"
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
  name: "strided_slice_1/stack_2"
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
  name: "strided_slice_1"
  op: "StridedSlice"
  input: "Shape_1"
  input: "strided_slice_1/stack"
  input: "strided_slice_1/stack_1"
  input: "strided_slice_1/stack_2"
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
  name: "optimization_1/gradients/Shape"
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
  name: "optimization_1/gradients/grad_ys_0"
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
  name: "optimization_1/gradients/Fill"
  op: "Fill"
  input: "optimization_1/gradients/Shape"
  input: "optimization_1/gradients/grad_ys_0"
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
  name: "optimization_1/gradients/Mean_1_grad/Reshape/shape"
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
  name: "optimization_1/gradients/Mean_1_grad/Reshape"
  op: "Reshape"
  input: "optimization_1/gradients/Fill"
  input: "optimization_1/gradients/Mean_1_grad/Reshape/shape"
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
  name: "optimization_1/gradients/Mean_1_grad/Shape"
  op: "Shape"
  input: "logistic_loss_1"
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
  name: "optimization_1/gradients/Mean_1_grad/Tile"
  op: "Tile"
  input: "optimization_1/gradients/Mean_1_grad/Reshape"
  input: "optimization_1/gradients/Mean_1_grad/Shape"
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
  name: "optimization_1/gradients/Mean_1_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss_1"
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
  name: "optimization_1/gradients/Mean_1_grad/Shape_2"
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
  name: "optimization_1/gradients/Mean_1_grad/Const"
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
  name: "optimization_1/gradients/Mean_1_grad/Prod"
  op: "Prod"
  input: "optimization_1/gradients/Mean_1_grad/Shape_1"
  input: "optimization_1/gradients/Mean_1_grad/Const"
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
  name: "optimization_1/gradients/Mean_1_grad/Const_1"
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
  name: "optimization_1/gradients/Mean_1_grad/Prod_1"
  op: "Prod"
  input: "optimization_1/gradients/Mean_1_grad/Shape_2"
  input: "optimization_1/gradients/Mean_1_grad/Const_1"
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
  name: "optimization_1/gradients/Mean_1_grad/Maximum/y"
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
  name: "optimization_1/gradients/Mean_1_grad/Maximum"
  op: "Maximum"
  input: "optimization_1/gradients/Mean_1_grad/Prod_1"
  input: "optimization_1/gradients/Mean_1_grad/Maximum/y"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization_1/gradients/Mean_1_grad/floordiv"
  op: "FloorDiv"
  input: "optimization_1/gradients/Mean_1_grad/Prod"
  input: "optimization_1/gradients/Mean_1_grad/Maximum"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization_1/gradients/Mean_1_grad/Cast"
  op: "Cast"
  input: "optimization_1/gradients/Mean_1_grad/floordiv"
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
  name: "optimization_1/gradients/Mean_1_grad/truediv"
  op: "RealDiv"
  input: "optimization_1/gradients/Mean_1_grad/Tile"
  input: "optimization_1/gradients/Mean_1_grad/Cast"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1_grad/Shape"
  op: "Shape"
  input: "logistic_loss_1/sub"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss_1/Log1p"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization_1/gradients/logistic_loss_1_grad/Shape"
  input: "optimization_1/gradients/logistic_loss_1_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1_grad/Sum"
  op: "Sum"
  input: "optimization_1/gradients/Mean_1_grad/truediv"
  input: "optimization_1/gradients/logistic_loss_1_grad/BroadcastGradientArgs"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/Reshape"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1_grad/Sum"
  input: "optimization_1/gradients/logistic_loss_1_grad/Shape"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/Sum_1"
  op: "Sum"
  input: "optimization_1/gradients/Mean_1_grad/truediv"
  input: "optimization_1/gradients/logistic_loss_1_grad/BroadcastGradientArgs:1"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/Reshape_1"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1_grad/Sum_1"
  input: "optimization_1/gradients/logistic_loss_1_grad/Shape_1"
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
  name: "optimization_1/gradients/logistic_loss_1_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/logistic_loss_1_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1_grad/Reshape_1"
}
node {
  name: "optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1_grad/Reshape_1"
  input: "^optimization_1/gradients/logistic_loss_1_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape"
  op: "Shape"
  input: "logistic_loss_1/Select"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape_1"
  op: "Shape"
  input: "logistic_loss_1/mul"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Sum"
  op: "Sum"
  input: "optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/BroadcastGradientArgs"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Reshape"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Sum"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Sum_1"
  op: "Sum"
  input: "optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/BroadcastGradientArgs:1"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Neg"
  op: "Neg"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Sum_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/Reshape_1"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Neg"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Shape_1"
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
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/logistic_loss_1/sub_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1/sub_grad/Reshape_1"
}
node {
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1/sub_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/sub_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/Reshape_1"
  input: "^optimization_1/gradients/logistic_loss_1/sub_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/sub_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Log1p_grad/add/x"
  op: "Const"
  input: "^optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency_1"
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
  name: "optimization_1/gradients/logistic_loss_1/Log1p_grad/add"
  op: "Add"
  input: "optimization_1/gradients/logistic_loss_1/Log1p_grad/add/x"
  input: "logistic_loss_1/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Log1p_grad/Reciprocal"
  op: "Reciprocal"
  input: "optimization_1/gradients/logistic_loss_1/Log1p_grad/add"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Log1p_grad/mul"
  op: "Mul"
  input: "optimization_1/gradients/logistic_loss_1_grad/tuple/control_dependency_1"
  input: "optimization_1/gradients/logistic_loss_1/Log1p_grad/Reciprocal"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/zeros_like"
  op: "ZerosLike"
  input: "ranking/score_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/Select"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency"
  input: "optimization_1/gradients/logistic_loss_1/Select_grad/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/Select_1"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "optimization_1/gradients/logistic_loss_1/Select_grad/zeros_like"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/logistic_loss_1/Select_grad/Select"
  input: "^optimization_1/gradients/logistic_loss_1/Select_grad/Select_1"
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/Select_grad/Select"
  input: "^optimization_1/gradients/logistic_loss_1/Select_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/Select_grad/Select_1"
  input: "^optimization_1/gradients/logistic_loss_1/Select_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_grad/Select_1"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape"
  op: "Shape"
  input: "ranking/score_1"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape_1"
  op: "Shape"
  input: "ranking_1/label"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/BroadcastGradientArgs"
  op: "BroadcastGradientArgs"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape_1"
  attr {
    key: "T"
    value {
      type: DT_INT32
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Mul"
  op: "Mul"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency_1"
  input: "ranking_1/label"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Sum"
  op: "Sum"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Mul"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/BroadcastGradientArgs"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Reshape"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Sum"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Mul_1"
  op: "Mul"
  input: "ranking/score_1"
  input: "optimization_1/gradients/logistic_loss_1/sub_grad/tuple/control_dependency_1"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Sum_1"
  op: "Sum"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Mul_1"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/BroadcastGradientArgs:1"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/Reshape_1"
  op: "Reshape"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Sum_1"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Shape_1"
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
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/logistic_loss_1/mul_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1/mul_grad/Reshape_1"
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Reshape"
  input: "^optimization_1/gradients/logistic_loss_1/mul_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/mul_grad/Reshape"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/mul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/Reshape_1"
  input: "^optimization_1/gradients/logistic_loss_1/mul_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/mul_grad/Reshape_1"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Exp_grad/mul"
  op: "Mul"
  input: "optimization_1/gradients/logistic_loss_1/Log1p_grad/mul"
  input: "logistic_loss_1/Exp"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/zeros_like"
  op: "ZerosLike"
  input: "logistic_loss_1/Neg"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/Select"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "optimization_1/gradients/logistic_loss_1/Exp_grad/mul"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/zeros_like"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/Select_1"
  op: "Select"
  input: "logistic_loss_1/GreaterEqual"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/zeros_like"
  input: "optimization_1/gradients/logistic_loss_1/Exp_grad/mul"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/logistic_loss_1/Select_1_grad/Select"
  input: "^optimization_1/gradients/logistic_loss_1/Select_1_grad/Select_1"
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/Select"
  input: "^optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_1_grad/Select"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/Select_1"
  input: "^optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_1_grad/Select_1"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/logistic_loss_1/Neg_grad/Neg"
  op: "Neg"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/control_dependency"
  attr {
    key: "T"
    value {
      type: DT_FLOAT
    }
  }
}
node {
  name: "optimization_1/gradients/AddN"
  op: "AddN"
  input: "optimization_1/gradients/logistic_loss_1/Select_grad/tuple/control_dependency"
  input: "optimization_1/gradients/logistic_loss_1/mul_grad/tuple/control_dependency"
  input: "optimization_1/gradients/logistic_loss_1/Select_1_grad/tuple/control_dependency_1"
  input: "optimization_1/gradients/logistic_loss_1/Neg_grad/Neg"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/BiasAddGrad"
  op: "BiasAddGrad"
  input: "optimization_1/gradients/AddN"
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
  name: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/AddN"
  input: "^optimization_1/gradients/ranking/dense_1/BiasAdd_grad/BiasAddGrad"
}
node {
  name: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/AddN"
  input: "^optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/logistic_loss_1/Select_grad/Select"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/BiasAddGrad"
  input: "^optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/ranking/dense_1/BiasAdd_grad/BiasAddGrad"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul"
  op: "MatMul"
  input: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/control_dependency"
  input: "dense_1/kernel/read"
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
  name: "optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul_1"
  op: "MatMul"
  input: "ranking_1/feature"
  input: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/control_dependency"
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
  name: "optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/group_deps"
  op: "NoOp"
  input: "^optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul"
  input: "^optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul_1"
}
node {
  name: "optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/control_dependency"
  op: "Identity"
  input: "optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul"
  input: "^optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul"
      }
    }
  }
}
node {
  name: "optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/control_dependency_1"
  op: "Identity"
  input: "optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul_1"
  input: "^optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/group_deps"
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
        s: "loc:@optimization_1/gradients/ranking/dense_1/MatMul_grad/MatMul_1"
      }
    }
  }
}
node {
  name: "optimization_1/beta1_power/initial_value"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta1_power"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta1_power/Assign"
  op: "Assign"
  input: "optimization_1/beta1_power"
  input: "optimization_1/beta1_power/initial_value"
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
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta1_power/read"
  op: "Identity"
  input: "optimization_1/beta1_power"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "optimization_1/beta2_power/initial_value"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta2_power"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta2_power/Assign"
  op: "Assign"
  input: "optimization_1/beta2_power"
  input: "optimization_1/beta2_power/initial_value"
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
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/beta2_power/read"
  op: "Identity"
  input: "optimization_1/beta2_power"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "dense_1/kernel/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
            size: 46
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
  name: "dense_1/kernel/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Adam/Assign"
  op: "Assign"
  input: "dense_1/kernel/Adam"
  input: "dense_1/kernel/Adam/Initializer/zeros"
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
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Adam/read"
  op: "Identity"
  input: "dense_1/kernel/Adam"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/kernel/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
            size: 46
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
  name: "dense_1/kernel/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Adam_1/Assign"
  op: "Assign"
  input: "dense_1/kernel/Adam_1"
  input: "dense_1/kernel/Adam_1/Initializer/zeros"
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
        s: "loc:@dense_1/kernel"
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
  name: "dense_1/kernel/Adam_1/read"
  op: "Identity"
  input: "dense_1/kernel/Adam_1"
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
        s: "loc:@dense_1/kernel"
      }
    }
  }
}
node {
  name: "dense_1/bias/Adam/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam/Assign"
  op: "Assign"
  input: "dense_1/bias/Adam"
  input: "dense_1/bias/Adam/Initializer/zeros"
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
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam/read"
  op: "Identity"
  input: "dense_1/bias/Adam"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "dense_1/bias/Adam_1/Initializer/zeros"
  op: "Const"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam_1"
  op: "VariableV2"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam_1/Assign"
  op: "Assign"
  input: "dense_1/bias/Adam_1"
  input: "dense_1/bias/Adam_1/Initializer/zeros"
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
        s: "loc:@dense_1/bias"
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
  name: "dense_1/bias/Adam_1/read"
  op: "Identity"
  input: "dense_1/bias/Adam_1"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "optimization_1/Adam/beta1"
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
  name: "optimization_1/Adam/beta2"
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
  name: "optimization_1/Adam/epsilon"
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
  name: "optimization_1/Adam/update_dense_1/kernel/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_1/kernel"
  input: "dense_1/kernel/Adam"
  input: "dense_1/kernel/Adam_1"
  input: "optimization_1/beta1_power/read"
  input: "optimization_1/beta2_power/read"
  input: "ranking_1/ExponentialDecay"
  input: "optimization_1/Adam/beta1"
  input: "optimization_1/Adam/beta2"
  input: "optimization_1/Adam/epsilon"
  input: "optimization_1/gradients/ranking/dense_1/MatMul_grad/tuple/control_dependency_1"
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
        s: "loc:@dense_1/kernel"
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
  name: "optimization_1/Adam/update_dense_1/bias/ApplyAdam"
  op: "ApplyAdam"
  input: "dense_1/bias"
  input: "dense_1/bias/Adam"
  input: "dense_1/bias/Adam_1"
  input: "optimization_1/beta1_power/read"
  input: "optimization_1/beta2_power/read"
  input: "ranking_1/ExponentialDecay"
  input: "optimization_1/Adam/beta1"
  input: "optimization_1/Adam/beta2"
  input: "optimization_1/Adam/epsilon"
  input: "optimization_1/gradients/ranking/dense_1/BiasAdd_grad/tuple/control_dependency_1"
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
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/Adam/mul"
  op: "Mul"
  input: "optimization_1/beta1_power/read"
  input: "optimization_1/Adam/beta1"
  input: "^optimization_1/Adam/update_dense_1/bias/ApplyAdam"
  input: "^optimization_1/Adam/update_dense_1/kernel/ApplyAdam"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "optimization_1/Adam/Assign"
  op: "Assign"
  input: "optimization_1/beta1_power"
  input: "optimization_1/Adam/mul"
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
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/Adam/mul_1"
  op: "Mul"
  input: "optimization_1/beta2_power/read"
  input: "optimization_1/Adam/beta2"
  input: "^optimization_1/Adam/update_dense_1/bias/ApplyAdam"
  input: "^optimization_1/Adam/update_dense_1/kernel/ApplyAdam"
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
        s: "loc:@dense_1/bias"
      }
    }
  }
}
node {
  name: "optimization_1/Adam/Assign_1"
  op: "Assign"
  input: "optimization_1/beta2_power"
  input: "optimization_1/Adam/mul_1"
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
        s: "loc:@dense_1/bias"
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
  name: "optimization_1/Adam/update"
  op: "NoOp"
  input: "^optimization_1/Adam/Assign"
  input: "^optimization_1/Adam/Assign_1"
  input: "^optimization_1/Adam/update_dense_1/bias/ApplyAdam"
  input: "^optimization_1/Adam/update_dense_1/kernel/ApplyAdam"
}
node {
  name: "optimization_1/Adam/value"
  op: "Const"
  input: "^optimization_1/Adam/update"
  attr {
    key: "_class"
    value {
      list {
        s: "loc:@ranking_1/Variable"
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
  name: "optimization_1/Adam"
  op: "AssignAdd"
  input: "ranking_1/Variable"
  input: "optimization_1/Adam/value"
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
        s: "loc:@ranking_1/Variable"
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
  name: "init_1"
  op: "NoOp"
  input: "^dense/bias/Adam/Assign"
  input: "^dense/bias/Adam_1/Assign"
  input: "^dense/bias/Assign"
  input: "^dense/kernel/Adam/Assign"
  input: "^dense/kernel/Adam_1/Assign"
  input: "^dense/kernel/Assign"
  input: "^dense_1/bias/Adam/Assign"
  input: "^dense_1/bias/Adam_1/Assign"
  input: "^dense_1/bias/Assign"
  input: "^dense_1/kernel/Adam/Assign"
  input: "^dense_1/kernel/Adam_1/Assign"
  input: "^dense_1/kernel/Assign"
  input: "^optimization/beta1_power/Assign"
  input: "^optimization/beta2_power/Assign"
  input: "^optimization_1/beta1_power/Assign"
  input: "^optimization_1/beta2_power/Assign"
  input: "^ranking/Variable/Assign"
  input: "^ranking_1/Variable/Assign"
}
node {
  name: "save_1/filename/input"
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
  name: "save_1/filename"
  op: "PlaceholderWithDefault"
  input: "save_1/filename/input"
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
  name: "save_1/Const"
  op: "PlaceholderWithDefault"
  input: "save_1/filename"
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
  name: "save_1/SaveV2/tensor_names"
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
            size: 18
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
        string_val: "dense_1/bias"
        string_val: "dense_1/bias/Adam"
        string_val: "dense_1/bias/Adam_1"
        string_val: "dense_1/kernel"
        string_val: "dense_1/kernel/Adam"
        string_val: "dense_1/kernel/Adam_1"
        string_val: "optimization/beta1_power"
        string_val: "optimization/beta2_power"
        string_val: "optimization_1/beta1_power"
        string_val: "optimization_1/beta2_power"
        string_val: "ranking/Variable"
        string_val: "ranking_1/Variable"
      }
    }
  }
}
node {
  name: "save_1/SaveV2/shape_and_slices"
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
            size: 18
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
      }
    }
  }
}
node {
  name: "save_1/SaveV2"
  op: "SaveV2"
  input: "save_1/Const"
  input: "save_1/SaveV2/tensor_names"
  input: "save_1/SaveV2/shape_and_slices"
  input: "dense/bias"
  input: "dense/bias/Adam"
  input: "dense/bias/Adam_1"
  input: "dense/kernel"
  input: "dense/kernel/Adam"
  input: "dense/kernel/Adam_1"
  input: "dense_1/bias"
  input: "dense_1/bias/Adam"
  input: "dense_1/bias/Adam_1"
  input: "dense_1/kernel"
  input: "dense_1/kernel/Adam"
  input: "dense_1/kernel/Adam_1"
  input: "optimization/beta1_power"
  input: "optimization/beta2_power"
  input: "optimization_1/beta1_power"
  input: "optimization_1/beta2_power"
  input: "ranking/Variable"
  input: "ranking_1/Variable"
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
        type: DT_INT32
        type: DT_INT32
      }
    }
  }
}
node {
  name: "save_1/control_dependency"
  op: "Identity"
  input: "save_1/Const"
  input: "^save_1/SaveV2"
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
        s: "loc:@save_1/Const"
      }
    }
  }
}
node {
  name: "save_1/RestoreV2/tensor_names"
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
            size: 18
          }
        }
        string_val: "dense/bias"
        string_val: "dense/bias/Adam"
        string_val: "dense/bias/Adam_1"
        string_val: "dense/kernel"
        string_val: "dense/kernel/Adam"
        string_val: "dense/kernel/Adam_1"
        string_val: "dense_1/bias"
        string_val: "dense_1/bias/Adam"
        string_val: "dense_1/bias/Adam_1"
        string_val: "dense_1/kernel"
        string_val: "dense_1/kernel/Adam"
        string_val: "dense_1/kernel/Adam_1"
        string_val: "optimization/beta1_power"
        string_val: "optimization/beta2_power"
        string_val: "optimization_1/beta1_power"
        string_val: "optimization_1/beta2_power"
        string_val: "ranking/Variable"
        string_val: "ranking_1/Variable"
      }
    }
  }
}
node {
  name: "save_1/RestoreV2/shape_and_slices"
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
            size: 18
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
      }
    }
  }
}
node {
  name: "save_1/RestoreV2"
  op: "RestoreV2"
  input: "save_1/Const"
  input: "save_1/RestoreV2/tensor_names"
  input: "save_1/RestoreV2/shape_and_slices"
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
        type: DT_INT32
        type: DT_INT32
      }
    }
  }
}
node {
  name: "save_1/Assign"
  op: "Assign"
  input: "dense/bias"
  input: "save_1/RestoreV2"
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
  name: "save_1/Assign_1"
  op: "Assign"
  input: "dense/bias/Adam"
  input: "save_1/RestoreV2:1"
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
  name: "save_1/Assign_2"
  op: "Assign"
  input: "dense/bias/Adam_1"
  input: "save_1/RestoreV2:2"
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
  name: "save_1/Assign_3"
  op: "Assign"
  input: "dense/kernel"
  input: "save_1/RestoreV2:3"
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
  name: "save_1/Assign_4"
  op: "Assign"
  input: "dense/kernel/Adam"
  input: "save_1/RestoreV2:4"
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
  name: "save_1/Assign_5"
  op: "Assign"
  input: "dense/kernel/Adam_1"
  input: "save_1/RestoreV2:5"
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
  name: "save_1/Assign_6"
  op: "Assign"
  input: "dense_1/bias"
  input: "save_1/RestoreV2:6"
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
        s: "loc:@dense_1/bias"
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
  name: "save_1/Assign_7"
  op: "Assign"
  input: "dense_1/bias/Adam"
  input: "save_1/RestoreV2:7"
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
        s: "loc:@dense_1/bias"
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
  name: "save_1/Assign_8"
  op: "Assign"
  input: "dense_1/bias/Adam_1"
  input: "save_1/RestoreV2:8"
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
        s: "loc:@dense_1/bias"
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
  name: "save_1/Assign_9"
  op: "Assign"
  input: "dense_1/kernel"
  input: "save_1/RestoreV2:9"
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
        s: "loc:@dense_1/kernel"
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
  name: "save_1/Assign_10"
  op: "Assign"
  input: "dense_1/kernel/Adam"
  input: "save_1/RestoreV2:10"
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
        s: "loc:@dense_1/kernel"
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
  name: "save_1/Assign_11"
  op: "Assign"
  input: "dense_1/kernel/Adam_1"
  input: "save_1/RestoreV2:11"
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
        s: "loc:@dense_1/kernel"
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
  name: "save_1/Assign_12"
  op: "Assign"
  input: "optimization/beta1_power"
  input: "save_1/RestoreV2:12"
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
  name: "save_1/Assign_13"
  op: "Assign"
  input: "optimization/beta2_power"
  input: "save_1/RestoreV2:13"
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
  name: "save_1/Assign_14"
  op: "Assign"
  input: "optimization_1/beta1_power"
  input: "save_1/RestoreV2:14"
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
        s: "loc:@dense_1/bias"
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
  name: "save_1/Assign_15"
  op: "Assign"
  input: "optimization_1/beta2_power"
  input: "save_1/RestoreV2:15"
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
        s: "loc:@dense_1/bias"
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
  name: "save_1/Assign_16"
  op: "Assign"
  input: "ranking/Variable"
  input: "save_1/RestoreV2:16"
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
  name: "save_1/Assign_17"
  op: "Assign"
  input: "ranking_1/Variable"
  input: "save_1/RestoreV2:17"
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
        s: "loc:@ranking_1/Variable"
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
  name: "save_1/restore_all"
  op: "NoOp"
  input: "^save_1/Assign"
  input: "^save_1/Assign_1"
  input: "^save_1/Assign_10"
  input: "^save_1/Assign_11"
  input: "^save_1/Assign_12"
  input: "^save_1/Assign_13"
  input: "^save_1/Assign_14"
  input: "^save_1/Assign_15"
  input: "^save_1/Assign_16"
  input: "^save_1/Assign_17"
  input: "^save_1/Assign_2"
  input: "^save_1/Assign_3"
  input: "^save_1/Assign_4"
  input: "^save_1/Assign_5"
  input: "^save_1/Assign_6"
  input: "^save_1/Assign_7"
  input: "^save_1/Assign_8"
  input: "^save_1/Assign_9"
}
versions {
  producer: 38
}
