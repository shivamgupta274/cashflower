import importlib
import time

from multiprocessing import Pool
from cashflower import get_model_input, Model


def do_everything(chunk):
    modelpoint_module = importlib.import_module("wol.modelpoint")
    model_module = importlib.import_module("wol.model")
    variables, modelpoints = get_model_input(modelpoint_module, model_module)

    for modelpoint in modelpoints:
        modelpoint.data = modelpoint.data[chunk*250:(chunk+1)*250]

    model = Model(variables, modelpoints)
    model.run()
    return model.output


def do_everything2():
    modelpoint_module = importlib.import_module("wol.modelpoint")
    model_module = importlib.import_module("wol.model")
    variables, modelpoints = get_model_input(modelpoint_module, model_module)

    model = Model(variables, modelpoints)
    model.run()
    return model.output


if __name__ == "__main__":
    print("Starting...")
    st = time.time()

    # with Pool() as pool:
    #     x = list(pool.map(do_everything, range(4)))

    x = do_everything2()
    print(x)

    # get the execution time
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
