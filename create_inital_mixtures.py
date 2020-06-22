import os
import random
import numpy as np
import argparse
import logging
def CreateFiles(input_dir, output_dir, nums_file, state):
    wavList = []
    mix_files = os.path.join(output_dir, 'mix_files')
    if not os.path.exists(mix_files):
        os.mkdir(mix_files)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if state.upper() in root.upper() and file.endswith('WAV') or file.endswith('wav'):
                wavFile = os.path.join(root, file)
                wavList.append(wavFile)
    random.shuffle(wavList)

    if state.upper() == 'TRAIN':

        existed_list_tr = []
        existed_list_cv = []

        wav_list_tr = wavList[:len(wavList)-int(len(wavList)*0.1)]
        wav_list_cv = wavList[len(wavList)-int(len(wavList)*0.1):]

        tr_file = os.path.join(mix_files, 'tr.txt')
        cv_file = os.path.join(mix_files, 'cv.txt')
        res_tr_list = []
        res_cv_list = []

        with open(tr_file, 'w') as ftr:
            for i in range(nums_file):
                mix = random.sample(wav_list_tr, 2)
                back_mix = [mix[1], mix[0]]
                if mix not in existed_list_tr:
                    res_tr_list.append(mix)
                else:
                    while mix in existed_list_tr:
                        mix = random.sample(wav_list_tr, 2)
                res_tr_list.append(mix)
                existed_list_tr.append(mix)
                existed_list_tr.append(back_mix)
                snr = np.random.uniform(0, 2.5)
                line = "{} {} {} {}\n".format(mix[0], snr, mix[1], -snr)
                ftr.write(line)
        ftr.close()

        with open(cv_file, 'w') as fcv:
            for i in range(int(nums_file * 0.1)):
                mix = random.sample(wav_list_cv, 2)
                back_mix = [mix[1], mix[0]]
                if mix not in existed_list_cv:
                    res_cv_list.append(mix)
                else:
                    while mix in existed_list_cv:
                        mix = random.sample(wav_list_cv, 2)
                res_cv_list.append(mix)
                existed_list_cv.append(mix)
                existed_list_cv.append(back_mix)
                snr = np.random.uniform(0, 2.5)
                line = "{} {} {} {}\n".format(mix[0], snr, mix[1], -snr)
                fcv.write(line)
        fcv.close()

    elif state.upper() == 'TEST':
        existed_list_tt = []
        wav_list_tt = wavList
        tt_file = os.path.join(mix_files, 'tt.txt')
        res_tt_list = []
        with open(tt_file, "w") as ftt:
            for i in range(100):
                mix = random.sample(wav_list_tt, 2)
                back_mix = [mix[1], mix[0]]
                if mix not in existed_list_tt:
                    res_tt_list.append(mix)
                else:
                    while mix in existed_list_tt:
                        mix = random.sample(wav_list_tt, 2)
                res_tt_list.append(mix)
                existed_list_tt.append(mix)
                existed_list_tt.append(back_mix)
                snr = np.random.uniform(0, 2.5)
                line = "{} {} {} {}\n".format(mix[0], snr, mix[1], -snr)
                ftt.write(line)
        ftt.close()


def run(args):
    logging.basicConfig(level=logging.INFO)

    input_dir =args.input_dir
    output_dir = args.output_dir
    state = args.state
    nums_file = args.nums_files
    CreateFiles(input_dir, output_dir, nums_file, state)
    logging.info("Done create initial data pair")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command to make separation dataset'
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        help="Path to input data directory"
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        help='Path ot output data directory'
    )
    parser.add_argument(
        "--nums_files",
        type=int,
        help='Path ot output data directory'
    )
    parser.add_argument(
        "--state",
        type=str,
        help='Whether create train or test data directory'
    )
    args = parser.parse_args()
    run(args)
