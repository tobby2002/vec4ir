
import os, sys
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from util import dirmanager

label_file_pat = PROJECT_ROOT + "/ltr/data/processed/%s_label.npy"
group_file_pat = PROJECT_ROOT + "/ltr/data/processed/%s_group.npy"
feature_file_pat = PROJECT_ROOT + "/ltr/data/processed/%s_feature.npy"



def convert(type):
    data_path = PROJECT_ROOT + "/ltr/data/MQ2008/Fold1/" + type + ".txt"
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
    np.save(label_file_pat % (type), np.array(labels, dtype=int))
    np.save(group_file_pat % (type), np.array(groups, dtype=int))
    np.save(feature_file_pat % (type), np.array(features, dtype=float))


if __name__ == "__main__":
    convert("train")
    convert("vali")
    convert("test")
