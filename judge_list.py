import json

# 定义错误ID字典
error_dict = {
    0: "可正常运行",
    1: "大模型只能放在工作流的结尾，请修改工作流",
    2: "工作流中没有模型智能体"
}


def check_model_list(data):
    # 确保 'modelList' 存在且不为空
    model_list = data.get('modelList', None)
    if not isinstance(model_list, list) or len(model_list) == 0:
        return {'error_id': 2, 'message': error_dict[2]}

    # 遍历每个层的模型
    for idx, layer in enumerate(model_list):
        # 确保 'models' 存在并且是列表
        models = layer.get('models', [])
        if not isinstance(models, list):
            return {'error_id': 2, 'message': error_dict[2]}

        for model in models:
            # 检查isAPI是否等于1（是否为大模型）
            if model.get('isAPI', 0) == 1:
                # 如果大模型不是最后一层，则返回错误ID 1
                if idx != len(model_list) - 1:
                    return {'error_id': 1, 'message': error_dict[1]}

    # 如果没有错误，返回 errorId = 0
    return {'error_id': 0, 'message': error_dict[0]}


# 示例使用
if __name__ == "__main__":
    # JSON输入
    json_input = {
      "content":"",
      "image":"https://qg23onnx.obs.cn-south-1.myhuaweicloud.com/Upload/6c669115-07f1-446c-afbc-159013adb177.png",
      "modelList": [
        {
          "layer": 1,
          "parallel": 1,
          "models": [
            {
              "modelName": "resnet50-CLDC.onnx",
              "modelUrl": "https://obs.cn-south-1.myhuaweicloud.com/onnx/resnet50-CLDC.onnx",
              "isAPI": 1,
              "weight":1
            },
            {
              "modelName": "resnet50-CLDC.onnx",
              "modelUrl": "https://obs.cn-south-1.myhuaweicloud.com/onnx/resnet50-CLDC.onnx",
              "isAPI": 0,
              "weight":1
            }
          ]
        },
        {
          "layer": 2,
          "parallel": 0,
          "models": [
            {
              "modelName": "Stable-Diffusion-XL",
              "modelUrl": "get_qianfan_graph",
              "isAPI": 0,
              "weight":1,
              "question": "请添加提示词，比如描述这张图片"
            }
          ]
        }
      ],
      "answer":"",
      "error" :""
    }

    result = check_model_list(json_input)
    print(result)
