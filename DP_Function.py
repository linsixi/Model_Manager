import numpy as np


def generate_matrices(weight_matrix):
    """
    根据权重矩阵的形状生成自适应的矩阵 D 和 A。

    :param weight_matrix: 一维 NumPy 数组，表示权重矩阵
    :return: 自适应的 D 矩阵和 A 矩阵
    """
    size = weight_matrix.shape[0]

    # 生成 D 矩阵，假设 D 是对角矩阵，对角线元素为2
    D = np.diag(np.full(size, 2))

    # 生成 A 矩阵，假设 A 是一个简单的邻接矩阵
    A = np.zeros((size, size))
    for i in range(size - 1):
        A[i, i + 1] = 1
        A[i + 1, i] = 1

    h = 0.01  # 步长参数
    c_i = 1.0  # 常数
    q_i = 0.1  # 减小噪声幅度

    return D, A, h, c_i, q_i


def differential_privacy_update(weight_matrix, iteration=1):
    """
    使用差分隐私算法更新权重矩阵，并保持元素大小关系和相同大小元素的相同数值。

    :param weight_matrix: 一维 NumPy 数组，表示权重矩阵
    :param iteration: 当前迭代步数
    :return: 添加了差分隐私噪声并更新后的矩阵
    """
    # 根据 weight_matrix 生成自适应的 D 和 A 矩阵
    D, A, h, c_i, q_i = generate_matrices(weight_matrix)

    # 计算 L = D - A
    L = D - A

    # 更新 theta: theta(k + 1) = theta(k) - hLx(k) + S*eta(k)
    theta_k = weight_matrix
    x_k = theta_k.copy()

    # 计算 hLx(k)
    hLx_k = h * np.dot(L, x_k)

    # 计算 b_i(k) 并生成拉普拉斯噪声
    b_i_k = c_i * (q_i ** iteration)

    # 生成一个与 weight_matrix 大小一致的噪声数组，初始化为零
    eta_k = np.zeros_like(weight_matrix)

    # 处理相同值的元素，确保添加噪声后相同
    unique_values, indices = np.unique(weight_matrix, return_inverse=True)
    noise_dict = {}
    for i, value in enumerate(unique_values):
        noise = np.random.laplace(0, b_i_k)  # 对于每个唯一值生成一个噪声
        noise_dict[value] = noise  # 存储每个唯一值对应的噪声

    # 将生成的噪声应用到对应的索引位置
    for i in range(len(weight_matrix)):
        eta_k[i] = noise_dict[weight_matrix[i]]

    # 更新 theta
    theta_k_next = theta_k - hLx_k + eta_k

    # 保持大小关系与原始矩阵相同
    sorted_indices = np.argsort(weight_matrix)
    sorted_theta_k_next = np.sort(theta_k_next)

    # 使用排序后的噪声矩阵，按照原始矩阵的排序将其重新映射回去
    noisy_weight_matrix = np.zeros_like(weight_matrix)
    noisy_weight_matrix[sorted_indices] = sorted_theta_k_next

    # 确保相同值的元素在加噪声后仍然保持相同
    for value in unique_values:
        mask = weight_matrix == value
        noisy_weight_matrix[mask] = np.mean(noisy_weight_matrix[mask])

    return noisy_weight_matrix