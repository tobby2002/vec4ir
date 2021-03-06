import os, sys
import numpy as np

try:
    from models import LogisticRegression, DNN, RankNet, LambdaRank
    from preparedata import label_file_pat_by_id, group_file_pat_by_id, feature_file_pat_by_id, convert_by_id
except:
    from .models import LogisticRegression, DNN, RankNet, LambdaRank
    from .preparedata import label_file_pat_by_id, group_file_pat_by_id, feature_file_pat_by_id, convert_by_id

from util import logmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

class LtrManager():

    def __init__(self):
        print('init')
        self.logger = logmanager.logger('ltr', 'train')
        self.params_common = {
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
            "epoch": 2,
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

    def load_data_by_id(self, type, cid):

        labels = np.load(label_file_pat_by_id % (cid, type))
        qids = np.load(group_file_pat_by_id % (cid, type))
        features = np.load(feature_file_pat_by_id % (cid, type))

        X = {
            "feature": features,
            "label": labels,
            "qid": qids
        }
        return X

    def train_lr(self, cid):
        params = {
            "offline_model_dir": PROJECT_ROOT+"/ltr/weights/lr",
        }
        params.update(self.params_common)

        X_train, X_valid = self.load_data_by_id("train", cid), self.load_data_by_id("vali", cid)

        model = LogisticRegression("ranking", params, self.logger)
        model.fit(X_train, validation_data=X_valid)
        model.save_session()


    # def train_dnn(self, cid):
    #     params = {
    #         "offline_model_dir": "./weights/dnn",
    #
    #         # deep part score fn
    #         "fc_type": "fc",
    #         "fc_dim": 32,
    #         "fc_dropout": 0.,
    #     }
    #     params.update(self.params_common)
    #
    #     X_train, X_valid = self.load_data("train", cid), self.load_data("vali", cid)
    #
    #     model = DNN("ranking", params, self.logger)
    #     model.fit(X_train, validation_data=X_valid)
    #     model.save_session()

    def train_dnn(self, cid):
        params = {
            "offline_model_dir": PROJECT_ROOT+"/ltr/weights/dnn",

            # deep part score fn
            "fc_type": "fc",
            "fc_dim": 32,
            "fc_dropout": 0.,
        }
        params.update(self.params_common)
        X_train, X_valid = self.load_data_by_id("train", cid), self.load_data_by_id("vali", cid)

        model = DNN("ranking", params, self.logger)
        model.fit(X_train, validation_data=X_valid)
        model.save_session()
        return model

    def restore_dnn(self, model):
        if not model:
            params = {
                "offline_model_dir": PROJECT_ROOT+"/ltr/weights/dnn",

                # deep part score fn
                "fc_type": "fc",
                "fc_dim": 32,
                "fc_dropout": 0.,
            }
            params.update(self.params_common)
            model = DNN("ranking", params, self.logger, training=False)
        model.restore_session()
        return model

    def predict_dnn(self, model, cid):
        X_test = self.load_data_by_id("test", cid)
        return model.predict(X_test)


    def train_ranknet(self, cid):
        params = {
            "offline_model_dir": "./weights/ranknet",

            # deep part score fn
            "fc_type": "fc",
            "fc_dim": 32,
            "fc_dropout": 0.,

            # ranknet param
            "factorization": True,
            "sigma": 1.,
        }
        params.update(self.params_common)

        X_train, X_valid = self.load_data_by_id("train", cid), self.load_data_by_id("vali", cid)

        model = RankNet("ranking", params, self.logger)
        model.fit(X_train, validation_data=X_valid)
        model.save_session()


    def train_lambdarank(self, cid):
        params = {
            "offline_model_dir": "./weights/lambdarank",

            # deep part score fn
            "fc_type": "fc",
            "fc_dim": 32,
            "fc_dropout": 0.,

            # lambdarank param
            "sigma": 1.,
        }
        params.update(self.params_common)

        X_train, X_valid = self.load_data_by_id("train", cid), self.load_data_by_id("vali", cid)

        model = LambdaRank("ranking", params, self.logger)
        model.fit(X_train, validation_data=X_valid)
        model.save_session()


    # def main():
    #     if len(sys.argv) > 1:
    #         if sys.argv[1] == "lr":
    #             train_lr()
    #         elif sys.argv[1] == "dnn":
    #             train_dnn()
    #         elif sys.argv[1] == "ranknet":
    #             train_ranknet()
    #         elif sys.argv[1] == "lambdarank":
    #             train_lambdarank()
    #     else:
    #         train_lr()


if __name__ == "__main__":

    try:
        from . import ltrmanager
    except:
        import ltrmanager

    cid = config.LTR_CID

    convert_by_id("train", cid)
    convert_by_id("vali", cid)
    convert_by_id("test", cid)

    ltm = ltrmanager.LtrManager()
    model = ltm.train_dnn(cid)

    # model = None
    model = ltm.restore_dnn(model)
    y_pred = ltm.predict_dnn(model, cid)
    print(y_pred)




