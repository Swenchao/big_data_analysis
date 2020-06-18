'''
Created on 2020年5月29日

@author: 95108
'''
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from view_data import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

city_dict = {"广州" : 1, "东莞" : 2, "湛江" : 3 }

class LossHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs = {}):
        self.losses = []
        self.val_losses = []
        
    def on_batch_end(self, batch,  logs = {}):
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))

def load_data(filename_x, filename_y, incity):
    f_x = open(filename_x, 'r', encoding = 'utf-8-sig')
    f_y = open(filename_y, 'r', encoding = 'utf-8-sig')
    head_x = f_x.readline()
    head_y = f_y.readline()
    
    res_x, res_y = [], []
    while True:
        s_x = f_x.readline()
        if s_x == "": break
        info_x = s_x.split(sep = ',')
        city = info_x[1]
        
        info_x[2:7] = []
        info_x.pop(0)
        info_x[0] = city_dict[info_x[0]]
        
        s_y = f_y.readline()
        info_y = s_y.split(sep = ',')
        info_y = info_y[1]
        
        if incity == "All":
            res_x.append(info_x[:])
            res_y.append([info_y])
        elif city == incity:
            res_x.append(info_x[:])
            res_y.append([info_y])
    
    return head_x, np.asarray(res_x, np.float32), head_y, np.asarray(res_y, np.float32)

# 超参数设定
batch = 10
max_epoch = 20
h_floor = 1
h_activation = "relu"
out_activation = "sigmoid"
n_hidden = 50
incity = "All"
reducelr = False
dropout = False
dropout_rate = 0.5
deglitch = True

# 读入和处理数据
X_add = ["data/x.csv"]
Y_add = ["data/y.csv"]
X_features = ["city", "day", "metro","park", "school", "CBD_dist", "urban_rate", "house_age",
              "total_floor", "elevator","size", "living_room","washroom","chamber", "kitchen",
              "decoration_simple","decoration_exquisite","decoration_other","ori", "mid_stage",
              "high_stage","buy_res","loan_res","trans_res","aug_dp","aug_sup","aug_admin"]
Y_features = "unit_price"
_, X, _, Y = load_data(X_add[0], Y_add[0], incity)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

# show_heat_corr_map(X_train, X_features, Y_train, Y_features)

# Normalization
scaler = MinMaxScaler(feature_range = (0, 1))
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)
Y_train = scaler.fit_transform(Y_train)
Y_test = scaler.fit_transform(Y_test)

# 剔除异常值，deglitch
def remove_glitch(X_train, Y_train, X_test, Y_test, glitch_rate):
    delete_train = []
    for i in range(len(Y_train)):
        if Y_train[i, 0] > glitch_rate:
            delete_train.append(i)
    X_train = np.delete(X_train, delete_train, 0)
    Y_train = np.delete(Y_train, delete_train, 0)
    
    delete_test = []
    for i in range(len(Y_test)):
        if Y_test[i, 0] > glitch_rate:
            delete_test.append(i)
    X_test = np.delete(X_test, delete_test, 0)
    Y_test = np.delete(Y_test, delete_test, 0)
    return X_train, Y_train, X_test, Y_test
    
if deglitch:
    X_train, Y_train, X_test, Y_test = remove_glitch(X_train, Y_train, X_test, Y_test, 0.7)
        

# 定义测试集数据量和特征数
m = len(X_train)
n = 27

# 建立模型
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(n_hidden, input_dim = n, activation = h_activation))
if dropout:
    model.add(tf.keras.layers.Dropout(dropout_rate)) 
model.add(tf.keras.layers.Dense(1, activation = out_activation))
model.summary()

model.compile(loss = 'mean_squared_error', optimizer = 'adam', metrics = [tf.keras.metrics.RootMeanSquaredError()])
loss_before_train, _ = model.evaluate(X_train, Y_train)
loss_before_test, _ = model.evaluate(X_test, Y_test)

tensorboard = TensorBoard(log_dir = "graph")
def scheduler(epoch):
    if epoch % 5 == 0 and epoch != 0:
        lr = tf.keras.backend.get_value(model.optimizer.lr)
        tf.keras.backend.set_value(model.optimizer.lr, lr * 0.1)
        print("lr = {}".format(lr * 0.1))
    return tf.keras.backend.get_value(model.optimizer.lr)
reduce_lr = tf.keras.callbacks.LearningRateScheduler(scheduler)
# reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor = 'val_loss', 
#                                                  factor = 0.1, 
#                                                  patience = 5, 
#                                                  mode = 'min')
hist = model.fit(X_train, Y_train, validation_data = (X_test, Y_test),
                 epochs = max_epoch, batch_size = batch, verbose = 1,
                 callbacks = [tensorboard] + ([reduce_lr] if reducelr else []))

# plotting data
Y_test_pred = model.predict(X_test)
plt.plot(Y_test, Y_test_pred, 'ro', label = "")
plt.axis("equal")
# plt.axis([0,100000,0,100000])
plt.show()

loss = hist.history['loss']
val_loss = hist.history['val_loss']
loss.insert(0, loss_before_train)
val_loss.insert(0, loss_before_test)
plt.plot(range(max_epoch + 1), loss, 'bo', label = "loss")
plt.plot(range(max_epoch + 1), val_loss, 'ro', label = "val_loss")
plt.show()

# writing data
outfile = open("BP_Training_data/{0}_h_act_{1}_out_act_{2}_epoch_{3}_batch_{4}_reducelr_{5}_dropout_{6}_deglitch_{7}.csv".format(
    incity, h_activation, out_activation, max_epoch, batch, reducelr, dropout, deglitch), 'w', encoding = "utf-8-sig")
outfile.write("test_data,predict_data,epochs,loss,val_loss\n")
for i in range(max((len(Y_test), len(loss)))):
    if i >= len(loss):
        outfile.write(str(Y_test[i, 0]) + "," + str(Y_test_pred[i, 0]) + "\n")
    if i >= len(Y_test):
        outfile.write(",," + str(i) + "," + str(loss[i]) + "," + str(val_loss[i]) + "\n")
    if i < len(Y_test) and i < len(loss):
        outfile.write(str(Y_test[i, 0]) + "," + str(Y_test_pred[i, 0]) + "," +
                      str(i) + "," + str(loss[i]) + "," + str(val_loss[i]) + "\n")
outfile.close()    


if __name__ == '__main__':
    pass