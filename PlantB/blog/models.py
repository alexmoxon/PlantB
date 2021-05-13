import warnings
warnings.filterwarnings('ignore')
from scipy import misc
from django.utils.text import slugify
from django.db import models
from django.core.files import File
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
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
from PIL import Image
from matplotlib import colors, ticker
from matplotlib.colors import LinearSegmentedColormap
import os

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    
    title = models.CharField(max_length=30)
    file = models.ImageField(null=True,blank=True,upload_to='Files')
    temp = models.FileField(null=True, blank=True, upload_to='Files/Converted')
    content = models.TextField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.temp = main(self.file)

        """self.file.url = file"""

        return super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

def approved_comments(self):
    return self.comments.filter(approved_comment=True)

class NDVI(object):

    def __init__(self, file_path):
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

        output_name = "NDVI"

        fig, ax = plt.subplots()
        image = ax.imshow(NDVI, cmap=self.create_colormap(*self.colors))
        plt.axis('off')

        self.create_colorbar(fig, image)

        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        img = Image.open(file_path)
        fig.savefig(output_name, dpi = 600, transparent=True, bbox_inches=extent, pad_inches=0)
        plt.show()
        plt.close()
        """
        image = plt.imread(file_path)
        imgplot = plt.show(fig)
        temp = imgplot
        Post.objects.instance.save()"""


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



def main(file):

    blue_ndvi = NDVI(file)
    blue_ndvi.convert(file)