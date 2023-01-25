import numpy as np
from copy import deepcopy
import cv2


class Clickertest(object):
    def __init__(self, clicks_list=None):
        self.clicks_list = clicks_list or []
        self.current_click_indx = 0

    def make_next_click(self, pred_mask):
        if self.current_click_indx < len(self.clicks_list):
            click = self.clicks_list[self.current_click_indx]
            self.current_click_indx += 1
            self.clicks_list.append(click)
    

    def get_clicks(self, clicks_limit=None):
        return self.clicks_list

    
    def add_click(self, click):
        coords = click.coords

        click.indx = self.click_indx_offset + self.num_pos_clicks + self.num_neg_clicks
        if click.is_positive:
            self.num_pos_clicks += 1
        else:
            self.num_neg_clicks += 1

        self.clicks_list.append(click)
        self.not_clicked_map[coords[0], coords[1]] = False





    def get_state(self):
        return deepcopy(self.clicks_list)

    def set_state(self, state):
        self.reset_clicks()
        for click in state:
            self.add_click(click)

    def __len__(self):
        return len(self.clicks_list)


class Click:
    def __init__(self, is_positive, coords, indx=None):
        self.is_positive = is_positive
        self.coords = coords
        self.indx = indx

    @property
    def coords_and_indx(self):
        return (*self.coords, self.indx)

    def copy(self, **kwargs):
        self_copy = deepcopy(self)
        for k, v in kwargs.items():
            setattr(self_copy, k, v)
        return self_copy
