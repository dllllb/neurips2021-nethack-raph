#!/usr/bin/env python
# This file is the entrypoint for your submission.
# You can modify this file to include your code or directly call your functions/modules from here.


def main():
    """
    This function will be called for training phase.
    """

    # Sample code for illustration, add your training code below
    env = gym.make("NetHackScore-v0")

#     actions = [env.action_space.sample() for _ in range(10)] # Just doing 10 samples in this example
#     xposes = []
#     for _ in range(1):
#         obs = env.reset()
#         done = False
#         netr = 0

#         # Limiting our code to 1024 steps in this example, you can do "while not done" to run till end
#         while not done:

            # To get better view in your training phase, it is suggested
            # to register progress continuously, example when 54% completed
            # aicrowd_helper.register_progress(0.54)

    # Save trained model to train/ directory
    # Training 100% Completed
    aicrowd_helper.register_progress(1)
    #env.close()


if __name__ == "__main__":
    main()
