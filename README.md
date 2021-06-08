![Nethack Banner](https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/logo.png)

# **NeurIPS 2021 - The NetHack Challenge** - Getting started
* **Challenge page** - https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge
* **IMPORTANT - [Accept the rules before you submit](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/challenge_rules)**
* **Join the discord server** - https://discord.gg/zkFWQmSWBA
* Clone the starter kit to start competing - TODO Add final starter kit link

This repository is the Nethack Challenge **Submission template and Starter kit**! It contains: 
*  **Documentation** on how to submit your models to the leaderboard
*  **The procedure** for best practices and information on how we evaluate your agent, etc.
*  **Baselines** for you to get started with training easily

<p style="text-align:center"><img style="text-align:center" src="https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/example_run.gif"></p>

# Table of Contents

1. [Competition Procedure](#competition-procedure)


#  Competition Procedure

The NetHack Learning Environment (NLE) is a Reinforcement Learning environment presented at NeurIPS 2020. NLE is based on NetHack 3.6.6 and designed to provide a standard RL interface to the game, and comes with tasks that function as a first step to evaluate agents on this new environment. You can read more about NLE in the NeurIPS 2020 paper.

We are excited that this competition offers machine learning students, researchers and NetHack-bot builders the opportunity to participate in a grand challenge in AI without prohibitive computational costs—and we are eagerly looking forward to the wide variety of submissions.


**The following is a high level description of how this process works**

1. **Sign up** to join the competition [on the AIcrowd website](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge).
2. **Clone** this repo and start developing your solution.
3. **Train** your models on NLE and write rollout code in `rollout.py`.
4. [**Submit**](#how-to-submit-a-model) your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com) for evaluation [(full instructions below)](#how-to-submit-a-model). The automated evaluation setup will evaluate the submissions against the NLE environment for a fixed number of rollouts to compute and report the metrics on the leaderboard of the competition.

![](https://i.imgur.com/xzQkwKV.jpg)

# Installation - Nethack Learning Environment

NLE requires `python>=3.5`, `cmake>=3.14` to be installed and available both when building the
package, and at runtime.

On **MacOS**, one can use `Homebrew` as follows:

``` bash
$ brew install cmake
```

On a plain **Ubuntu 18.04** distribution, `cmake` and other dependencies
can be installed by doing:

```bash
# Python and most build deps
$ sudo apt-get install -y build-essential autoconf libtool pkg-config \
    python3-dev python3-pip python3-numpy git flex bison libbz2-dev

# recent cmake version
$ wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | sudo apt-key add -
$ sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
$ sudo apt-get update && apt-get --allow-unauthenticated install -y \
    cmake \
    kitware-archive-keyring
```

Afterwards it's a matter of setting up your environment. We advise using a conda
environment for this:

```bash
$ conda create -n nle python=3.8
$ conda activate nle
$ pip install git+https://github.com/facebookresearch/nle.git@eric/competition
```

Find more details on the [original nethack repository](https://github.com/facebookresearch/nle)

# How to start participating

## Setup

1. **Add your SSH key** to AIcrowd GitLab

You can add your SSH Keys to your GitLab account by going to your profile settings [here](https://gitlab.aicrowd.com/profile/keys). If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

2.  **Clone the repository** - TODO

    ```
    git clone git@github.com:AIcrowd/neurips-2021-nethack-starter-kit.git
    ```

3. **Install** competition specific dependencies!
    ```
    pip install aicrowd-api
    pip install aicrowd-gym

    ## Install NLE according to the instructions above
    ```

4. Try out a random agent by setting `AGENT = RandomAgent` in `submission_config.py` and then running `rollout.py`.

5. See [this](/nethack_baselines/torchbeast/README.md) for an example of how to train and submit an IMPALA agent. Check out `nethack_baselines` for more examples. 

## How do I specify my software runtime / dependencies ? - TODO

We accept submissions with custom runtime, so you don't need to worry about which libraries or framework to pick from.

The configuration files typically include `requirements.txt` (pypi packages), `apt.txt` (apt packages) or even your own `Dockerfile`.

You can check detailed information about the same in the [RUNTIME.md](/docs/RUNTIME.md) file.

## What should my code structure be like ?

Please follow the example structure as it is in the starter kit for the code structure.
The different files and directories have following meaning:

```
.
├── aicrowd.json           # Submission meta information - like your username
├── apt.txt                # Packages to be installed inside docker image
├── requirements.txt       # Python packages to be installed
├── rollout.py             # Your rollout code - can use a batched agent
├── run.sh                 # Submission entrypoint   
└── utility                # The utility scripts to provide smoother experience to you.
    ├── docker_build.sh
    ├── docker_run.sh
    ├── environ.sh
```

Finally, **you must specify an AIcrowd submission JSON in `aicrowd.json` to be scored!** 

The `aicrowd.json` of each submission should contain the following content:

```json
{
  "challenge_id": "evaluations-api-neurips-nethack",
  "authors": ["your-aicrowd-username"],
  "description": "(optional) description about your awesome agent",
  "external_dataset_used": false
}
```

This JSON is used to map your submission to the challenge - so please remember to use the correct `challenge_id` as specified above.

## Can I use some other language instead of python?

The submission entrypoint is a bash script `run.sh`, you can call any arbitrary code you like from here. However, the environment has to be setup using python as in `rollout.py`. Any other code will have to communicte with the envrironment created in python.

**Note**: You need to install your dependencies for running your code by following the `How do I specify my software runtime/dependencies` section above.


## How to make submission

👉 [SUBMISSION.md](/docs/SUBMISSION.md)



# Other Information

## Hardware and Time constraints

To be added.

## Local Run

To be added.

## Contributing? - TODO

To be added

## Contributors - TODO

- [Jyotish Poonganam](https://www.aicrowd.com/participants/jyotish)
- [Dipam chakraborty](https://www.aicrowd.com/participants/dipam)
- [Shivam Khandelwal](https://www.aicrowd.com/participants/shivam)


# 📎 Important links - TODO

💪 &nbsp;Challenge Page: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge

🗣️ &nbsp;Discussion Forum: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/discussion

🏆 &nbsp;Leaderboard: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/leaderboards

**Best of Luck** 🎉 🎉