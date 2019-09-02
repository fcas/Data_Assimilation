"""
Run outstanding activation experiments for GDN and relu
    GRDN (place on x2 GPU)
"""

from VarDACAE.settings.models.resNeXt import ResStack3
from VarDACAE.settings.models.CLIC import CLIC, GRDNBaseline

from VarDACAE import TrainAE, ML_utils, BatchDA

from run_expts.expt_config import ExptConfigTest


TEST = False
GPU_DEVICE = 0
NUM_GPU = 1
exp_base = "experiments/train2/09c/"

#global variables for DA and training:
class ExptConfig():
    EPOCHS = 150
    SMALL_DEBUG_DOM = False #For training
    calc_DA_MAE = True
    num_epochs_cv = 0
    LR = 0.0002
    print_every = 10
    test_every = 10

def main():
    activations = ["GDN", "relu"]


    idx = 0
    for act in activations:
        if TEST:
            expt = ExptConfigTest()
        else:
            expt = ExptConfig()
        if act == "relu":
            expt.LR *= 0.1

        grdnkwargs =  {"block_type": "CBAM_NeXt", "Cstd": 32,
                    "aug_scheme": 0, "activation": act }

        idx_ = idx
        idx += 1
        if idx_ % NUM_GPU != GPU_DEVICE:
            continue


        for k, v in grdnkwargs.items():
            print("{}={}, ".format(k, v), end="")
        print()

        settings = GRDNBaseline(**grdnkwargs)
        settings.GPU_DEVICE = GPU_DEVICE
        settings.export_env_vars()

        expdir = exp_base + str(idx - 1) + "/"


        trainer = TrainAE(settings, expdir, expt.calc_DA_MAE)
        expdir = trainer.expdir #get full path


        model = trainer.train(expt.EPOCHS, test_every=expt.test_every,
                                num_epochs_cv=expt.num_epochs_cv,
                                learning_rate = expt.LR, print_every=expt.print_every,
                                small_debug=expt.SMALL_DEBUG_DOM)



if __name__ == "__main__":
    main()


