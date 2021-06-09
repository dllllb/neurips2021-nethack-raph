![Nethack Banner](https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/logo.png)

# **NeurIPS 2021 - The NetHack Challenge** - Starter Kit


This repository is the Nethack Challenge **Starter kit**! It contains:
* **Instructions** for setting up your codebase to make submissions easy.
* **Baselines** for quickly getting started training your agent.
* **Notebooks** for introducing you to NetHack and the NLE.
* **Documentation** for how to submit your model to the leaderboard.

Quick Links:

* [The NetHack Challenge - Competition Page](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge)
* [The NetHack Challenge - Discord Server](https://discord.gg/zkFWQmSWBA)
* [The NetHack Challenge - Starter Kit](https://gitlab.aicrowd.com/nethack/neurips-2021-the-nethack-challenge)
* [IMPORTANT - Accept the rules before you submit](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/challenge_rules)


# Table of Contents
1. [Intro to Nethack and the Nethack Challenge](#intro-to-nethack-and-the-nethack-challenge)
2. [Setting up your codebase](setting-up-your-codebase)
3. [Baselines](baselines)
4. [How to test and debug locally](how-to-test-and-debug-locally)
5. [How to submit](how-to-submit)

# Intro to Nethack and the Nethack Challenge

Your goal is to produce the best possible agent for navigating the depths
of Nethack dungeons and emerging with the Amulet in hand! 
You can approach this task however you please, but a good starting point 
would be [**this notebook**](./notebooks/NetHackTutorial.ipynb) which provides
an overview of  (1) the many dynamics at play in the game and   (2) the 
observation and action space with which your agent will interact. 

#### A high level description of the Challenge Procedure:
1. **Sign up** to join the competition [on the AIcrowd website](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge).
2. **Clone** this repo and start developing your solution.
3. **Train** your models on NLE, and ensure run.sh will generate rollouts.
4. **Submit** your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com)
for evaluation (full instructions below). The automated evaluation setup
will evaluate the submissions against the NLE environment for a fixed 
number of rollouts to compute and report the metrics on the leaderboard
of the competition.

![](https://i.imgur.com/xzQkwKV.jpg)

# Setting Up Your Codebase

AIcrowd provides great flexibility in the details of your submission!  
Find the answers to FAQs about submission structure below, followed by 
the guide for setting up this starter kit and linking it to the AIcrowd 
GitLab.

## FAQs

**How does submission work?**

The submission entrypoint is a bash script `run.sh`. When this script is 
called, aicrowd will expect you to generate all your rollouts in the 
allotted time, using `aicrowd_gym` in place of regular `gym`.  This means 
that AIcrowd can make sure everyone is running the same environment, 
and can keep score!

**What languages can I use?**

Since the entrypoint is a bash script `run.sh`, you can call any arbitrary
code from this script.  However, to get you started, the environment is 
set up to generate rollouts in Python. 

The repo gives you a template placeholder to load your model 
(`agents/your_agent.py`), and a config to choose which agent to load 
(`submission_config.py`). You can then test a submission, adding all of 
AIcrowd’s timeouts on the environment, with `python test_submission.py`

**How do I specify my dependencies?**

We accept submissions with custom runtimes, so you can choose your 
favorite! The configuration files typically include `requirements.txt` 
(pypi packages), `apt.txt` (apt packages) or even your own `Dockerfile`.

You can check detailed information about the same in the `RUNTIME.md` file.

**What should my code structure look like?**

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

Finally, **you must specify an AIcrowd submission JSON in `aicrowd.json` to be scored!** See "How do I actually make a submission" below for more details.



**How can I get going with an existing baseline?**

The best current baseline is the torchbeast baseline. Follow the instructions 
[here](/nethack_baselines/torchbeast/) to install and start training 
the model (there are even some suggestions for improvements).

To then submit your saved model, simply set the `AGENT` in 
`submission config` to be `TorchBeastAgent`, and modify the 
`agent/torchbeast_agent.py` to point to your saved directory.

You can now test your saved model with `python test_baseline.py`

**How can I get going with a completely new model?**

Train your model as you like, and when you’re ready to submit, just adapt
`YourAgent` in `agents/your_agent.py` to load your model and take a `batched_step`.

Then just set your `AGENT` in `submission_config.py` to be this class 
and you are ready to test with `python test_submission.py`

**How do I actually make a submission?**

First you need to fill in you `aicrowd.json`, to give AIcrowd some info so you can be scored.
The `aicrowd.json` of each submission should contain the following content:

```json
{
  "challenge_id": "evaluations-api-neurips-nethack",
  "authors": ["your-aicrowd-username"],
  "description": "(optional) description about your awesome agent",
  "external_dataset_used": false
}
```

The submission is made by adding everything including the model to git,
tagging the submission with a git tag that starts with `submission-`, and 
pushing to AIcrowd's GitLab. The rest is done for you!

More details are available [here](/docs/SUBMISSION.md)

**Are there any hardware or time constraints?**

Your submission will need to complete 128 rollouts in 30 minutes. We will
run 4 of these in parallel, and a total of 512 episodes will be used for
evaluation. The episode will timeout and terminate if any action is
left hanging for 300 seconds, or 10,000 steps are taken without 
advancing the in game clock. 

The machine where the submission will run will have following specifications:
* 1 NVIDIA T4 GPU
* 4 vCPUs
* 16 GB RAM

## Setting Up Details

1. **Add your SSH key** to AIcrowd GitLab

You can add your SSH Keys to your GitLab account by going to your profile settings [here](https://gitlab.aicrowd.com/profile/keys). If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

2.  **Clone the repository**

    ```
    git clone git@gitlab.aicrowd.com:nethack/neurips-2021-the-nethack-challenge.git
    ```

3. **Install** competition specific dependencies!
    ```
    pip install -r requirements
    ```

4. Run rollouts with a random agent with `python test_submission.py`.

### For setting up the Nethack Learning Environment:

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
$ pip install nle
```

Find more details on the [original nethack repository](https://github.com/facebookresearch/nle)

# Baselines

Although we are looking to supply this repository with more baselines throughout the first month of the competition, this repository comes with a strong IMPALA-based baseline in the directory `./nethack_baselines/torchbeast`.

More info on how to install, train and submit that repo are available [here](./nethack_baselines/torchbeast/README.md) - along with some suggestions on where to go next!

# How to Test and Debug Locally

The best way to test your model is to run your submission locally.

You can do this naively by simply running  `python rollout.py` or you can simulate the extra timeout wrappers that AIcrowd will implement by using `python test_submission.py`. 

# How to Submit

More information on submissions can be found at our [SUBMISSION.md](/docs/SUBMISSION.md)

## Contributors

- [Jyotish Poonganam](https://www.aicrowd.com/participants/jyotish)
- [Dipam chakraborty](https://www.aicrowd.com/participants/dipam)
- [Shivam Khandelwal](https://www.aicrowd.com/participants/shivam)
- [Eric Hambro](https://www.aicrowd.com/participants/eric_hammy)
- [Danielle Rothermel](https://www.aicrowd.com/participants/danielle_rothermel)


<!--  
=================

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
$ pip install git+https://github.com/facebookresearch/nle.git@eric/competition --no-binary:nle
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

4. Try out random rollout script in `rollout.py`.


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



├── Dockerfile
├── LICENSE
├── README.md
├── __pycache__
│   ├── rollout.cpython-37.pyc
│   └── submission_config.cpython-37.pyc
├── agents
│   ├── __pycache__
│   ├── batched_agent.py
│   ├── random_batched_agent.py
│   ├── rllib_batched_agent.py
│   └── torchbeast_agent.py
├── aicrowd.json
├── apt.txt
├── docs
│   ├── RUNTIME.md
│   └── SUBMISSION.md
├── envs
│   ├── __init__.py
│   ├── __pycache__
│   ├── batched_env.py
│   └── wrappers.py
├── evaluation_utils
│   └── custom_wrappers.py
├── nethack_baselines
│   ├── other_examples
│   ├── rllib
│   └── torchbeast
├── notebooks
├── requirements.txt
├── rollout.py
├── run.sh
├── submission_config.py
├── test_submission.py
└── utility
    ├── docker_build.sh
    ├── docker_run.sh
    ├── environ.sh
    ├── parser.py
    └── verify_or_download_data.py


<p style="text-align:center"><img style="text-align:center" src="https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/example_run.gif"></p> -->
