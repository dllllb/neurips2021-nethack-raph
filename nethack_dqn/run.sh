#!/bin/sh
# nohup python3 main.py --env-name QbertNoFrameskip-v4 --frame-skip 4 --total-steps 200000000 --grad-norm 10 --lr 0.0001 --eval-freq 100000 --plot-freq 100000 --duel --double --loss-type 'Huber' > ./temp_dir/Qbert_Double_Duel.txt &
python3 nethack_dqn/main.py --total-steps 5000000 --grad-norm 10 --lr 0.0001 --eval-freq 10000 --duel --double --loss-type 'Huber' --buffer-size 30000 --init-buff-size=30000 --decay-steps=1000000
