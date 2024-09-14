import re
import torch
import numpy as np
import onnxruntime as ort


def load_vocab(vocab_path):
    vocab = {}
    with open(vocab_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:  # 确保行包含两个值
                word, idx = parts
                vocab[word] = int(idx)
    return vocab


def preprocess_text(text, vocab, pad_size):
    def tokenizer(text):
        # 去除标点符号并转换为小写
        text = re.sub(r'[^\w\s]', '', text).lower()
        return [tok for tok in text.split(" ") if tok]

    tokenized_text = tokenizer(text)
    vocab_dict = vocab
    max_l = pad_size

    def pad(x):
        return x[:max_l] if len(x) > max_l else x + [1] * (max_l - len(x))

    features = torch.tensor([pad([vocab_dict.get(word, 0) for word in tokenized_text])])
    return features


def predict(features, ort_session):
    ort_inputs = {ort_session.get_inputs()[0].name: features.numpy()}
    ort_outs = ort_session.run(None, ort_inputs)
    return ort_outs


# 使用主函数即可，传入字典地址，模型地址，输入文本，分词数量
def main_voc(vocab_path, onnx_model_path, input_text, pad_size=500):
    # 加载词典
    vocab = load_vocab(vocab_path)

    # 加载 ONNX 模型
    ort_session = ort.InferenceSession(onnx_model_path)

    # 预处理输入文本
    features = preprocess_text(input_text, vocab, pad_size)
    features = features.to(torch.int64)  # 确保输入是整数类型

    # 进行预测
    predictions = predict(features, ort_session)

    # 解码输出
    predicted_class = np.argmax(predictions[0], axis=1)
    print(f"Predicted class: {predicted_class[0]}")
    return predicted_class[0]


# if __name__ == "__main_voc__":
#     # 示例词典路径和模型路径
#     vocab_path = r'D:\qgsummer\QG_Summer_Camp\中期考核\vocab.txt'
#     onnx_model_path = r'D:\qgsummer\QG_Summer_Camp\中期考核\transformer-imdb.onnx'
#
#     # 示例输入文本
#     input_text = ("")
#
#     # 调用主函数
#     main_voc(vocab_path, onnx_model_path, input_text)
