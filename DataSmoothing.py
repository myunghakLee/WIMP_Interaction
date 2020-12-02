import numpy as np
import pylab as plt
import statsmodels.api as sm

def smoothing(arr, weight=1):
    if len(arr)>0:
        arr[...,0] += [i/10000*weight for i in range(len(arr))]
        arr[...,1] += [i/10000*weight for i in range(len(arr))]

        ans = sm.nonparametric.lowess(arr[...,1] , arr[...,0])
        nan_check = np.isnan(ans)
        
        if (True in nan_check):
            ans = smoothing(arr, weight *0.8)
            assert weight > 0.1, "recursive function is too continuous"
            
            nan_check = np.isnan(ans)
        assert not (True in nan_check), ("None is exist, ",arr)
#             dist1 = max(arr[...,1]) - min(arr[...,1])
#             dist2 = max(arr[...,0]) - min(arr[...,0])
#             print(dist1, dist2)
# #             if dist1>5 or dist2>5:
# #                 print(max(arr[...,0]), min(arr[...,0]),max(arr[...,1]), min(arr[...,1]))
#             print(arr)
        
        return ans
    return arr


from tqdm import tqdm
import numpy as np
import pickle
import os

dir_arr = ["train"]

for index in range(1):
    pickle_dir = f"data/argoverse_processed/{dir_arr[index]}/"
    save_dir = f"data/argoverse_processed_smoothing/{dir_arr[index]}/"
    file_list = sorted(os.listdir(pickle_dir), key = lambda a: int(a.split(".")[0]))
    print(save_dir)
    for file_index in tqdm(range(len(file_list))):
        with open(pickle_dir + file_list[file_index], 'rb') as f:
            data = pickle.load(f)
            write_pickle = {}
            write_pickle["AGENT"] = {}
            write_pickle["SOCIAL"] = []
            write_pickle['AGENT']["XY_FEATURES"] = smoothing(data['AGENT']["XY_FEATURES"])
            write_pickle['AGENT']["HEURISTIC_ORACLE_CENTERLINE_NORMALIZED_PARTIAL"] = data['AGENT']["HEURISTIC_ORACLE_CENTERLINE_NORMALIZED_PARTIAL"]
            if "LABELS" in data["AGENT"]:
                write_pickle['AGENT']["LABELS"] = smoothing(data['AGENT']["LABELS"])
            write_pickle["PATH"] = data["PATH"]
            write_pickle["SEQ_ID"] = data["SEQ_ID"]
            write_pickle["TRANSLATION"] = data["TRANSLATION"]
            write_pickle["ROTATION"] = data["ROTATION"]
            write_pickle["CITY_NAME"] = data["CITY_NAME"]
            
            for i in range(len(data['SOCIAL'])):
                T = {}
                T["XY_FEATURES"] = smoothing(data['SOCIAL'][i]["XY_FEATURES"])
                T["HEURISTIC_ORACLE_CENTERLINE_NORMALIZED_PARTIAL"] = data['SOCIAL'][i]["HEURISTIC_ORACLE_CENTERLINE_NORMALIZED_PARTIAL"]
                if "LABELS" in data['SOCIAL'][i]:
                    T["LABELS"] = smoothing(data['SOCIAL'][i]["LABELS"])
                T["TSTAMPS"] = data["SOCIAL"][i]["TSTAMPS"]
                write_pickle["SOCIAL"].append(T)
            with open(save_dir + file_list[file_index], 'wb') as fw:
                pickle.dump(write_pickle, fw)
