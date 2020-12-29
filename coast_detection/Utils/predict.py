import os
import cv2
import numpy as np
import pandas as pd


"""
代码作用：
通过canny后的array，每个角度上找到一个边界点，通过多年历史数据（可选择）利用GM进行预测，最终输出多
张图片（可选择），并存储。
"""

class GM():
    def __init__(self, dt):
        self.df = np.array(dt, dtype=np.float32)

    def fit(self, dt):
        self.n = len(self.df)
        self.x, self.max_value = self.sigmod(self.df)
        z = self.next_to_mean(np.cumsum(self.x, axis=0))
        self.coef = self.coefficient(self.x, z)
        del z
        self.x0 = self.x[0]
        self.pre = self.pred()

    # 归一化
    def sigmod(self, x):
        maxv = max(x)
        return np.divide(x, maxv), maxv

    # 计算紧邻均值数列
    def next_to_mean(self, x_1):
        z = np.zeros(self.n - 1)
        for i in range(1, self.n):  # 下标从0开始，取不到最大值
            z[i - 1] = 0.5 * x_1[i] + 0.5 * x_1[i - 1]
        return z

    # 计算系数 a,b
    def coefficient(self, x, z):
        # 矩阵计算
        B = np.stack((-1 * z, np.ones(self.n - 1)), axis=1)
        Y = x[1:].reshape((-1, 1))
        # 返回的是a和b的向量转置，第一个是a 第二个是b；
        return np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Y)

    def pred(self, start=1, end=0):
        les = self.n + end
        resut = np.zeros(les)
        resut[0] = self.x0
        for i in range(start, les):
            resut[i] = (self.x0 - (self.coef[1] / self.coef[0])) * \
                       (1 - np.exp(self.coef[0])) * np.exp(-1 * self.coef[0] * (i))
        del les
        return resut

    # 计算绝对误差
    def confidence(self):
        return round(np.sum(np.abs(np.divide((self.x - self.pre), self.x))) / self.n, 4)

    # 预测个数，默认个数大于等于0，
    def predict(self, m=1, decimals=4):
        ypred = np.multiply(self.pre, self.max_value)
        ypred_ = np.zeros(1)
        if m < 0:
            return "预测个数需大于等于0"
        elif m > 0:
            ypred_ = np.multiply(self.pred(self.n, m)[-m:], self.max_value)
        else:
            return list(map(lambda _: round(_, decimals), ypred.numpy().tolist()))

        # cat 拼接 0 x水平拼接，1y垂直拼接
        result = np.concatenate((ypred, ypred_), axis=0)
        del ypred, ypred_
        return list(map(lambda _: round(_, decimals), result.tolist()))

"""
Draw函数：
输入：弧度值，canny后的array（灰度图），图的行，图的列，选定的原点
输出：两个列表[左侧弧度值，到原点的距离],[右侧弧度值，到原点的距离]（一条射线交到两个点）
"""

def Draw(theta, edge, row, col, origin0):
    i_0, j_0 = origin0[0], origin0[1]
    distance_l = []
    picked_dot_l = []
    j_min = int(max(0, min(j_0 + i_0 / np.tan(theta), j_0 - i_0 / np.tan(theta))))
    j_max = int(min(col - 1, max(j_0 + i_0 / np.tan(theta), j_0 - i_0 / np.tan(theta))))
    for j_k in np.arange(j_min, j_max + 1):
        i_k = int(i_0 - (j_k - j_0) * np.tan(theta))
        i_k1 = int(i_0 - (j_k + 1 - j_0) * np.tan(theta))

        if row > i_k >= 0 and row > i_k1 >= 0:
            picked_mat = edge[min(i_k, i_k1):max(i_k, i_k1) + 1, j_k:j_k + 2]
            # edge[min(i_k, i_k1):max(i_k, i_k1) + 1, j_k:j_k + 2] = 255
            # 每个矩阵去找最小距离
            if np.sum(picked_mat) > 0:
                distance_mat = np.zeros((max(i_k, i_k1) - min(i_k, i_k1) + 1, 2))
                for a in np.arange(min(i_k, i_k1), max(i_k, i_k1) + 1):
                    for b in np.arange(j_k, j_k + 2):
                        distance_mat[a - min(i_k, i_k1), b - j_k] = \
                            np.sqrt((a - origin0[0]) ** 2 + (b - origin0[1]) ** 2)
                flag_mat = np.where(picked_mat > 0, 1, 0)
                distance_mat *= flag_mat
                min_distance = np.min(np.where(distance_mat == 0, 10 ** 10, distance_mat))
                place = np.where(distance_mat == min_distance)
                picked_dot = [place[0][0] + min(i_k, i_k1), j_k]
                # 存储
                distance_l.append(min_distance)
                picked_dot_l.append(picked_dot)
    # 可能会有空列表，try + except一下避免报错
    try:
        left_dis_l = []
        left_dot_l = []
        right_dis_l = []
        right_dot_l = []
        left_theta_l = []
        right_theta_l = []
        for dot in picked_dot_l:
            if dot[1] < origin0[1]:
                left_dot_l.append(dot)
                left_dis_l.append(distance_l[picked_dot_l.index(dot)])
                left_theta_l.append(theta)
            else:
                right_dot_l.append(dot)
                right_dis_l.append(distance_l[picked_dot_l.index(dot)])
                right_theta_l.append(theta + np.pi)
        left_min_theta = left_theta_l[left_dis_l.index(min(left_dis_l))]
        right_min_theta = right_theta_l[right_dis_l.index(min(right_dis_l))]
        left_list = [left_min_theta, min(left_dis_l)]
        right_list = [right_min_theta, min(right_dis_l)]
        return left_list, right_list
    except:
        pass

