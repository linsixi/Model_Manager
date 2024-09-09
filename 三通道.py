import mindspore
from mindspore import nn, context, Tensor
from mindspore.dataset import vision, transforms
import numpy as np
from PIL import Image
import os


context.set_context( mode = mindspore.GRAPH_MODE )

graph = mindspore.load( "AlexNet_flower.mindir")
model = nn.GraphCell( graph )


model.set_train(False)


def transform_image( img_path ):
    image = Image.open( img_path ).convert('RGB')
    image = np.array(image)

    transform = transforms.Compose( [
        vision.Resize((256, 256)),
        vision.Rescale(1.0 / 255.0, 0),
        vision.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        vision.HWC2CHW()
    ])
    image = transform(image)
    image = np.expand_dims(image, axis=0)

    image = Tensor( image, mindspore.float32 )
    return image

def get_prediction( img_path ):
    tensor = transform_image( img_path )
    outputs = model( tensor )
    predicted = outputs.argmax( axis=1 ).asnumpy().item()
    return predicted



# predictions = []
# test_folder_path = r'C:\Users\24468\Desktop\QG人工智能组\Python学习\实战\Lenet-5_MNIST.png'
# #test_names = os.listdir( test_folder_path )
# #for test_name in test_names:
# #    img_path = os.path.join( test_folder_path, test_name )
#     # print( img_path )
# pred = get_prediction( str(test_folder_path) )
# predictions.append( pred )
#
# print( predictions )
