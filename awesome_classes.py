class ResizeWithBB(transforms.Resize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self, img, bbs):
        prev_h, prev_w = img.shape[-2:]
        img = TF.resize(img, self.size, self.interpolation, self.max_size, self.antialias)
        new_h, new_w = img.shape[-2:]
        bbs = self.resize_bbs(bbs, prev_h, prev_w, new_h, new_w)
        return img, bbs

    @staticmethod   
    def resize_bbs(bbs, prev_h, prev_w, new_h, new_w):
        bbs[:,0] *= new_w/prev_w
        bbs[:,2] *= new_w/prev_w
        bbs[:,1] *= new_h/prev_h
        bbs[:,3] *= new_h/prev_h
        return bbs

class CenterCropWithBB(transforms.CenterCrop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self, img, bbs):
        image_height, image_width = img.shape[-2:]
        crop_height, crop_width = self.size
        

        if crop_width > image_width or crop_height > image_height:
            padding_ltrb = [
                (crop_width - image_width) // 2 if crop_width > image_width else 0,
                (crop_height - image_height) // 2 if crop_height > image_height else 0,
                (crop_width - image_width + 1) // 2 if crop_width > image_width else 0,
                (crop_height - image_height + 1) // 2 if crop_height > image_height else 0,
            ]

            image_new_height = image_height +  padding_ltrb[1] + padding_ltrb[3]
            image_new_width += image_width + padding_ltrb[0] + padding_ltrb[2]
            print("padding going on!")
            # image_width = get_dimensions(img)
            # if crop_width == image_width and crop_height == image_height: #TODO Not sure if this is important for bbox
            #     return img
        else:
            image_new_height = image_height
            image_new_width = image_width
        crop_top = int(round((image_new_height - crop_height) / 2.0))
        crop_left = int(round((image_new_width - crop_width) / 2.0))
        bbs = self.crop_bbs(bbs, crop_top, crop_left, crop_height, crop_width)
        img = TF.center_crop(img, self.size)
        return img, bbs
    @staticmethod
    def crop_bbs(bbs, crop_top, crop_left, crop_height, crop_width):
        for bb in bbs:
            bb[0] = max(crop_left, bb[0]) - crop_left # xmin
            bb[1] = max(crop_top, bb[1]) - crop_top # ymin
            bb[2] = min(crop_left+crop_width, bb[2]) - crop_left # xmax
            bb[3] = min(crop_top+crop_height, bb[3]) - crop_top # ymax
        return bbs

class RandomResizedCropWithBB(transforms.RandomResizedCrop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self, img, bbs):
        top, left, h, w = self.get_params(img, self.scale, self.ratio)
        img = TF.resized_crop(img, top, left, h, w, self.size, self.interpolation, antialias=self.antialias)
        bbs = CenterCropWithBB.crop_bbs(bbs, crop_top=top, crop_left=left, crop_height=h, crop_width=w)
        bbs = ResizeWithBB.resize_bbs(bbs, prev_h=h, prev_w=w, new_h=self.size[1], new_w=self.size[0])
        return img, bbs

class RandomHorizontalFlipWithBB(transforms.RandomHorizontalFlip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def forward(self, img, bbs):
        # Unlike RandomResizedCrop, this class didn't have get_params,
        # so we have to flip image manually to have access to random state.
        if torch.rand(1) < self.p:
            img = TF.hflip(img)
            w, h = img.shape[-2:]
            for bb in bbs:
                xmin, _, xmax, _ = bb
                bb[0] = w - xmax # new xmin is w - xmax
                bb[2] = w - xmin # new xmax is w - xmin
        return img, bbs
