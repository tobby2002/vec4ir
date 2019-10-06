
import os, sys
import numpy as np

import utils
from model import LogisticRegression, DNN, RankNet, LambdaRank
from prepare_data import label_file_pat, group_file_pat, feature_file_pat

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config


def load_data(type):

    labels = np.load(label_file_pat % type)
    qids = np.load(group_file_pat % type)
    features = np.load(feature_file_pat%type)

    X = {
        "feature": features,
        "label": labels,
        "qid": qids
    }
    return X


utils._makedirs("./logs")
logger = utils._get_logger("./logs", "tf-%s.log" % utils._timestamp())

params_common = {
    # you might have to tune the batch size to get ranknet and lambdarank working
    # keep in mind the followings:
    # 1. batch size should be large enough to ensure there are samples of different
    # relevance labels from the same group, especially when you use "sample" as "batch_sampling_method"
    # this ensure the gradients are nonzeros and stable across batches,
    # which is important for pairwise method, e.g., ranknet and lambdarank
    # 2. batch size should not be very large since the lambda_ij matrix in ranknet and lambdarank
    # (which are of size batch_size x batch_size) will consume large memory space
    "batch_size": 128,
    # "epoch": 50,
    "epoch": 5,
    "feature_dim": 46,

    "batch_sampling_method": "sample",
    "shuffle": True,

    "optimizer_type": "adam",
    "init_lr": 0.001,
    "beta1": 0.975,
    "beta2": 0.999,
    "decay_steps": 1000,
    "decay_rate": 0.9,
    "schedule_decay": 0.004,
    "random_seed": 2018,
    "eval_every_num_update": 100,
}


def train_lr():
    params = {
        "offline_model_dir": PROJECT_ROOT + "/lr/weights/lr",
    }
    params.update(params_common)

    X_train, X_valid = load_data("train"), load_data("vali")

    model = LogisticRegression("ranking", params, logger)
    model.fit(X_train, validation_data=X_valid)
    model.save_session()
    return model


def train_dnn():
    params = {
        "offline_model_dir": PROJECT_ROOT + "/ltr/weights/dnn",

        # deep part score fn
        "fc_type": "fc",
        "fc_dim": 32,
        "fc_dropout": 0.,
    }
    params.update(params_common)

    X_train, X_valid = load_data("train"), load_data("vali")

    model = DNN("ranking", params, logger)
    model.fit(X_train, validation_data=X_valid)
    model.save_session()
    return model



def train_ranknet():
    params = {
        "offline_model_dir": PROJECT_ROOT + "/ltr/weights/ranknet",

        # deep part score fn
        "fc_type": "fc",
        "fc_dim": 32,
        "fc_dropout": 0.,

        # ranknet param
        "factorization": True,
        "sigma": 1.,
    }
    params.update(params_common)

    X_train, X_valid = load_data("train"), load_data("vali")

    model = RankNet("ranking", params, logger)
    model.fit(X_train, validation_data=X_valid)
    model.save_session()


def train_lambdarank():
    params = {
        "offline_model_dir": PROJECT_ROOT + "/ltr/weights/lambdarank",

        # deep part score fn
        "fc_type": "fc",
        "fc_dim": 32,
        "fc_dropout": 0.,

        # lambdarank param
        "sigma": 1.,
    }
    params.update(params_common)

    X_train, X_valid = load_data("train"), load_data("vali")

    model = LambdaRank("ranking", params, logger)
    model.fit(X_train, validation_data=X_valid)
    model.save_session()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "lr":
            train_lr()
        elif sys.argv[1] == "dnn":
            train_dnn()
        elif sys.argv[1] == "ranknet":
            train_ranknet()
        elif sys.argv[1] == "lambdarank":
            train_lambdarank()
    else:
        train_lr()

def restore_dnn(model):
    if not model:
        params = {
            "offline_model_dir": PROJECT_ROOT + "/ltr/weights/dnn",

            # deep part score fn
            "fc_type": "fc",
            "fc_dim": 32,
            "fc_dropout": 0.,
        }
        params.update(params_common)
        model = DNN("ranking", params, logger, training=False)
    model.restore_session()
    return model

def restore_lr(model):
    if not model:
        params = {
            "offline_model_dir": PROJECT_ROOT + "/lr/weights/dnn",

            # deep part score fn
            "fc_type": "fc",
            "fc_dim": 32,
            "fc_dropout": 0.,
        }
        params.update(params_common)
        model = LogisticRegression("ranking", params, logger, training=False)
    model.restore_session()
    return model


def predict_dnn(model):
    X_test = load_data("test")
    return model.predict(X_test)


def predict_lr(model):
    X_test = load_data("test")
    return model.predict(X_test)

if __name__ == "__main__":
    # main()

    # train_dnn()
    # model = train_dnn()
    #
    # model = None
    # model = restore_dnn(model)
    # y_pred = predict_dnn(model)
    # print(y_pred)

    train_lr()
    model = train_lr()

    # model = None
    model = restore_dnn(model)
    y_pred = predict_dnn(model)
    print(y_pred)
