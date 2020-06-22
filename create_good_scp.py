import os
import argparse
import logging

def GenrateTrainScp(dataPath):
    train_mix = os.path.join(dataPath, 'audio', 'tr', 'mix')
    train_s1 = os.path.join(dataPath, 'audio', 'tr', 's1')
    train_s2 = os.path.join(dataPath, 'audio', 'tr', 's2')

    wav_scp_dir = os.path.join(dataPath, 'wav_scp')
    if not os.path.exists(wav_scp_dir):
        os.mkdir(wav_scp_dir)

    train_mix_scp = os.path.join(wav_scp_dir, 'tr_mix.scp')
    train_s1_scp = os.path.join(wav_scp_dir, 'tr_s1.scp')
    train_s2_scp = os.path.join(wav_scp_dir, 'tr_s2.scp')


    tr_mix = open(train_mix_scp, 'w')
    for root, dirs, files in os.walk(train_mix):
        files.sort()
        for file in files:
            tr_mix.write(file + " " + root + '/' + file)
            tr_mix.write('\n')

    tr_s1 = open(train_s1_scp, 'w')
    for root, dirs, files in os.walk(train_s1):
        files.sort()
        for file in files:
            tr_s1.write(file + " " + root + '/' + file)
            tr_s1.write('\n')

    tr_s2 = open(train_s2_scp, 'w')
    for root, dirs, files in os.walk(train_s2):
        files.sort()
        for file in files:
            tr_s2.write(file + " " + root + '/' + file)
            tr_s2.write('\n')


def GenrateTestScp(dataPath):
    test_mix = os.path.join(dataPath, 'audio', 'tt', 'mix')
    test_s1 = os.path.join(dataPath, 'audio', 'tt', 's1')
    test_s2 = os.path.join(dataPath, 'audio', 'tt', 's2')

    wav_scp_dir = os.path.join(dataPath, 'wav_scp')
    if not os.path.exists(wav_scp_dir):
        os.mkdir(wav_scp_dir)

    test_mix_scp = os.path.join(wav_scp_dir, 'tt_mix.scp')
    test_s1_scp = os.path.join(wav_scp_dir, 'tt_s1.scp')
    test_s2_scp = os.path.join(wav_scp_dir, 'tt_s2.scp')

    tt_mix = open(test_mix_scp, 'w')
    for root, dirs, files in os.walk(test_mix):
        files.sort()
        for file in files:
            tt_mix.write(file + " " + root + '/' + file)
            tt_mix.write('\n')

    tt_s1 = open(test_s1_scp, 'w')
    for root, dirs, files in os.walk(test_s1):
        files.sort()
        for file in files:
            tt_s1.write(file + " " + root + '/' + file)
            tt_s1.write('\n')

    tt_s2 = open(test_s2_scp, 'w')
    for root, dirs, files in os.walk(test_s2):
        files.sort()
        for file in files:
            tt_s2.write(file + " " + root + '/' + file)
            tt_s2.write('\n')


def GenrateCroValScp(dataPath):
    cv_mix = os.path.join(dataPath, 'audio', 'cv', 'mix')
    cv_s1 = os.path.join(dataPath, 'audio', 'cv', 's1')
    cv_s2 = os.path.join(dataPath, 'audio', 'cv', 's2')

    wav_scp_dir = os.path.join(dataPath, 'wav_scp')
    if not os.path.exists(wav_scp_dir):
        os.mkdir(wav_scp_dir)

    cv_mix_scp = os.path.join(wav_scp_dir, 'cv_mix.scp')
    cv_s1_scp = os.path.join(wav_scp_dir, 'cv_s1.scp')
    cv_s2_scp = os.path.join(wav_scp_dir, 'cv_s2.scp')

    cv_mix_file = open(cv_mix_scp, 'w')
    for root, dirs, files in os.walk(cv_mix):
        files.sort()
        for file in files:
            cv_mix_file.write(file + " " + root + '/' + file)
            cv_mix_file.write('\n')

    cv_s1_file = open(cv_s1_scp, 'w')
    for root, dirs, files in os.walk(cv_s1):
        files.sort()
        for file in files:
            cv_s1_file.write(file + " " + root + '/' + file)
            cv_s1_file.write('\n')

    cv_s2_file = open(cv_s2_scp, 'w')
    for root, dirs, files in os.walk(cv_s2):
        files.sort()
        for file in files:
            cv_s2_file.write(file + " " + root + '/' + file)
            cv_s2_file.write('\n')



def main(args):
    logging.basicConfig(level=logging.INFO)

    dataPath = args.data_dir
    GenrateTrainScp(dataPath)
    GenrateTestScp(dataPath)
    GenrateCroValScp(dataPath)
    logging.info("Finish creating wav scp")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script to create mixtures scp as Kaldi scp form'
    )

    parser.add_argument(
        "--data_dir",
        type=str,
        help='Input audio path'
    )

    args = parser.parse_args()
    main(args)
