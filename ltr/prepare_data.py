import os
import numpy as np
import utils

label_file_pat = "./data/processed/%s_%s_label.npy"
group_file_pat = "./data/processed/%s_%s_group.npy"
feature_file_pat = "./data/processed/%s_%s_feature.npy"

utils._makedirs('logs')
logger = utils._get_logger("./logs", "tf-%s.log" % utils._timestamp())

def convert(type, cid):
    data_path = os.path.join(".", "data/MQ2008/Fold1/"+ type + ".txt")

    labels = []
    features = []
    groups = []
    with open(data_path, "r") as f:
        for line in f:
            if not line:
                break
            if "#" in line:
                line = line[:line.index("#")]
            splits = line.strip().split(" ")
            labels.append(splits[0])
            groups.append(splits[1].split(":")[1])
            features.append([split.split(":")[1] for split in splits[2:]])
    np.save(label_file_pat % (cid, type), np.array(labels, dtype=int))
    np.save(group_file_pat % (cid, type), np.array(groups, dtype=int))
    np.save(feature_file_pat % (cid, type), np.array(features, dtype=float))
    logger.info("read {0} reviews".format('in convert'))


if __name__ == "__main__":
    logger.info("read {0} reviews".format('here'))
    convert("train", 1000000000)
    convert("vali", 1000000000)
    convert("test", 1000000000)

