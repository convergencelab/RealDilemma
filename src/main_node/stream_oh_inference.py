from ObjectDetection.OverHead import OverHead
from ObjectDetection.training.inference import run_inference
LABELMAP: str = r"src/ObjectDetection/data/training/annotations/label_map.pbtxt" # to be used for model inference
IMG_DIR: str = r"src/ObjectDetection/data/inference/*"

if __name__ == "__main__":
    oh_stream = OverHead()

    model_dict = {
        # 'ssd_resnet50_v1_fpn_640x640_coco17_tpu-8': 9,
        # 'faster_rcnn_inception_resnet_v2_640x640_coco17_tpu-8': 2,
        # 'centernet_resnet50_v1_fpn_512x512_coco17_tpu-8': 2,
        # 'efficientdet_d0_coco17_tpu-32': 3,
        'ssd_mobilenet_v2_320x320_coco17_tpu-8': 3
    }
    for model in model_dict.keys():
        output_dir = f"src/ObjectDetection/data/training/models/{model}/test/"
        config = f"src/ObjectDetection/data/training/models/{model}/pipeline.config"
        ckpt = f"src/ObjectDetection/data/training/models/{model}/out-of-box/ckpt/"
        run_inference(PATH_TO_CFG=config,
                      PATH_TO_CKPT=ckpt,
                      PATH_TO_LABELS=LABELMAP,
                      IMAGE_PATHS=IMG_DIR,
                      OUTPUT_DIR=output_dir,
                      CKPT_NUM=model_dict[model],
                      oh_stream=oh_stream)