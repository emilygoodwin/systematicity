#!/bin/sh
model=BGRUlastEncoder

python format_data.py -s 0 --seed 10 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 1 --seed 10 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 2 --seed 10 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 3 --seed 10 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 0 --seed 20 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 1 --seed 20 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 2 --seed 20 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 3 --seed 20 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 0 --seed 30 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 1 --seed 30 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 2 --seed 30 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
python format_data.py -s 3 --seed 30 --model $model -t "TIR,TCR" -c >/dev/null 2>&1 &
#python format_data.py -s 0 --seed 40 >/dev/null 2>&1 &
#python format_data.py -s 1 --seed 40 >/dev/null 2>&1 &
#python format_data.py -s 2 --seed 40 >/dev/null 2>&1 &
#python format_data.py -s 3 --seed 40 >/dev/null 2>&1 &
#python format_data.py -s 0 --seed 50 >/dev/null 2>&1 &
#python format_data.py -s 1 --seed 50 >/dev/null 2>&1 &
#python format_data.py -s 2 --seed 50 >/dev/null 2>&1 &
#python format_data.py -s 3 --seed 50 >/dev/null 2>&1 &
wait

