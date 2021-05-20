![Nethack Banner](https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/logo.png)

# Nethack Challenge - Starter Kit

👉 [Challenge page](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge)

[![Discord](https://img.shields.io/discord/565639094860775436.svg)](https://discord.gg/fNRrSvZkry)


This repository is the Nethack Challenge **Submission template and Starter kit**! 

Clone the repository to compete now!

**This repository contains**:
*  **Documentation** on how to submit your models to the leaderboard
*  **The procedure** for best practices and information on how we evaluate your agent, etc.
*  **Starter code** for you to get started!



# Table of Contents

1. [Competition Procedure](#competition-procedure)
2. [How to access and use dataset](#how-to-access-and-use-dataset)
3. [How to start participating](#how-to-start-participating)
4. [How do I specify my software runtime / dependencies?](#how-do-i-specify-my-software-runtime-dependencies-)
5. [What should my code structure be like ?](#what-should-my-code-structure-be-like-)
6. [How to make submission](#how-to-make-submission)
7. [Other concepts](#other-concepts)
8. [Important links](#-important-links)


<p style="text-align:center"><img style="text-align:center" src="https://raw.githubusercontent.com/facebookresearch/nle/master/dat/nle/example_run.gif"></p>


#  Competition Procedure

The NetHack Learning Environment (NLE) is a Reinforcement Learning environment presented at NeurIPS 2020. NLE is based on NetHack 3.6.6 and designed to provide a standard RL interface to the game, and comes with tasks that function as a first step to evaluate agents on this new environment. You can read more about NLE in the NeurIPS 2020 paper.


We are excited that this competition offers machine learning students, researchers and NetHack-bot builders the opportunity to participate in a grand challenge in AI without prohibitive computational costs—and we are eagerly looking forward to the wide variety of submissions.


**The following is a high level description of how this process works**

![](https://i.imgur.com/xzQkwKV.jpg)

1. **Sign up** to join the competition [on the AIcrowd website](https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge).
2. **Clone** this repo and start developing your solution.
3. **Train** your models for audio seperation and write prediction code in `test.py`.
4. [**Submit**](#how-to-submit-a-model) your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com) for evaluation [(full instructions below)](#how-to-submit-a-model). The automated evaluation setup will evaluate the submissions against the test dataset to compute and report the metrics on the leaderboard of the competition.

# How to run the environment

Install the environment from the [original nethack repository](https://github.com/facebookresearch/nle)

# How to start participating

## Setup

1. **Add your SSH key** to AIcrowd GitLab

You can add your SSH Keys to your GitLab account by going to your profile settings [here](https://gitlab.aicrowd.com/profile/keys). If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

2.  **Clone the repository**

    ```
    git clone git@github.com:AIcrowd/neurips-2021-nethack-starter-kit.git
    ```

3. **Install** competition specific dependencies!
    ```
    cd neurips-2021-nethack-starter-kit
    pip install -r requirements.txt
    ```

4. Try out random prediction codebase present in `test.py`.


## How do I specify my software runtime / dependencies ?

We accept submissions with custom runtime, so you don't need to worry about which libraries or framework to pick from.

The configuration files typically include `requirements.txt` (pypi packages), `environment.yml` (conda environment), `apt.txt` (apt packages) or even your own `Dockerfile`.

You can check detailed information about the same in the 👉 [RUNTIME.md](/docs/RUNTIME.md) file.

## What should my code structure be like ?

Please follow the example structure as it is in the starter kit for the code structure.
The different files and directories have following meaning:

```
.
├── aicrowd.json           # Submission meta information - like your username
├── apt.txt                # Packages to be installed inside docker image
├── data                   # Your local dataset copy - you don't need to upload it (read DATASET.md)
├── requirements.txt       # Python packages to be installed
├── test.py                # IMPORTANT: Your testing/prediction code, must be derived from NethackSubmission (example in test.py)
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

## How to make submission

👉 [SUBMISSION.md](/docs/SUBMISSION.md)

**Best of Luck** :tada: :tada:

# Other Concepts

## Hardware and Time constraints

To be added.

## Local Run

To be added.

## Contributing

You can share your solutions or any other baselines by contributing directly to this repository by opening merge request.

- Add your implemntation as `test_<approach-name>.py`
- Test it out using `python test_<approach-name>.py`
- Add any documentation for your approach at top of your file.
- Import it in `predict.py`
- Create merge request! 🎉🎉🎉 

## Contributors

- [Shivam Khandelwal](https://www.aicrowd.com/participants/shivam)
- [Jyotish Poonganam](https://www.aicrowd.com/participants/jyotish)
- [Dipam chakraborty](https://www.aicrowd.com/participants/dipam)

# 📎 Important links


💪 &nbsp;Challenge Page: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge

🗣️ &nbsp;Discussion Forum: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/discussion

🏆 &nbsp;Leaderboard: https://www.aicrowd.com/challenges/neurips-2021-nethack-challenge/leaderboards
