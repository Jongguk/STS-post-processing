import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import tkinter as tk
from tkinter import filedialog
from matplotlib.widgets import Slider

# Set the style of the plot using Seaborn
sns.set_style("whitegrid")

# Open a dialog box to select a folder
root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()

# Find all .asc files in the selected folder
file_pattern = path + "/*.asc"
file_list = glob.glob(file_pattern)

# Initialize to import data
data_list_fwd = []
data_list_bwd = []
data_list = []

# Import data from selected folder
for filename in file_list:
    data = np.loadtxt(filename)
    df = pd.DataFrame(data, columns=['x', 'y'])
    data_list.append(df) # Add data
    data_list_fwd.append(df[:300]) # Add separately forward and backward scan
    data_list_bwd.append(df[300:])

df_all = pd.concat(data_list)
df_fwd_all = pd.concat(data_list_fwd)
df_bwd_all = pd.concat(data_list_bwd)

# Average all data
df_avg = df_all.groupby('x')['y'].mean().reset_index()

# Export the averaged data to a CSV file
df_avg.to_csv(path + '/averaged_data.csv', index=False)

# Create the figure and axis objects
fig, ax = plt.subplots(figsize=(10, 7))

# Adjust the padding around the subplots
plt.subplots_adjust(bottom=0.3, left=0.2, right=0.9, top=0.9)

# Create the initial plots
l_fwd = ax.scatter(df_fwd_all['x'], df_fwd_all['y'], label='forward scan')
l_bwd = ax.scatter(df_bwd_all['x'], df_bwd_all['y'], label='backward scan')
l_avg = ax.plot(df_avg['x'], df_avg['y'], label = 'averaged data', color = 'red')

# Draw figure
ax.legend()
ax.set_xlabel("Voltage (V)")
ax.set_ylabel("Current (A)") # uA? nA? pA? !!Please check!!

# Define the sliders
ax_transparent = plt.axes([0.2, 0.10, 0.65, 0.03])
s_transparent = Slider(ax_transparent, 'Transparent', 0, 1, valinit=1)

# Create a function to update the plot based on the slider values
def update(val):
    # Get the slider values
    transparent = s_transparent.val
    
    # Update the plot
    l_fwd.set_alpha(transparent)
    l_bwd.set_alpha(transparent)
            
    plt.draw()

# Connect the sliders to the update function
s_transparent.on_changed(update)

plt.show()