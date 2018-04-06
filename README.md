# Multiple 3D Volume Viewer
Short Python GUI built using Matplotlib to help visualize (in-shell) multiple 3D datasets and controlling their opacities.

## Purpose
I really built this viewer to be used in the Python shell while working with 3D imaging datasets and their segmentation masks.
Therefore, the best way to use this is to import the Python file into your code or session (I've used IPython and it's great) and view the datasets from there. It allow for anisotropy in the z-axis (generally the case for most medical images) to be resolved by a simple linear interpolation in that direction that's executed natively in the plotting code.

## Dependencies
- Numpy / Scipy
- Matplotlib

## Usage
`viewMultiple3Dseries.main( img, spacing=[1,1,1], cmap='gray' );`

`img:`      list of MxNxP dimensional `numpy` arrays.

`names:`    list of strings, with names[i] corresponding to the name of img[i].

`spacing:`  3x1 `numpy` array of the spacing in cases of anisotropy. Default is `[1, 1, 1]`.

`cmap:`     `matplotlib` colormap to use. Default is `"gray"`.

## Example
Here's a sample test case for you to try out. I would work in IPython since that's the environment that I've been working in. You should just be able to copy the code below and use `%paste` to see the results.
I also recommend that you normalize each image from 0 to 1 prior to viewing.

![alt text](screenshot.gif "Viewer in all it's glory.")

```
ipython
import matplotlib.pyplot as plt
from viewMultiple3Dseries import main as view
import numpy as np

plt.ion(); # Allow interactive mode so that we can work in the console while the plot is up.

# Note here that I'm creating sample data; what I've done for my projects has been to load up saved numpy arrays or use some external medical image dataset viewer and use them directly.
data = []
names = []
for i in range(0, 5):
  sampleData = np.random.rand( 100, 100, 100 )
  start = int(30+5*np.random.rand())
  end = int(50+10*np.random.rand())
  sampleData[ start:end, start:end, start:end ] = 3; # Create a box for our sample data.
  data.append(sampleData)
  names.append('Dataset: ' + str(i))

view( sampleData, names ); 
view( sampleData, spacing=[2, 1, 1], cmap='spectral' );
