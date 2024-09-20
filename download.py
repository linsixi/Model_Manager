import os
from obs import ObsClient


def download_file(bucket_name, object_key, local_folder, endpoint, ak, sk):
    """
    下载指定的OBS对象到本地文件夹。

    :param bucket_name: OBS桶名称
    :param object_key: OBS中对象的键
    :param local_folder: 本地文件夹路径，用于保存下载的文件
    :param endpoint: OBS服务终端节点
    :param ak: 访问密钥ID
    :param sk: 密钥访问密钥
    """
    # 创建ObsClient实例
    obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)

    # 确保本地文件夹存在
    if not os.path.exists(local_folder):
        os.makedirs(local_folder, exist_ok=True)

    # 构造本地文件的完整路径
    download_file_path = os.path.join(local_folder, os.path.basename(object_key))

    # 检查文件是否已经存在
    if os.path.exists(download_file_path):
        print(f"文件已存在：{download_file_path}")
        return str(download_file_path)

    try:
        # 执行下载操作
        obsClient.downloadFile(bucket_name, object_key, downloadFile=download_file_path)
        print(f"文件下载成功：{download_file_path}")
    except Exception as e:
        print(f"下载失败：{e}")

    return str(download_file_path)


def model_json_url(model_url, ):  # 例子onnx/transformer-imdb.onnx
    # 使用split方法分割字符串
    first_url = "model_json"
    split_name = model_url.split("/")[-1]  # 先按'/'分割，然后取最后一部分
    print(split_name)  # 输出: transformer-imdb.onnx
    # 去掉扩展名,#transformer-imdb
    without_extension = split_name.split('.')[0]
    final_url = first_url + '/' + without_extension + '.json'
    print(final_url)
    return final_url
