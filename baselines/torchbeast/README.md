# TorchBeast NetHackChallenge Benchmark

This is a baseline model for the NetHack Challenge based on [TorchBeast](https://github.com/facebookresearch/torchbeast) - FAIR's implementation of IMPALA for PyTorch.

It comes with all the code you need to train, run and submit a model that is based on the results published in the original NLE paper.

This implementation runs with 2 GPUS (one for acting and one for learning), and runs many simultaneous environments with dynamic batching.

## Installation

To get this running all you need to do is follow the TorchBeast installation instructions, on the repo page, and then install the requirements.txt

A Dockerfile is also provided with installation of Torchbeast.

## Running The Baseline

Once installed, in this directory run:

`python polyhydra.py` 

To change parameters, edit `config.yaml`, or to override parameters from the command-line run:

`python polyhydra.py embedding_dim=16`

The training will save checkpoints to a new directory (`outputs`) and should the environments create any outputs, they will be saved to `nle_data` - (by default recordings of episodes are switched off to save space).

The default polybeast runs on 2 GPUs, one for the learner and one for the actors. However, with only one GPU you can run still run polybeast - just override the `actor_device` argument:

`python polyhydra.py actor_device=cpu`

## Making a submission

Take the output directory of your trained model, add the `checkpoint.tar` and `config.yaml` to the git repo. Then change the `SUBMISSION` variable in `rollout.py` in the base of this repository to point to that directory.

After that tag the submission, and push the branch and tag to AIcrowd's gitlab!


## Repo Structure

```
baselines/torchbeast
├── core/           
├── models/                #  <- Models HERE
├── util/           
├── config.yaml            #  <- Flags HERE
├── polybeast_env.py       #  <- Training Env HERE
├── polybeast_learner.py   #  <- Training Loop HERE
└── polyhydra.py           #  <- main() HERE

```

The structure is simple, compartmentalising the environment setup, training loop and models in to different files. You can tweak any of these separately, and add parameters to the flags (which are passed around).



## About the Model

This model (`BaselineNet`) we provide is simple and all in `models/baseline.py`.

* It encodes the dungeon into a fixed-size representation (`GlyphEncoder`)
* It encodes the topline message into a fixed-size representation (`MessageEncoder`)
* It encodes the bottom line statistics (eg armour class, health) into a fixed-size representation (`BLStatsEncoder`)
* It concatenates all these outputs into a fixed size, runs this through a fully connected layer, and into an LSTM.
* The outputs of the LSTM go through policy and baseline heads (since this is an actor-critic alorithm)


As you can see there is a lot of data to play with in this game, and plenty to try, both in modelling and in the learning algorithms used.

## Improvement Ideas

*Here are some ideas we haven't tried yet, but might be easy places to start. Happy tinkering!*


### Model Improvements (`baseline.py`)

* The model is currently not using the terminal observations (`tty_chars`, `tty_colors`, `tty_cursor`), so it has no idea about menus - could this we make use of this somehow?
* The bottom-line stats are very informative, but very simply encoded in `BLStatsEncoder` - is there a better way to do this?
* The `GlyphEncoder` builds a embedding for the glyphs, and then takes a crop of these centered around the player icon coordinates (`@`). Should the crop be reusing these the same embedding matrix? 
* The current model constrains the vast action space to a smaller subset of actions. Is it too constrained? Or not constrained enough?

###  Environment Improvements (`polybeast_env.py`)

* Opening menus (such as when spellcasting) do not advance the in game timer. However, models can also get stuck in menus as you have to learn what buttons to press to close the menu. Can changing the penalty for not advancing the in-game timer improve the result? 
* The NetHackChallenge assesses the score on random character assignments. Might it be easier to learn on just a few of these at the beginning of training? 

### Algorithm/Optimisation Improvements (`polybeast_learner.py`)

* Can we add some intrinsic rewards to help our agents learn? 
* Should we add penalties for disincentivise pathological behaviour we observe? 
* Can we improve the model by using a different optimizer?
