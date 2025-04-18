model=SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B
#model=Nexesenex/mrcuddle_Dark-Hermes3-Llama3.2-3B
#model=SentientAGI/Dobby-Mini-Leashed-Llama-3.1-8B
# share a volume with the Docker container to avoid downloading weights every run
volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:3.2.3 --model-id $model
