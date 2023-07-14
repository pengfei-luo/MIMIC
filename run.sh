export PYTHONPATH=$(pwd)
echo "Device is ${1}. Training on task ${2}";
CUDA_VISIBLE_DEVICES=${1} python -u ./codes/main.py --config "./config/${2}.yaml"