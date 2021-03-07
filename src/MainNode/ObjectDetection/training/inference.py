"""
script to perform inference on trained models:
credit to https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/auto_examples/plot_object_detection_checkpoint.html
"""
from src.MainNode.Communication import main_node
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"   # need to supress GPU due to high memory usage
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import tensorflow as tf
import glob
# tf.get_logger().setLevel('ERROR')       # Suppress TensorFlow logging (2)
import time
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

def run_inference(PATH_TO_CFG: str, PATH_TO_CKPT: str, PATH_TO_LABELS: str, IMAGE_PATHS: str, OUTPUT_DIR: str, CKPT_NUM: str, oh_stream, pi_addresses) -> None:
    """
    This function is adapted *very closely* from:
    https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/auto_examples/plot_object_detection_checkpoint.html
    :param PATH_TO_CFG:
    :param PATH_TO_CKPT:
    :param PATH_TO_LABELS:
    :param IMAGE_PATHS:
    :param OUTPUT_DIR:
    :param CKPT_NUM:
    :return:
    """
    IMAGE_PATHS = glob.glob(IMAGE_PATHS)
    print('Loading model... ', end='')
    start_time = time.time()

    # Load pipeline config and build a detection model
    configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
    model_config = configs['model']
    detection_model = model_builder.build(model_config=model_config, is_training=False)

    # Restore checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(PATH_TO_CKPT, f'ckpt-{CKPT_NUM}')).expect_partial()

    @tf.function
    def detect_fn(image):
        """Detect objects in image."""

        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)

        return detections

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))

    # labelmap
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                        use_display_name=True)

    while True:
        # image_np = load_image_into_numpy_array(image_path)
        frame = oh_stream.getframe()
        input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        data = str(detections['num_detections']) + str(detections['detection_boxes'])
        # we will need to send this infor to all the diff PIs #
        for addr in pi_addresses:
            main_node.send(addr, data)






