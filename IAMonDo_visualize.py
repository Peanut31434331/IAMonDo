import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
trace_Info=[]

# 把每个正则出来的数字（可能含前缀）转变为坐标存储
def add_cord(num, cord_list, last_signal):
    # 如果前缀是单引号，则直接在上一个坐标上加上数值
    diff_map = {"'": 1, '"' : 2}
    if num[0] in diff_map:
        last_signal = diff_map[num[0]]
        num = num[1:]
    if last_signal == 1:
        cord_list.append(cord_list[-1] + float(num))
    elif last_signal == 2:
        cord_list.append(cord_list[-1] * 2 + float(num) - cord_list[-2])
    else:
        cord_list.append(float(num))
    return cord_list, last_signal


def IAMonDo_visualize(filename, min_trace=0, max_trace=-1):
    with open(filename, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'xml').find_all('trace')
    #从min_trace开始，到max_trace结束
    for i in range(min_trace, len(soup) if max_trace == -1 else max_trace):
        trace=soup[i]
        trace_list = trace.string.split(',')
        # X,Y存坐标信息。signal存最后一次前缀信息，0表示显式绝对值，1表示一级差值，2表示二级差值
        X = []
        Y = []
        X_signal = 0
        Y_signal = 0
        for tl in trace_list:
            a = re.sub(r'([\'"\-]+)', r' \1', tl)
            tl_xy = re.search(r'([\'"\-\d\.]+)[\s]+([\'"\-\d\.]+)', a).groups()
            X, X_signal = add_cord(tl_xy[0], X, X_signal)
            Y, Y_signal = add_cord(tl_xy[1], Y, Y_signal)
        #7种区分性很大的颜色
        color=['red','blue','green','yellow','grey','purple','orange']
            #{'Word', 'Correction', 'Marking_Angle', 'Marking_Bracket', 'Marking_Underline', 'Marking_Sideline', 'Drawing'}
        if(trace_Info[i]=='Word'):
            plt.plot(X, Y, color='red', linewidth='1')  
        # elif(trace_Info[i]=='Correction'):
        #     plt.plot(X, Y, color='blue', linewidth='1')
        # elif(trace_Info[i]=='Marking_Angle'):
        #     plt.plot(X, Y, color='green', linewidth='1')  
        # elif(trace_Info[i]=='Marking_Bracket'):
        #     plt.plot(X, Y, color='yellow', linewidth='1')  
        # elif(trace_Info[i]=='Marking_Underline'):
        #     plt.plot(X, Y, color='grey', linewidth='1')  
        # elif(trace_Info[i]=='Marking_Sideline'):
        #     plt.plot(X, Y, color='purple', linewidth='1')  
        # elif(trace_Info[i]=='Drawing'):
        #     plt.plot(X, Y, color='orange', linewidth='1')  
        else:
            plt.plot(X, Y, color='black', linewidth='2')
        
    
    plt.gca().invert_xaxis()
    plt.show()


def IAMonDo_getType(filename):
    with open(filename, 'r') as f:
        data = f.read()
    #将data以type="type"为分隔符分割成列表
    data_list = re.split(r'type="type"', data)
    #若列表中的元素包含"#t"，则打印出之后的字符直到"结束
    for i in data_list:
        if re.search(r'#t', i):
            #我只需要其中的数字，所以再次用findall提取数字
            index_of_trace=re.findall(r'\d+', i)
            #从i的头往后找，直到找到"</annotation>"，然后打印出">""</annotation>"之间的字符串
            type_of_trace=re.search(r'>.*</annotation>', i).group()
            for(j) in range(len(type_of_trace)):
                if(type_of_trace[j]=='<'):
                    type_of_trace=type_of_trace[1:j]
                    break
            #index_of_trace作为下标，打印出对应的type_of_trace
            for(j) in range(len(index_of_trace)):
                index_of_trace[j]=int(index_of_trace[j])
                trace_Info.append(type_of_trace)
    return 



if __name__ == '__main__':
    filename = r'./IAMonDo-db-1.0/002.inkml'
    IAMonDo_getType(filename)
    # trace_Info=set(trace_Info)
    # print(trace_Info)
    min_trace = 0
    max_trace = -1
    IAMonDo_visualize(filename, min_trace, max_trace)
    
   
