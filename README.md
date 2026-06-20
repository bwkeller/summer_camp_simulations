# Simulating Galaxies with GASOLINE

## Step 0: Set up your environment
To use the simulations in this activity, we will first need to configure our environment to allow us to run the simulation code gasoline.

First, we will download all of the tools we need using `git`.  `git` is a tool for managing projects, it helps you keep track of changes
and share code and data with others:  

`git clone https://github.com/bwkeller/summer_camp_simulations.git summer_camp`

We can change directories into the new stuff we just fetched using `cd`:

`cd summer_camp`

You can take a look at the files in this directory with ls:

`ls`

Now we will load the required modules. Since we will be using python scripts to help us out, we will need to load python. To make the movie of the collision we will use a tool called ffmpeg. We can load both of these with:

`module load python ffmpeg/7.1.1`

Next, we will need to install a couple of python libraries that will let us work with simulation data.

`pip install --user numpy pynbody matplotlib`

Aside from that, you already have the rest of the scripts and data needed in your home directory.

## Step 1: Build Your Initial Conditions Workspace
Every N-Body simulation starts with *initial conditions*, which describe the positions and velocities of the particles at $t=0$. We're going to build an initial condition which contains a thin, rotating disc and a spheroidal "bulge" in the center.  With this, we will see how the initial velocities of the stars can change how things like bars and spiral arms grow.

I've written a script called `make_single.py` that will create this for you. It takes one required arguments: 
1. The velocity dispersion (think of "noise" in the velocity: the higher the dispersion, the more random the velocity magnitudes and directions are).  This is given in kilometers per second.

Let's first try an experiment where we start with a "cold" disc: one with zero added velocity dispersion

`python make_single.py 0 --name cold`

This script will automatically create a new workspace folder for you called `run_cold/` and put everything inside it—including your physics files, the supercomputer settings, and the simulation code!

## Step 2: Run the simulation
You can submit the simulation directly to the supercomputer queue by changing into your newly generated experiment folder and launching its custom run script.

First, change directory into your new folder:

`cd run_cold`

Then, use the `sbatch` command to submit your job to the supercomputer:

`sbatch run.sh`

You can see if your job has started using the `squeue` command:

`squeue -u $USER`

If the `ST` column shows `R`, the supercomputer has started running your calculations. You can monitor its progress live by viewing the log:

`tail screen.log`

When the simulation has finished, there should be up to 300 "snapshots" in this directory, each corresponding to roughly 8 million years of time—meaning your simulation covers roughly 3 billion years of cosmic history!

## Step 3: Visualize your simulation
Now that we've run this simulation, we want to look at it. To make a movie, return back to the main directory using:

`cd ..`

Now run the movie-making script. It takes two arguments: the name of the folder containing your snapshots, and the name you want to give your video file:

`./make_movie.sh run_cold cold_disc`

This will make you a movie file `cold_disc.mp4`. You can view your movie by double-clicking the file on the left-hand side of your MobaXTerm window!

## Step 5: Simulate a Hot Disc
Let's see what happens now with a disc that has a lot of random velocity noise (what we would call a "hot" disc).  Try a velocity dispersion in the range of 20 - 60 km/s, and repeat steps 1-3:

Make the IC:

`python make_single.py 40 --name hot`

Run the IC:

`cd run_hot`

`sbatch run.sh`

When the run is finished, visualize the results:

`./make_movie.sh run_hot hot_disc`

What do you see that is different from the cold disc?  Why do you think that is?

## Step 6: Smash two galaxies together!
We've seen how to simulate individual galaxies, let's now build an initial condition made of two galaxies that will collide with each other.

I've written a script called `make_merger.py` that will create this for you. It takes two required arguments: 
1. The rotation angle of the second galaxy around the X-axis (`theta`)
2. The rotation angle around the Z-axis (`phi`)

Let's first try an experiment where we smash two galaxies together that are both face-on, using the unique name `baseline`:

`python make_merger.py 0 0 --name baseline`

Run the IC:

`cd run_baseline`

`sbatch run.sh`

When the run is finished, visualize the results:

`./make_movie.sh run_baseline baseline`

What do you see that is different from the isolated discs?  What features in the merger do you think you can change by changing how the merger starts?


## Step 7: Experiment and Alter the Universe!
Now it's time to build your own custom cosmic experiment. Repeat Step 6, but change the parameters and assign an entirely new, unique `--name`. 

For example, to simulate a custom interaction, you can pass parameters to alter the galaxy structures. By using unique names each time, your baseline data and your new experiment data will live in separate folders safely without ever overwriting each other. You can create as many unique universes as your supercomputer time allocation allows!

---

## 🚀 Optional Advanced Challenges

If you have completed the baseline simulation and successfully generated your movie, you can begin altering fundamental laws of astrophysics in your next experiment. 

### Checking Your Controls (The Help Menu)
The `make_merger.py` script has a built-in interactive manual. You can view every mathematical constraint and customizable option by running:

`python make_merger.py --help`

This will print a guide detailing what parameters can be altered and the exact boundaries allowed by the program.

### Advanced Physics Flags to Try
You can chain any of the following optional arguments onto your Step 1 command to completely redesign the collision:

* **Mass Ratio (`--mass_ratio <number>`)**
  * *What it does:* Changes the relative mass scale between Galaxy 1 and Galaxy 2. For example, `--mass_ratio 3` makes Galaxy 2 exactly 1/3 the mass of Galaxy 1, establishing a minor merger (a dwarf galaxy colliding with a massive spiral galaxy).
  * *Allowed Range:* 1.0 to 5.0 (Default: 1.0)
* **Initial Separation (`--distance <number>`)**
  * *What it does:* Adjusts the starting gap between the two galaxies in kiloparsecs (kpc). A smaller distance makes them collide much faster; a wider distance gives them more time to interact dynamically.
  * *Allowed Range:* 50.0 to 300.0 (Default: 200.0)
* **Impact Parameter (`--impact_param <number>`)**
  * *What it does:* Adjusts the sideways approach velocity. A value of `0` results in an exact, catastrophic head-on collision. Higher values introduce an orbital offset, allowing the galaxies to gracefully slide past each other, forming long, dramatic tidal tails before merging.
  * *Allowed Range:* 0.0 to 1.5 (Default: 0.0)

### Example Advanced Run Command:
To create a minor merger event with a tilted, wide cosmic flyby, your command would look like this:

`python make_merger.py 45 90 --name minor_flyby --mass_ratio 3 --impact_param 1.5 --distance 250`
