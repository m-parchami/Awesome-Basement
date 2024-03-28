## Count number of files in each sub-dir
du -a | sed '/.*\.\/.*\/.*/!d' | cut -d/ -f2 | sort | uniq -c | sort -nr

## Touch the repositories so that they don't get deleted by IST :)
find ./someDir/ -type f -print0 | xargs -0 -P $(nproc) -n 5000 touch
# Potentially you can add -maxdepth -mindepth to make the search faster

## List all the directories without a certain file:
# e.g. if you want to see which experiments lack a certain file:
find ./someDir/ -maxdepth 2 -mindepth 2 -type d '!' -exec test -e "{}/model_checkpoint_final.pt" ';' -print


## List sub-directories and create empty dirs under the same name at another path
find ./ -type d -exec mkdir -p -- ../IMNA/{} \;

## A good sync command to sync a directory with a remote directory using a proxy jump. It also ignores .png files
## and relies on checksum (rather than timestamp) for deciding what to transfer.
rsync -avz --checksum --exclude "*.png" -e "ssh -J user@proxy_server" experiments/ user@remote_server:copy_path
