# setting-up-github for CTP

## VERY IMPORTANT first step, Setup! 
0. Complete the setup.md install instructions from the Summer HW Phase 1 setup instructions here:  https://github.com/CUNYTechPrep/2024-python-summer-prep/blob/main/setup.md
	* You should have already done this, however, if you did not do this yet, complete the guide above or else this will def fail. 


## Forking The Repo
0. Create a fork of this repo. ![forking](https://raw.githubusercontent.com/zd123/images-for-class/main/forking-image-instructions/01-fork-button.png)

0. Name that fork `my-fork-2025-fall-data-science` ![enter image description here](https://github.com/zd123/images-for-class/blob/main/forking-image-instructions/02-naming-fork.png?raw=true)
	
0. Copy the link of your forked repo.  ![enter image description here](https://github.com/zd123/images-for-class/blob/main/forking-image-instructions/03-getting-fork-link.png?raw=true)

0. Open your terminal

0. Clone your forked version of the original version by typing in `git clone` then pasting the link you just copied. 
	* `git clone https://github.com/[YOUR-GITHUB-USER-NAME]/my-fork-2025-fall-data-science.git`

## Setting it up to listen for updates. 

0. Navigate to inside that repo. 
	* `cd my-fork-2025-fall-data-science`

0. Set the upstream (Note this is the link of the CUNY Tech Preps version of the repo, not your fork)
	* `git remote add upstream https://github.com/CUNYTechPrep/2025-DS-Fri-1230`

## Doing, Uploading/Pushing, and Submitting your HW

0. Make a copy of `Exercise-DONT-EDIT-MAKE-COPY.ipynb`
0. Name the new copy as `Exercise-[YOUR-INITIALS].ipynb`. Zack DeSario's would be `Exercise-ZD.ipynb`.


#### Doing your HW. 
0. MAKE A COPY OF THE EXERCISE FILE!!!!!!  
	* Make a copy of `Exercise-DONT-EDIT-MAKE-COPY.ipynb`
	* Name the new copy as `Exercise-[YOUR-INITIALS].ipynb`. Zack DeSario's would be `Exercise-ZD.ipynb`.
	* DO NOT EDIT THE `Exercise-DONT-EDIT-MAKE-COPY.ipynb`
	* Complete all the questions in YOUR COPY of the exercise file.

0. OPEN YOUR REPO USING VS CODE.
	* If you are not using VS Code then... 
		* Open your termial, type into your terminal and run
		* `jupyter notebook`
		* If that doesn't work, run `jupyter lab`

0. In the first cell OF YOUR COPIED EXERCISE FILE print something nice about the TA. 
	* `print('[SOMETHING NICE ABOUT YOUR TA]')`

0. Save the file by clicking the disk icon in the top right or `Command+s`. Or clicking the floppy-disk icon in the top right. 


## Uploading/Pushing Your HW
*Adding your changes and pushing them to github so they are viewable the internet*

0. In your terminal that is in repo where you just edited the Exercise file....
0. Add your changes 
	* `git add Week-01-Pandas/Exercise-[YOUR-INITIALS].ipynb`
0. Commit your changes
	* `git commit -m '[YOUR COMMIT MESSAGE HERE]'`
0. Push your changes
	* `git push`
0. SOME OF YOU WILL GET AN ERROR WHEN RUNNING GIT PUSH. 
0. This is because you have not logged into github yet. 
0. Its okay, see the AUTHING GITHUB section below for instructions on how to fix that error.

## Sanity check
0. Go to YOUR FORKED github repo. 
0. Navigate to Week-01 and click on the Exercise-[YOUR-INITIALS].ipynb file.
0. YOU SHOULD SEE YOUR `print('[SOMETHING NICE ABOUT YOUR TA]')` edits.
0. Make sure you can see the changes you made. 
0. Copy that exact URL, it should look something like this. https://github.com/zd123/my-fork-2023-fall-data-science-fridays/blob/main/Week-01-Pandas/Exercise-ZD.ipynb 
0. Paste that URL next to your name in the HW Submission Sheet in the Exercise column. 
	* [Tuesday's HW Submission Sheet](https://docs.google.com/spreadsheets/d/150MVMGhClrJ7NFAoukEvbZoujM3a_-7v9r9q4QihiAc/edit?gid=0#gid=0)
	* [Wed HW Submission Sheet](https://docs.google.com/spreadsheets/d/1h3TcC5mDSPhOuRIHJnq5qr-MHsEXfVdDxgx9s1YHWRM/edit?usp=sharing)
	* [Friday's 12:30 HW Submission Sheet](https://docs.google.com/spreadsheets/d/1jws-NeM5Ww4m903Xa8Vgdzcqi1LO3r_zXNQkNxeBk34/edit?usp=sharing)
	* [Friday's 6:30 HW Submission Sheet](https://docs.google.com/spreadsheets/d/1mIpyT3I08v-uU--gOqb0dVLy95jtnchKMAsAWXf_mus/edit?usp=sharing)


## Authing Github
If you have already cloned and successfully pushed to a github repo you can skip this.  IF YOU ARE NEW TO GITHUB THIS STEP IS SUPER IMPORTANT. 

### Authing for Mac users. 
0. Install brew 
	* `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
	* Make sure you follow the terminal output instructions to add brew to your path!!!
0. Update git
	* `brew install git`
	* `brew upgrade git`
0. Install github CLI
	* `brew install gh`
	* `brew update gh`
0. Log into Github via command line. 
	* `gh auth login`
	* Complete the prompted questions, the will look something like this...
		```
		? What account do you want to log into? 
			GitHub.com  <<-- YOUR ANSWER

		? What is your preferred protocol for Git operations on this host? 
			HTTPS <<-- YOUR ANSWER

		? Authenticate Git with your GitHub credentials? 
			Yes <<-- YOUR ANSWER

		? How would you like to authenticate GitHub CLI? 
			Login with a web browser. <<-- YOUR ANSWER
		```

### Authing for Windows

0. None if this will work if you haven't installed [Anaconda](https://www.anaconda.com/download). You should have done this step already as you were required to do this in the Summer HW.
0. Open up the Anaconda Powershell Terminal
	* Instructions on how to find it here --> [link](https://saturncloud.io/blog/how-to-access-anaconda-command-prompt-in-windows-10-64bit/#method-1-through-the-start-menu)
0. Download and install [git](https://git-scm.com/download/win).
	* Use the Standalone Installer not the Portable ("thumbdrive edition") installer. 
* Install Githubs CLI 
	* `conda install gh --channel conda-forge`
* Login to git by running this and following the prompts. 
	* `gh auth login`
	* Follow the on-screen prompts. GitHub CLI automatically stores your Git credentials for you when you choose HTTPS as your preferred protocol for Git operations and answer "yes" to the prompt asking if you would like to authenticate to Git with your GitHub credentials. This can be useful as it allows you to use Git commands like git push and git pull without needing to set up a separate credential manager or use SSH.
		```
		? What account do you want to log into? 
			GitHub.com  <<-- YOUR ANSWER

		? What is your preferred protocol for Git operations on this host? 
			HTTPS <<-- YOUR ANSWER

		? Authenticate Git with your GitHub credentials? 
			Yes <<-- YOUR ANSWER

		? How would you like to authenticate GitHub CLI? 
			Login with a web browser. <<-- YOUR ANSWER
		```

* If that doesn't work, try folling these instructions [provided here](https://github.com/CUNYTechPrep/2024-python-summer-prep/blob/main/setup-part-2-github.md) 
	* In the document above... Stop before the 'Making Sure It Works - Create and Edit your own Repo' section.  We will be doing that part later today. 


If you're still having issues... Follow these instructions CAREFULLY.
* https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

* https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
