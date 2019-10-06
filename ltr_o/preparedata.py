import os, sys
import numpy as np
from utils import logmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

label_file_pat_by_id = PROJECT_ROOT + "/ltr/data/processed/%s_%s_label.npy"
group_file_pat_by_id = PROJECT_ROOT + "/ltr/data/processed/%s_%s_group.npy"
feature_file_pat_by_id = PROJECT_ROOT + "/ltr/data/processed/%s_%s_feature.npy"

logger = logmanager.logger('ltr', 'train')


def convert_by_id(type, cid):
    data_path = os.path.join(".", "data/MQ2008/Fold1/" + type + ".txt")

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

    print('labels:', labels)
    print('features:', features)
    print('groups:', groups)
    np.save(label_file_pat_by_id % (cid, type), np.array(labels, dtype=int))
    np.save(group_file_pat_by_id % (cid, type), np.array(groups, dtype=int))
    np.save(feature_file_pat_by_id % (cid, type), np.array(features, dtype=float))
    # logger.info("read {0} reviews".format('in convert'))


if __name__ == "__main__":
    # logger.info("read {0} reviews".format('here'))
    cid = config.LTR_CID
    convert_by_id("train", cid)
    convert_by_id("vali", cid)
    convert_by_id("test", cid)

