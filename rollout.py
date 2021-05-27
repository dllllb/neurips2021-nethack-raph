#!/usr/bin/env python
# This file is the entrypoint for your submission
# You can modify this file to include your code or directly call your functions/modules from here.

import aicrowd_gym
import nle

def main():
    """
    This function will be called for training phase.
    """

    # This allows us to limit the features of the environment 
    # that we don't want participants to use during the submission
    env = aicrowd_gym.make("NetHackChallenge-v0") 

    env.reset()
    done = False
    episode_count = 0
    while episode_count < 20:
        _, _, done, _ = env.step(env.action_space.sample())
        if done:
            episode_count += 1
            print(episode_count)
            env.reset()

if __name__ == "__main__":
    main()
