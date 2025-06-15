# Simulating a Galaxy Merger with GASOLINE

## Step 0: Set up your environment
To use the simulations in this activity, we will first need to configure the
supercomputer BigBlue to allow us to run the simulation code gasoline.

The first step will be to load the required modules.  Since we will be using 
python scripts to help us out, we will need to load python.  To make the movie
of the collision we will use a tool called ffmpeg.  We can load both of these with:

`module load python ffmpeg/7.1.1`

Next, we will need to install a couple of python libraries that will let us
work with simulation data.

`pip install --user numpy pynbody matplotlib`

Finally, you will need to copy the scripts and data needed for this to your home directory:

`cp -r ~bkeller1/summer_camp ~`

## Step 1: Build Initial Conditions
Every N-Body simulation starts with _initial conditions_, which describe the
positions and velocities of the particles at t=0.  We're going to build an
initial condition made of two galaxies that will collide with each other.

I've written a script called `make_IC.py` that will create this for you.  It
takes two arguments: the first is the angle of the second galaxy in the x-axis
(which rotates the disl towards or away from you), and the second is the angle
of the second galaxy in the y-axis (which rotates the disk up or down).  

Let's first try an experiment where we smash two galaxies together that are both
face-on:

`./make_IC.py 0 0`

This should create a new file called `merger.tipsy` that contains our initial conditions.

## Step 2: Run the simulation
I've set up everything you need to run your simulation in the `run_merger` directory of the
`summer_camp` folder.

First copy your new initial conditions over:

`cp merger.tipsy run_merger`

Then, you can submit the simulation to the supercomputer queue by first changing directory into
`run_merger`:

`cd run_merger`

and then using the `sbatch` command to submit the job's run script:

`sbatch run.sh`

You can see if your job has started using the `squeue` command:

`squeue -u $USER`

If the `ST` column shows `R`, the supercomputer has started running your job.
