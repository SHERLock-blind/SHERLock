import pandas as pd
import json

import numpy as np
f = open('youcook.json',)

data = json.load(f)

data = data["database"]

print(len(data))
# train_df = pd.read_csv("./splits/train_duration_totalframe.csv")
train_df = pd.read_csv("./splits/val_duration_totalframe.csv")

train_map = {}

for i in range(len(train_df)):
    train_map[str(train_df['vid_id'][i])] = (float(train_df['total_frame'][i]) , float(train_df['duration'][i]))


feat_comment = {}
name_map = {"validation":"val_frame_feat_csv"}#{"training":"train_frame_feat_csv"}#

for dat in data:
    if data[dat]['subset'] == "validation":
        path = name_map[data[dat]['subset']] + "/" + data[dat]['recipe_type'] + "/" + str(dat)


        comment = ""
        pair_intervals = []
        pair_timestamp = []
        annot = data[dat]['annotations']
        for entry in annot:
            comment = comment + " . " + entry['sentence']
            pair_timestamp.append(abs(int(entry['segment'][0])- int(entry['segment'][1])))
            interval = (int(entry['segment'][0]) * (train_map[str(dat)][0] / train_map[str(dat)][1]), int(entry['segment'][1]) * (train_map[str(dat)][0] / train_map[str(dat)][1]))
            fps = float(train_map[str(dat)][0]) / float(train_map[str(dat)][1])
            xx = (interval[0] * 500.0) / max(500.0, float(train_map[str(dat)][0]))
            yy = (interval[1] * 500.0) / max(500.0 ,float(train_map[str(dat)][0]))
            pair_intervals.append((xx, yy))
        feat_comment[(path, fps)] = (comment, pair_intervals, pair_timestamp)
        # print(path)
        # print(comment)
        # break

np.save("feat_comment_interval_200_validation.npy", feat_comment)
f.close()