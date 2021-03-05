"""
Extension of the World Model:

Held and Hein kitten as motivation:
1 kitten was given full capability to walk, another not able to walk:


1) ultrasound sensor: use VAE: kitten with "ability to walk" can use the
reward system as part of sensory model, other kitten only uses encoder from VAE alone

Experiment: when training, train both VAEs using ultrasound point cloud,
Kitten 1 who has the ability "to walk" i.e. gather info about the environment
will further tune Encoder based on interaction with the environment. Kitten 2 will
not train based the encoder any further information.

This environment will be maze like and the robots will just simply want to navigate autonomously and
avoid objects (walls/robots). We will allow the robot that can "move" to train in the environment
to further train the encoder with feedback from the environment, we will be attempting to integrate meaning into the
interpretation of the vision. Train in "handicapped setting" for the introduction of meaning integration.
"""

from src.DRL.archive.VAE import *
LATENTDIM: int = 4
# VISION MODEL
VISION = CVAE(LATENTDIM)

# MEMORY MODEL

# CONTROLLER MODEL

