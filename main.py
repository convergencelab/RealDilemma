from src.main_node.Utils import OverHead
from src.main_node.Utils.stream_oh_inference import run

def main():
    oh_stream = OverHead()
    """ for model we can choose any one we already have downloaded
    model_dict = {
        # 'ssd_resnet50_v1_fpn_640x640_coco17_tpu-8': 9,
        # 'faster_rcnn_inception_resnet_v2_640x640_coco17_tpu-8': 2,
        # 'centernet_resnet50_v1_fpn_512x512_coco17_tpu-8': 2,
        # 'efficientdet_d0_coco17_tpu-32': 3,
        'ssd_mobilenet_v2_320x320_coco17_tpu-8': 3
    }"""
    #model = ('ssd_mobilenet_v2_320x320_coco17_tpu-8', 3)
    #run(model, oh_stream)

if __name__ == "__main__":

    main()


    
