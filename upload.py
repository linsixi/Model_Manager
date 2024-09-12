import os
from obs import ObsClient

# 例子
"""   bucket_name = "qg23onnx"
    object_key = "Upload/0274ba1f-4efb-4ea3-ac8f-b09cf947e9cd.png"  # OBS中文件的完整路径
    local_folder = "download"  # 你希望保存下载文件的本地文件夹
    https://qg23onnx.obs.cn-south-1.myhuaweicloud.com/output/as-nxprubxuwi.png # 需要的下载链接
    https://obs.cn-south-1.myhuaweicloud.com/output/as-nxprubxuwi.png # 返回的下载链接
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


def convert_upload_url(original_url, bucket_name):
    # 根据"obs.cn-south-1.myhuaweicloud.com"和"https://"分割URL
    split_feature = "https://"
    parts = original_url.split(split_feature)

    # 检查是否分割成功
    if len(parts) > 1:  # 判断有没有这个分割
        new_url = split_feature + bucket_name + '.' + parts[1]  # 拼接成新的URL
        return new_url
    else:
        print("上传函数的返回url分割失败")
        return None  # 如果分割失败，返回None或其他提示信息


# def convert_download_url(original_url, bucket_name):
#     # 根据"obs.cn-south-1.myhuaweicloud.com"和"https://"分割URL
#     split_feature = bucket_name
#     parts = original_url.split(split_feature+'.')
#     print(parts[0])
#     print(parts[1])
#     # 检查是否分割成功
#     if len(parts) > 1:  # 判断有没有这个分割
#         new_url = parts[0] + parts[1]  # 拼接成新的URL
#         return new_url
#     else:
#         print("下载函数的返回url分割失败")
#         return None  # 如果分割失败，返回None或其他提示信息


if __name__ == "__main__":
    url = "https://qg23onnx.obs.cn-south-1.myhuaweicloud.com/onnx/transformer-imdb.onnx"
    bucket_name = "qg23onnx"
    url = convert_download_url(url, bucket_name)
    print(url)
