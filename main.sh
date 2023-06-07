## Count number of files in each sub-dir
du -a | sed '/.*\.\/.*\/.*/!d' | cut -d/ -f2 | sort | uniq -c | sort -nr

## Touch the repositories so that they don't get deleted by IST :)
find ./someDir/ -type f | xargs -0 -P $(nproc) -n 5000 touch
# Potentially you can add -maxdepth -mindepth to make the search faster

## List all the directories without a certain file:
# e.g. if you want to see which experiments lack a sertain file:
find ./someDir/ -maxdepth 2 -mindepth 2 -type d '!' -exec test -e "{}/model_checkpoint_final.pt" ';' -print
