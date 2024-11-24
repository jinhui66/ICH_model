import argparse
import os

import numpy as np


def patientSelection(train_rate, val_rate, test_rate):
    """
    There should be two folders under the data folder, which represent whether the prognosis is good or bad
    """
    if not os.path.exists("./bad"):
        raise FileNotFoundError("no \"bad\" fold")
    if not os.path.exists("./good"):
        raise FileNotFoundError("no \"good\" fold")
    if train_rate + val_rate + test_rate > 100:
        raise SyntaxError("please check the dataset ratio.")
    print("Program launching: selecting data")
    print("dataset setting(by patient): %d%% for training,"
          " %d%% for val, %d%% for test." % (train_rate, val_rate, test_rate))
    try:
        train = open("./train.txt", 'w')
        val = open("./val.txt", 'w')
        test = open("./test.txt", 'w')
    except OSError as err:
        raise err

    count_train = 0
    count_val = 0
    count_test = 0
    bad_names = os.listdir("./bad")
    for name in bad_names:
        choice = np.random.randint(100)
        if choice < train_rate:
            train.write("bad/" + name + " " + str(0) + "\n")
            count_train += 1
        elif choice < train_rate + val_rate:
            val.write("bad/" + name + " " + str(0) + "\n")
            count_val += 1
        else:
            test.write("bad/" + name + " " + str(0) + "\n")
            count_test += 1

    good_names = os.listdir("./good")
    for name in good_names:
        choice = np.random.randint(100)
        if choice < train_rate:
            train.write("good/" + name + " " + str(1) + "\n")
            count_train += 1
        elif choice < train_rate + val_rate:
            val.write("good/" + name + " " + str(1) + "\n")
            count_val += 1
        else:
            test.write("good/" + name + " " + str(1) + "\n")
            count_test += 1
    print(f"In total, {count_train} for training, {count_val} for val, and {count_test} for test")
    train.close()
    val.close()
    test.close()
    print("selection completed!")


def add_gcs(img: np.ndarray, item: str) -> np.ndarray:
    item_list = item.split('_')
    gcs = int(item_list[len(item_list) - 1])
    img[img < 15] = (15 - gcs) * (240 / 15) + 15
    return img


def get_gcs(item: str) -> int:
    item_list = item.split('_')
    gcs = int(item_list[len(item_list) - 1])
    return gcs


if __name__ == "__main__":
    # Adding necessary input arguments
    parser = argparse.ArgumentParser(description="Data selection module")
    parser.add_argument("--train_rate", default=80, type=int, help="data ratio for training(%%)")
    parser.add_argument("--val_rate", default=10, type=int, help="data ratio for valid(%%)")
    parser.add_argument("--test_rate", default=10, type=int, help="data ratio for test(%%)")

    args = parser.parse_args()

    patientSelection(args.train_rate, args.val_rate, args.test_rate)
