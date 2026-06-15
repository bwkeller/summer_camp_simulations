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

You can monitor the progress of the job by looking at either `screen.log` or `merger.log`:

`tail screen.log`

or 

`tail merger.log`

When the simulation has finished, there should be 300 "snapshots" in the
`run_merger` directory, each corresponding to roughly 8 million years of time:
that means the simulation covers a total time of about 3 billion years.

# Step 3: Visualize your simulation
Now that we've run this simulation, we probably want to actually look at it.  I've 
created a script you can run that will make a movie out of your simulation.  You just need to
run it from the main `summer_camp` directory using:

```cd ~/summer_camp
./make_movie.sh run_merger faceon
```

This will make you a movie file `faceon.mp4`, showing the collision of these two galaxies.

You can view your movie by dragging-and-dropping the file from mobaXTerm to
your desktop and opening it there.

# Step 4: Experiment with different galaxy rotations
Next, let's try making a different simulation by repeating steps 1-3, but using
angles other than 0 degrees. (90 or 45 would be good choices to try, but you
can pick anything between 0 and 360).  To compare, you should pick a movie name
other than `faceon`, so you don't overwrite the original.
