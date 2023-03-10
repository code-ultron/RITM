from time import time

import numpy as np
import torch

from isegm.inference import utils
from isegm.inference.clicker import Clicker
from isegm.inference.clicker import Click
from isegm.inference.clickertest import Clickertest
try:
    get_ipython()
    from tqdm import tqdm_notebook as tqdm
except NameError:
    from tqdm import tqdm


def evaluate_dataset(dataset, predictor, **kwargs):
    all_ious = []

    start_time = time()
    for index in tqdm(range(len(dataset)), leave=False):
        sample = dataset.get_sample(index)

        _, sample_ious, _ = evaluate_sample(sample.image, sample.gt_mask, predictor,
                                            sample_id=index, **kwargs)
        all_ious.append(sample_ious)
    end_time = time()
    elapsed_time = end_time - start_time

    return all_ious, elapsed_time


def evaluate_sample(image, gt_mask, predictor, max_iou_thr,
                    pred_thr=0.49, min_clicks=1, max_clicks=20,
                    sample_id=None, callback=None):
    clicker = Clicker(gt_mask=gt_mask)
    pred_mask = np.zeros_like(gt_mask)
    ious_list = []

    with torch.no_grad():
        predictor.set_input_image(image)

        for click_indx in range(max_clicks):
            clicker.make_next_click(pred_mask)
            pred_probs = predictor.get_prediction(clicker)
            pred_mask = pred_probs > pred_thr

            if callback is not None:
                callback(image, gt_mask, pred_probs, sample_id, click_indx, clicker.clicks_list)

            iou = utils.get_iou(gt_mask, pred_mask)
            ious_list.append(iou)

            if iou >= max_iou_thr and click_indx + 1 >= min_clicks:
                break

        return clicker.clicks_list, np.array(ious_list, dtype=np.float32), pred_probs


def evaluate_test(image, predictor,img_type
                    ):
    
    if img_type == 1:
        # (y,x) coordinate format
        init_clicks = [Click(is_positive=True, coords=(1850, 200)),
               Click(is_positive=True, coords=(1850, 1000)),
               Click(is_positive=True, coords=(1250, 200)),
               Click(is_positive=True, coords=(1250, 1500)),
               Click(is_positive=True, coords=(500, 200)),
               Click(is_positive=True, coords=(500, 1200)),
               Click(is_positive=True, coords=(500, 2000)),
               Click(is_positive=False, coords=(50, 50)),
               Click(is_positive=False, coords=(250, 2500)),
               Click(is_positive=False, coords=(1900, 1900))]
    
    elif img_type == 2:
        # (y,x) coordinate format
        init_clicks = [
               Click(is_positive=True, coords=(50,1000)),
               Click(is_positive=True, coords=(50,2500)),
               Click(is_positive=True, coords=(1850, 200)),
               Click(is_positive=True, coords=(1850, 1000)),
               Click(is_positive=True, coords=(1250, 200)),
               Click(is_positive=True, coords=(1250, 1500)),
               Click(is_positive=True, coords=(500, 200)),
               Click(is_positive=True, coords=(500, 1100)),
               Click(is_positive=True, coords=(500, 2100)),
               Click(is_positive=False, coords=(1750, 1500)),
               Click(is_positive=False, coords=(1000, 2100)),
               Click(is_positive=False, coords=(325, 2590)),
               Click(is_positive=False, coords=(1900, 1900))]
        
               
        
   
    
    clicker = Clicker(init_clicks=init_clicks)
    with torch.no_grad():
        predictor.set_input_image(image)

        
        pred_probs = predictor.get_prediction(clicker)


        return clicker.clicks_list, pred_probs
