import os
from ase import io

def wrfile(path ="" ):
    path = path
    datanames = os.listdir(path)
    list = []
    for i in datanames:
        if i.endswith('.xsd') == True:
            list.append(i)
    #print(list)
    #list = sorted(list)
    #list.sort(reverse=False)
    # listo = []
    # for i in range(1,(int(len(list))+1)):
    #     listo.append(f'{i}.xsd')
    return list
def convert(path = "",list = "",savepath = ""):
    lenfile = len(list)
    savepath = savepath
    for j in range(lenfile):
        k = list[j]
        i = k.split('.')[0]
        print(i)
        if os.path.isdir(os.path.join(savepath,f'{i}/POSCAR')) == True:
            break
        else:
            os.mkdir(os.path.join(savepath,f'{i}'))
            conv = openbabel.OBConversion()  # 使用openbabel模块中的OBConversion函数，用于文件格式转换的
            name = str(list[i][0]).split('/')[-1]
            conv.OpenInAndOutFiles(os.path.join(path, k), os.path.join(savepath,f'{i}/POSCAR'))  # 输入需要转换的文件的名字，以及定义转换后文件的文件名
            conv.SetInAndOutFormats("cif", "poscar")  # 定义转换文件前后的格式
            conv.Convert()  # 执行转换操作
            conv.CloseOutFile()  # 转换完成后关闭转换后的文件，完成转换

if __name__ == '__main__':
    pathwr = "/Users/user/Documents/Materials Studio Projects/dualatom_Files/Documents/dualatom2/10/add/vaspin"
    savepath = "/Users/user/Documents/Materials Studio Projects/dualatom_Files/Documents/dualatom2/10/add/vaspin"
    list = wrfile(path=pathwr)
    #print(list)
    with open( pathwr + 'log.log', 'a', encoding='utf-8') as f:
        for i in range(len(list)):
            values = list[i]
            #print(values)
            #print(key + "," + values + "\r")
            f.write(str(i+1) + "," + values + "\r")
        f.close()
    convert(path=pathwr,list=list,savepath=savepath)
    #print("hello")
