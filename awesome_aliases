alias myjobs='watch -n 1 squeue --format=\"%.12i %.7P %.40j %.20S %.10M %.9l %R\" --me --sort=-p'
alias docancelall='squeue --user $USER --format "scancel %i" | sh'
alias gpus="watch -n 1 nvidia-smi"
alias mydf="df -h /BS/mparcham"
alias work="cd /BS/mparcham2/work"
alias code=/var/tmp/build/usr/share/code/code; 

cleannotebook(){
jupyter nbconvert \
        --ClearOutputPreprocessor.enabled=True \
        --ClearMetadataPreprocessor.enabled=True \
        --to=notebook --log-level=ERROR --inplace \
        "$1"
}
export PS1='\h ~ \W: '
