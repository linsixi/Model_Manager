import os
from obs import ObsClient
#例子
"""   bucket_name = "qg23onnx"
    object_key = "Upload/0274ba1f-4efb-4ea3-ac8f-b09cf947e9cd.png"  # OBS中文件的完整路径
    local_folder = "download"  # 你希望保存下载文件的本地文件夹
"""

def upload_file(bucket_name, object_key, file_path, endpoint, ak, sk):
    """
    上传指定的OBS对象到本地文件夹。

    :param bucket_name: OBS桶名称
    :param object_key: OBS中对象的键
    :param file_path: 本地文件夹路径，上传文件的本地路径 folder
    :param endpoint: OBS服务终端节点
    :param ak: 访问密钥ID
    :param sk: 密钥访问密钥
    """
    # 创建ObsClient实例
    obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)

    try:
        # 执行上传操作
        obsClient.putFile(bucket_name, object_key, file_path=file_path)
        url = endpoint + "/" + object_key
        print(f"successful upload:{url}")
        return url
    except Exception as e:
        print(f"error：{e}")
