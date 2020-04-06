#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

random_uuid=$(uuidgen --random)
temp_branch=${random_uuid:(-12)}
git checkout -b ${temp_branch}
git add tasks/${pool}
git commit -m "tc queue observations for ${pool}"
git_ref=$(git rev-parse --verify HEAD)
git checkout master

push_attempts=0
push_success=false
until [ "${push_success}" = true ] || [ ${push_attempts} -gt 3 ]; do
  ((push_attempts=push_attempts+1))
  git fetch --all
  git reset --hard origin/master
  if git cherry-pick ${git_ref} && git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master; then
    push_success=true
    echo "push success on attempt ${push_attempts}"
  else
    echo "push failure on attempt ${push_attempts}"
  fi
done