def Predict(lines, row, col, num, pred_year, history_year, now_year, origin0):

    # 输入canny后的图片构成的dict
    times = [k[0:4] for k in lines.keys()]
    
    imgs = {}

    for k in times:
        
        idx_r, idx_c = lines[k]
        imgs[k] = np.zeros((row, col), dtype = np.uint8)
        imgs[k][idx_r, idx_c] = 255

    for time in imgs.keys():

        final_dict = {}  # 输出字典用于后续预测
        pred_df = pd.DataFrame(None)
        # 输入图片，进行canny，这里可以去掉，连接上一步直接调取变量即可
        img = imgs[time]
        
        # 描点
        a = 0
        for alpha in np.arange(0, np.pi, np.pi / num):
            try:
                left, right = Draw(alpha, img, row, col, origin0)
            except:
                left,right = [alpha, -1], [np.pi + alpha, -1]
                pass
            final_dict[left[0]] = left[1]
            final_dict[right[0]] = right[1]
            a += 1
            # print(a)
        pred_df['theta'] = final_dict.keys()
        pred_df[name_i] = final_dict.values()
    pred_df = pred_df.sort_values(by='theta')
    pred_df = pred_df[np.min(pred_df.iloc[:, 1:].values, axis=1) > 0]

    # 开始预测

    pred_dict = {}
    for i in range(len(pred_df['theta'].values)):
        theta_i = pred_df.iloc[i, 0]
        pred_x = pred_df.iloc[i, max(1, len(imgs) - history_year + 1):].values
        gm = GM(pred_x)
        try:
            gm.fit(pred_x)
            pred_conf = gm.confidence()
            pred = np.array(gm.predict(m=pred_year)[-pred_year:])
            if pred_x[0]==pred_x[1] and pred_x[0]==np.average(pred_x):
                pred_dict[theta_i] = np.average(pred_x) * np.ones(pred_year)
            else:
                pred_dict[theta_i] = pred
        except:
            pass

    for k in range(now_year + 1, now_year + pred_year + 1):
        j = 0
        new_array = np.zeros((row, col))
        lines_bold = {}
        for i in pred_dict.keys():
            try:
                x = np.rint(origin0[0] - pred_dict[i] * np.sin(i))
                y = np.rint(origin0[1] + pred_dict[i] * np.cos(i))
                x_k = int(x[k - now_year - 1])
                y_k = int(y[k - now_year - 1])
                new_array[x_k, y_k] = 255
                j += 1
            except:
                pass
        lines_bold[k] = np.where(new_array == 255)

#        edge_mod = np.zeros((row, col))
#        flag = new_array / 255
#        for i in range(3, row - 3):
#            for j in range(3, col - 3):
#                if np.sum(flag[i - 3:i + 4, j - 3:j + 4]) / 49 > 0.01:
#                    edge_mod[i, j] = 255

    return lines_bold

if __name__=='__main__':

    os.chdir(r"C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ")
    img_l = os.listdir(r'.\step2')

    num = 360  # 画多少条线
    pred_year = 3  # 预测多少年
    history_year = 4  # 用多少年进行预测
    now_year = 2020  # 今年
    pred_df = pd.DataFrame(None)
    origin0 = [1300, 1800]  # 这里可以替换坐标（e.g.用鼠标取点）

    Predict(img_l, num, pred_year, history_year, now_year, pred_df, origin0)
