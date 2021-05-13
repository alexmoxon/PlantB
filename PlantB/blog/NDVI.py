"""
Creates a NIR image from .jpg upload by filtering out the blue bands.
Provides a custom bar to help users understand healthiness of plant.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_web_app.settings')
import warnings
warnings.filterwarnings('ignore')
from django.core.files.images import ImageFile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os.path
from matplotlib import colors, ticker
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image as Img
from .models import Post

class NDVI(object):

    def __init__(self, file_path):
        self.output_name = "NDVI"
        """suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")"""
        self.image = plt.imread(file_path)
        """self.output_name = "_".join([basename, suffix])"""
        self.colors = ['gray', 'gray', 'red', 'yellow', 'green']

    def create_colormap(self, *args):
        return LinearSegmentedColormap.from_list(name='custom1', colors=args)

    def create_colorbar(self, fig, image):
        position = fig.add_axes([0.125, 0.19, 0.2, 0.05])
        norm = colors.Normalize(vmin=-1., vmax=1.)
        cbar = plt.colorbar(image,
                            cax=position,
                            orientation='horizontal',
                            norm=norm)
        cbar.ax.tick_params(labelsize=6)
        tick_locator = ticker.MaxNLocator(nbins=3)
        cbar.locator = tick_locator
        cbar.update_ticks()
        cbar.set_label("NDVI", fontsize=10, x=0.5, y=0.5, labelpad=-25)

    def convert(self, file_path):
        """
        NDVI calculation and mapped colors
        """
        NIR = (self.image[:, :, 0]).astype('float')
        blue = (self.image[:, :, 2]).astype('float')
        green = (self.image[:, :, 1]).astype('float')
        bottom = (blue - green) ** 2
        bottom[bottom == 0] = 1  
        VIS = (blue + green) ** 2 / bottom
        NDVI = (NIR - VIS) / (NIR + VIS)

        fig, ax = plt.subplots()
        image = ax.imshow(NDVI, cmap=self.create_colormap(*self.colors))
        plt.axis('off')

        self.create_colorbar(fig, image)

        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        m = Post.objects.create()
        m.temp = fig.savefig(self.output_name, output_type = 'file', dpi = 600, transparent=True, bbox_inches=extent, pad_inches=0)
        m.save()
        """
        new = fig.savefig(self.output_name, output_type = 'file', dpi = 600, transparent=True, bbox_inches=extent, pad_inches=0)
        figure = io.BytesIO()
        new.get_figure().savefig(figure, format='png')
        image_file = ImageFile(new)
        return image_file"""

        """fig = Img.fromarray(fig.gca(), 'RGB')"""
        """output_file = StringIO()
        f = Img.open(fig)
        f.convert('RGB')
        f.save(self.output_name, upload_location = "PlantB/media/Files")
        fig = io.BytesIO()
        plt.savefig(fig, format="png")"""
        temp = fig.savefig(self.output_name, output_type='file', dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)


def main(request):

    blue_ndvi = NDVI(request)
    blue_ndvi.convert(request)
