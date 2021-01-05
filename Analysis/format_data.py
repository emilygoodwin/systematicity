# Format data according to required output
import pandas as pd
import argparse
import os
import json
from tqdm import tqdm
from collections import Counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--step', default='0', type=str, help="Step number")
    parser.add_argument('-b','--base', default='/checkpoint/koustuvs/compositionality/', type=str, help="Base location")
    parser.add_argument('-o','--out', default='format_out.jsonl', type=str)
    parser.add_argument('-t', '--test_type', default="nbr,TIR,TCR", type=str)
    parser.add_argument('-c', '--choose', default=False, action='store_true', help='Choose test_type instead of skip')
    parser.add_argument('--model', default='BGRUlastEncoder',type=str)
    parser.add_argument('--seed', default='10',type=str)
    args = parser.parse_args()

    step_name = 'step_{}'.format(args.step)
    exp_id = 'exp_seed_{}_model_{}'.format(args.seed, args.model)
    base_folder = os.path.join(args.base, step_name)
    all_csv = os.path.join(base_folder, 'all_data.csv')
    # reconstruct all_csv in dict. have a line number as the key
    acd = {}
    ct = -1
    with open(all_csv,'r') as fp:
        for line in fp:
            ct +=1
            if ct == 0:
                continue
            acd[len(acd)] = line.rstrip().split(',')
    test_id_path = os.path.join(base_folder, 'ids.test')
    test_ids = []
    with open(test_id_path,'r') as fp:
        for line in fp:
            test_ids.append(int(line.rstrip()))
    test_records = [acd[ti] for ti in test_ids]
    raw_outputs = pd.read_csv(os.path.join(args.base, 'outputs','exp_seed_{}'.format(args.seed), step_name,
        'step_{}_{}_outp.csv'.format(args.step, args.model)))
    # create record id pointers
    test_rec_id = {tt[3]:ti for ti, tt in enumerate(test_records)}
    # merge the arrays
    for rec_id in range(len(test_records)):
        rec = test_records[rec_id]
        if len(rec) == 10:
            if type(rec[-1]) == str:
                rec[-1] = eval(rec[-1])
        else:
            arr = eval(','.join(rec[9:]))
            del rec[9:]
            rec.append(arr)
    ## prepare formatted output csv

    sentences = {}

    def add_get_sent(sent):
        if sent not in sentences:
            sentences[sent] = len(sentences)
        return sentences[sent]

    def get_one_test_nbrs(rec_id):
        f_data = {
            'PairA':'',
            'PairB':[],
            'PairAcorrectlabel':'',
            'PairApredictedlabel':'',
            'PairBcorrectlabel':[],
            'PairBPredictedlabel':[],
            'PairAtesttype':'',
            'PairBtesttype':[]
        }
        f_data['missing_IDs'] = []
        rec = test_records[rec_id]
        pair_a = (add_get_sent(rec[0]), add_get_sent(rec[1]))
        true_label = rec[2]
        out_rec = raw_outputs.loc[rec_id]
        assert true_label == out_rec['true_target']
        predicted_label = out_rec['predicted']
        test_type = rec[5]
        f_data['PairA'] = pair_a
        f_data['PairAcorrectlabel'] = true_label
        f_data['PairApredictedlabel'] = predicted_label
        f_data['PairAtesttype'] = test_type
        for nbr in rec[-1]:
            if str(nbr) in test_rec_id:
                nbr_rec_id = test_rec_id[str(nbr)]
                nbr_rec = test_records[nbr_rec_id]
                nbr_out_rec = raw_outputs.loc[nbr_rec_id]
                pair_b = (add_get_sent(nbr_rec[0]), add_get_sent(nbr_rec[1]))
                nbr_true_label = nbr_rec[2]
                assert nbr_true_label == nbr_out_rec['true_target']
                nbr_pred_label = nbr_out_rec['predicted']
                nbr_test_type = nbr_rec[5]
                f_data['PairB'].append(pair_b)
                f_data['PairBcorrectlabel'].append(nbr_true_label)
                f_data['PairBPredictedlabel'].append(nbr_pred_label)
                f_data['PairBtesttype'].append(nbr_test_type)
            else:
                f_data['missing_IDs'].append(nbr)
        return f_data

    skip_test = args.test_type.split(',')
    print("Total Records : {}".format(len(test_records)))
    print("Test types:")
    print(Counter([r[5] for r in test_records]))
    if args.choose:
        print("Choosing the following test types : {}".format(skip_test))
        test_recs_to_iterate = [rec_id for rec_id, rec in enumerate(test_records) if rec[5] in skip_test]
    else:
        print("Skipping the following test types : {}".format(skip_test))
        test_recs_to_iterate = [rec_id for rec_id, rec in enumerate(test_records) if rec[5] not in skip_test]
    print("Number of records  : {}".format(len(test_recs_to_iterate)))

    pb = tqdm(total=len(test_recs_to_iterate))
    with open(os.path.join(base_folder, '{}_'.format(exp_id) + args.out),'w') as fp:
        for rec_id in test_recs_to_iterate:
            fp.write(json.dumps(get_one_test_nbrs(rec_id)) + "\n")
            pb.update(1)
    pb.close()
    meta_data = {}
    meta_data['sentences'] = sentences

    print("{} IDS missing from all_data.csv")
    print("Saving meta data")
    json.dump(meta_data, open(os.path.join(base_folder, '{}_meta_data.json'.format(exp_id)),'w'))
    print("saved!")

