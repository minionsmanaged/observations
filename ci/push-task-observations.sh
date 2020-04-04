#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"
random_delay=$((1 + RANDOM % 60))
echo waiting ${random_delay} seconds
sleep ${random_delay}
git checkout -b master
git pull
git add workers/${pool}
git commit -m "tc queue observations for ${pool}"
git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master