
# Solve the SHE with multiplicative noise
# We use Space-Time discretesation (1D Finite elements)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg
from matplotlib import colors
from IPython import embed
from os import path
import sys

class she:
	"""
	We model the multiplicative SHE (1D).
	"""
	def __init__(self, x0):
		# Initial state of the sistem.
		self.state = x0

	def do_step(self):
		# We do one more step in the implicit Euler approximations
		self.state = np.dot(resolvent, self.state  - (np.multiply(np.multiply(self.state, self.state-1), self.state-0.5) )*delta_t \
			+ np.random.normal(size = (space_pts) , scale = np.sqrt(delta_t/delta_x)) )
		#self.state = np.dot(resolvent, self.state + np.random.normal(size = (space_pts), scale = np.sqrt(delta_t/delta_x) ) ) 

def animate(i):
	# global she_sample, ax, fig, time_text
	# Real time is:
	ani_time = i*delta_t
	# Redefine the plot
	lines.set_data(space, she_sample.state)
	# Set the new time
	time_text.set_text("Time = {:2.3f}".format(ani_time) )
	# We print the step we are in:
	sys.stdout.flush()
	sys.stdout.write("\r Step = {}".format(i))
	# And we do the next step:
	she_sample.do_step()
	return [lines,] + [time_text,]

# Time discretisation
delta_t = 1/1000
delta_x = 1/1000

# Space discretisation
space = np.arange(0.0, np.pi + 0.001, delta_x)
space_pts = len(space)

# We create a sample path
# with initial condition x0:
x0 = np.sin(space)
she_sample = she(x0)

# This is the resolvent of the laplacian matrix:
main_diag = np.ones(shape = (space_pts))
offu_diag = 0.5*(1/(1+2*(delta_t/delta_x**2)) -1)*np.ones(shape = (space_pts-1))
to_invert = scipy.sparse.diags([offu_diag, main_diag, offu_diag], [-1, 0, 1]).toarray()
resolvent = scipy.linalg.inv(to_invert)/(1+2*(delta_t/delta_x**2))

#We set up the picture
fig       = plt.figure()
ax        = plt.axes(xlim=(0, np.pi), ylim = (-5.0, 5.0))
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
lines,    = ax.plot([],[], lw = 2)
plt.title("Stannat") 

# We let the animation go.
ani       = animation.FuncAnimation(fig, animate, frames=600, interval = 70, blit = True)
ani.save(filename = 'stannat_SPDE.mp4', extra_args=['-vcodec', 'libx264'], bitrate = 7000)


# INSTRUCTION FOR PUTTING VIDEO IN PRESENTATION.

# 1) RUN: ffmpeg -i <input> -vf scale="trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -profile:v high -pix_fmt yuv420p -g 25 -r 25 output.mp4
#	 on powershell. The result (output.mp4) is the video you will use.
# 2)  IN Latex, with package movie9 write:
#   \includemedia[
#  width=0.7\linewidth,
#  totalheight=0.7\linewidth,
#  activate=onclick,
#  %passcontext,  %show VPlayer's right-click menu
#  addresource=ballistic_out.mp4,
#  flashvars={
#    %important: same path as in `addresource'
#    source=ballistic_out.mp4
#  }
#]{\fbox{Click!}}{VPlayer.swf}