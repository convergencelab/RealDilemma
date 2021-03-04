from src.main_node.ObjectDetection.training.inference import run_inference
LABELMAP: str = r"src/ObjectDetection/data/training/annotations/label_map.pbtxt" # to be used for model inference
IMG_DIR: str = r"src/ObjectDetection/data/inference/*"

def run(model, oh_stream):
    """
    run the inference function for the object detection model
    :param model:
    :param oh_stream:
    :return:
    """
    output_dir = f"src/ObjectDetection/data/training/models/{model[0]}/test/"
    config = f"src/ObjectDetection/data/training/models/{model[0]}/pipeline.config"
    ckpt = f"src/ObjectDetection/data/training/models/{model[0]}/out-of-box/ckpt/"
    run_inference(PATH_TO_CFG=config,
                  PATH_TO_CKPT=ckpt,
                  PATH_TO_LABELS=LABELMAP,
                  IMAGE_PATHS=IMG_DIR,
                  OUTPUT_DIR=output_dir,
                  CKPT_NUM=model[1],
                  oh_stream=oh_stream)


