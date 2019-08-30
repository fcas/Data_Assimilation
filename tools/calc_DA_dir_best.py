"""File to run elements of VarDACAE module from"""
from VarDACAE import ML_utils,  SplitData
from VarDACAE.VarDA.batch_DA import BatchDA
from tools.check_train_load_DA import run_DA_batch
from notebooks.utils import get_model_specific_data
import os
import pickle


################ DA3 06a/06b
# BASE = "experiments/train/"
# DIR1 = BASE + "06a/"
# DIR2 = BASE + "06a2/"
# DIR3 = BASE + "06a3/"
#
# DIRS = [DIR1, DIR2, DIR3, "experiments/train2/06a4/"]

EXPDIR = "experiments/DA/02c/"
EPOCH = None #choose latest epoch if this is None

#Expt 02
B = "/home/jfm1118/DA/experiments/"
DIRS = [B + "02b/", B + "train/02a/"]
# B = "/home/jfm1118/DA/experiments/train2/08b/"
# DIRS = [B + str(x) + "/" for x in range(8, 11)]


#global variables for DA:
PRINT = True
ALL_DATA = True
def calc_DA_best(dirs, params, expdir, prnt=True, all_data=True, epoch=None):
    if isinstance(dirs, list):
        pass
    elif isinstance(dirs, str):
        dirs = [dirs]

    results = []
    index = 0

    for idx, dir in enumerate(dirs):
        for path, subdirs, files in os.walk(dir):
            for file in files:

                if file == "settings.txt":
                    #this is a model directory
                    dir = path
                    expt_name = path.split("/")
                    expt_name = "{}_{}".format([-1], str(index))
                    expdirnew = os.path.join(expdir, expt_name[-1])

                    mse_DA, model_data = calc_DA_dir(dir, params, expdirnew,
                                            prnt=True, all_data=all_data, epoch=epoch)
                    results.append((mse_DA, model_data, path))
                    index += 1
    print(results)
    print()
    res = sorted(results)
    out_fp = os.path.join(expdir, "final.txt")

    with open(out_fp, "wb") as f:
        results = pickle.dump(res, f)


    print(res)
    print("BEST")
    print(res[0])
    print()
    print("SECOND")
    print(res[1])
    print("THIRD")
    print(res[2])
    print("FOURTH")
    print(res[3])
    print("FIFTH")
    print(res[4])

def calc_DA_dir(dir, params, expdir, prnt=True, all_data=True, epoch=None):
    model, settings = ML_utils.load_model_and_settings_from_dir(dir, choose_epoch=epoch)
    df = run_DA_batch(settings, model, all_data, expdir, params)
    mse_DA = df["mse_DA"].mean()
    model_data = get_model_specific_data(settings, dir, model=model)
    if prnt:
        print(mse_DA, model_data)
        print(df.tail(5))
    return mse_DA, model_data


if __name__ == "__main__":
    params = {"var": 0.005, "tol":1e-3}
    calc_DA_best(DIRS, params, EXPDIR, PRINT, ALL_DATA, EPOCH)



