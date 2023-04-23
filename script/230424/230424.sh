#!/bin/bash
cd ~/chatnvl/script/230424
sbatch -p inspur --gres gpu:A100 gpu1.sh
sbatch -p inspur --gres gpu:A100 gpu2.sh
sbatch -p inspur --gres gpu:A100 gpu3.sh
sbatch -p inspur --gres gpu:A100 gpu4.sh
sbatch -p inspur --gres gpu:A100 gpu5.sh
sbatch -p inspur --gres gpu:A100 gpu6.sh
sbatch -p inspur --gres gpu:A100 gpu7.sh
sbatch -p inspur --gres gpu:A100 gpu8.sh
