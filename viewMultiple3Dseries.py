import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import zoom
from matplotlib.widgets import Slider

def main(img, names, spacing=[1, 1, 1], cmap='gray'):

    # Input image is a list of images, list of names for each of the images. Note that 'base' image will be the 0th indexed image.

    # Equalize the spacing in the image by zooming.
    # Also, let's just assume that the spacing is really problematic in z...so let's keep z at the original spacing.
    spacing = np.array(spacing)
    spacing = spacing/spacing.min()
    spacing = np.round_(spacing)
    imgZoom = []
    for i in range(0, len(img)):
        imgZoom.append( zoom(img[i], spacing, order=1) )

    axcolor = 'white'
    alpha0 = 0.1

    # Create our layout and add the images.
    fig = plt.figure(figsize=(18,6))
    fig.add_axes([0, 0.2, 0.25, 0.7])
    fig.add_axes([0.25, 0.2, 0.25, 0.7])
    fig.add_axes([0.5, 0.2, 0.25, 0.7])
    for ax in fig.axes:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    ax = fig.axes
    val0z = int(img[0].shape[0]/2)
    val0y = int(imgZoom[0].shape[1]/2)
    val0x = int(imgZoom[0].shape[2]/2)
    for i in range(0, len(img)):
        imgPlotz = ax[0].imshow(img[i][val0z, :, :], cmap=cmap, interpolation='nearest', vmin=img[0].min(), vmax=img[0].max(), alpha=alpha0)
        imgPloty = ax[1].imshow(imgZoom[i][-1::-1, val0y, :], cmap=cmap, interpolation='nearest', vmin=img[0].min(), vmax=img[0].max(), alpha=alpha0)
        imgPlotx = ax[2].imshow(imgZoom[i][-1::-1, :, val0x], cmap=cmap, interpolation='nearest', vmin=img[0].min(), vmax=img[0].max(), alpha=alpha0)


    axImgs = ax[0].get_images()
    crImgs = ax[1].get_images()
    sgImgs = ax[2].get_images()

    # Now, add our layout content.
    layerHeader = fig.add_axes([0.76, 0.8, 0.23, 0.1], axisbg = 'white')

    # Set up our layer box
    layerHeader.text(0.5, 0.5,'Layers', horizontalalignment='center', verticalalignment='center', transform=layerHeader.transAxes, fontsize=16)
    layerHeader.xaxis.set_visible(False)
    layerHeader.yaxis.set_visible(False)
    layerContainerWidth = 0.21
    if len(img) > 5:
        layerTextContainerHeight = 0.375/(len(img))
        layerOpacContainerHeight = 0.375/(len(img))
    else:
        layerTextContainerHeight = 0.05;
        layerOpacContainerHeight = 0.05;

    layerTextHeightStart = 0.79 - layerTextContainerHeight
    layerOpacHeightStart = (layerTextHeightStart) - layerOpacContainerHeight

    opacitySliders = []

    # Create opacity slider class.
    class OpacitySlider(object):
        def __init__(self, axes, refimg):
            self.refimg = refimg
            self.slider = Slider(sliderAx, 'O', 0, 1, valinit=alpha0)
            self.slider.on_changed(self.updateOpacity)

        def updateOpacity(self, newOpacity):
            axImgs[self.refimg].set_alpha(newOpacity)
            crImgs[self.refimg].set_alpha(newOpacity)
            sgImgs[self.refimg].set_alpha(newOpacity)
            fig.canvas.draw_idle()

    for i in range(0, len(img)):
        # Create text axis.
        textAx = fig.add_axes([0.76, layerTextHeightStart, layerContainerWidth, layerTextContainerHeight])
        textAx.xaxis.set_visible(False)
        textAx.yaxis.set_visible(False)
        textAx.text(0.5, 0.5, names[i], horizontalalignment='center', verticalalignment='center', transform=textAx.transAxes)

        # Create opacity scale axis.
        sliderAx = fig.add_axes([0.76, layerOpacHeightStart, layerContainerWidth, layerOpacContainerHeight], axisbg='white')
        sliderAx.xaxis.set_visible(False)
        sliderAx.yaxis.set_visible(False)
        opacSlider = OpacitySlider(sliderAx, i)
        opacitySliders.append( opacSlider )

        # Adjust positions for subsequent textbox/slider addition.
        layerTextHeightStart = layerOpacHeightStart - layerTextContainerHeight
        layerOpacHeightStart = (layerTextHeightStart) - layerOpacContainerHeight


    # Create image sliders
    zslidaxis = fig.add_axes([0.035, 0.05, 0.18, 0.07], axisbg=axcolor)
    zslider = Slider(zslidaxis, 'Z:', 1, img[0].shape[0], valinit=val0z, valfmt='%0.0f')
    yslidaxis = fig.add_axes([0.285, 0.05, 0.18, 0.07], axisbg=axcolor)
    yslider = Slider(yslidaxis, 'Y:', 1, imgZoom[0].shape[1], valinit=val0y, valfmt='%0.0f')
    xslidaxis = fig.add_axes([0.535, 0.05, 0.18, 0.07], axisbg=axcolor)
    xslider = Slider(xslidaxis, 'X:', 1, imgZoom[0].shape[2], valinit=val0x, valfmt='%0.0f')

    # Set update functions for changes in slider marker position.
    def updatez(valz):
        slicez = zslider.val - 1
        for i in range(0, len(img)):
            axImgs[i].set_data(img[i][np.round_(slicez).astype('int'), :, :])
        fig.canvas.draw_idle()
    def updatey(valy):
        slicey = yslider.val - 1
        for i in range(0, len(img)):
            crImgs[i].set_data(imgZoom[i][-1::-1, np.round_(slicey).astype('int'), :])
        fig.canvas.draw_idle()
    def updatex(valx):
        slicex = xslider.val - 1
        for i in range(0, len(img)):
            sgImgs[i].set_data(imgZoom[i][-1::-1, :, np.round_(slicex).astype('int')])
        fig.canvas.draw_idle()

    # Turn on our sliders and show the plot.
    zslider.on_changed(updatez)
    yslider.on_changed(updatey)
    xslider.on_changed(updatex)
    plt.show()

    # For reasons not worth going into here, we have to return these values so that we can run these plots in the python shell...
    return fig, opacitySliders
