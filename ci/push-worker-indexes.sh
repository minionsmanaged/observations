#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"
#git stash
git checkout master
#git stash apply
git pull
git add ./*.json
git commit -m "worker and pool indexes"
git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master