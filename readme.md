# GitHub branching basic commands
Author: Matthew Shan

Getting the files on your local machine (First time set up)
```
git clone [GitHub Repo]
```


## Pulling from GitHub upon updates to remote origin/master

**Important: Make sure you pull from master when there are updates, *especially* before created a new pull request.**

Pulls the remote branch of master
```
git pull origin master 
```

## Adding your changes and pushing it up
Goes to your own branch. Add -b to create a new one. 
```
git checkout [branch name]
```

**Important: Make sure you are working on your own branch before commiting/pushing. It's *bad* practice to work on master. See above. You can check to see what branch you are on by doing ```git branch``` or ```git status```**
1. **Do work**

2. **Add all the files in the repository to the staging area** 
```
git add . 
```

3. **Commit the staged file**
```
git commit -m “[Message]”
```

4. **Make sure you have pulled the lastest master changes befor pushing**
```
git pull origin master
```

5. **Push your commits to the remote repo branch.**
```
git push -u origin [Branch name]
```


6. **Now go to your branch on GitHub and create a new pull request. Ask someone to accept the pull request and your changes will be merged remote origin/master**

## Other potentially useful commands

If you want to revert all your changes back to the last commit. Useful when you want to go to a different branch and don’t care about your current work. If you do care about your work on this branch before checking out to another branch, just commit.
```
git stash
```
