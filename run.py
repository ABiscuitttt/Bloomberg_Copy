import time
from copydata_class import COPYDATA


#在开始之前注意检查彭博终端的初始状态
#1.全屏 且缩放比例为100% (一般不会改变)
#2.需要先进入任意一个指数的界面, 推荐MXCN Index, 因为总是有数据
#3.输入法需要是英文状态
#TODO 对这三项进行检测

def main():
    #read country formatted
    with open("country.csv") as f:
        country_list = list()
        for i in f.readlines():
            country_list.append(i.replace("\n",""))
    
    #do the copy
    for i in country_list:

        #准备阶段
        copydata_inst = COPYDATA(i)
        copydata_inst.set_index()
        time.sleep(3)
        copydata_inst.set_time()
        time.sleep(3)
        if copydata_inst.check_status() == False:
            print("init index check failed")
            return
        else:
            print("index check passed")
        
        copydata_inst.copy_loop(delay=1.5) 
    """
    delay参数的说明:
    参数显示了在输入日期并回车之后, 进行复制操作的间隔这主
    要是由于彭博客户端需要时间加载数据, 在发现彭博客户端跳
    转的速度比较快的时候, 可以适当减小该参数的值, 该参数默
    认值为3
    """    




if __name__ == "__main__":
    main()