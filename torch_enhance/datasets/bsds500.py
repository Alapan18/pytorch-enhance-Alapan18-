import os
import shutil
import glob
from torchvision.transforms import Compose, CenterCrop, ToTensor, Resize

from .common import BSDS500_URL, DatasetFolder
from .utils import download_and_extract_archive


class BSDS500(object):
    def __init__(
        self,
        scale_factor=2,
        image_size=256,
        data_dir=os.path.join(os.getcwd(), 'data'),
        color_space='RGB'
    ):
        self.scale_factor = scale_factor
        self.image_size = image_size
        self.root_dir = os.path.join(data_dir, 'BSDS500')
        self.color_space = color_space
        self.extensions = ['.jpg']
        self.url = BSDS500_URL

        self.crop_size = self.image_size - (self.image_size % self.scale_factor)

        self.download(data_dir)

        self.input_transform = Compose(
            [
                CenterCrop(self.crop_size),
                Resize(self.crop_size // self.scale_factor),
                ToTensor(),
            ]
        )

        self.target_transform = Compose([CenterCrop(self.crop_size), ToTensor()])

    def download(self, data_dir):

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
            
            download_and_extract_archive(self.url, data_dir, remove_finished=True)

            # Tidy up
            for d in ['train', 'val', 'test']:
                shutil.move(src=os.path.join(data_dir, 'BSR/BSDS500/data/images', d),
                            dst=self.root_dir)
                os.remove(os.path.join(self.root_dir, d, 'Thumbs.db'))
                
            shutil.rmtree(os.path.join(data_dir, 'BSR'))

    def get_dataset(self, set_type='train'):

        assert set_type in ['train', 'val', 'test']
        root_dir = os.path.join(self.root_dir, set_type)
        return DatasetFolder(
            data_dir=root_dir,
            input_transform=self.input_transform,
            target_transform=self.target_transform,
            color_space=self.color_space,
            extensions=self.extensions,
        )
