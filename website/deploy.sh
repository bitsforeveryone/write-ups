#!/bin/bash
# reference: https://gohugo.io/hosting-and-deployment/hosting-on-github/#host-github-user-or-organization-pages

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
hugo 

# Go To Public folder and add changes to git
cd public
# ensure we are at head
git checkout master
git pull origin master
# add changes
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master

# Come Back up to the Project Root
cd ..

# Update submodule
git add public
git commit -m "deployed site `date`"
