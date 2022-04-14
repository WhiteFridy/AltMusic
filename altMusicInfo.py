"""
更改mp3文件名和封面
@Lunatic
"""

import os

import eyed3
from mutagen.id3 import ID3, APIC, TCOP, TOAL, COMM

"""
定位目标文件
@Lunatic
"""
def fileLocation():
    filePath = input("请输入需要更改的文件位置:")
    try:
        filelist = os.listdir(filePath)
    except:
        print('找不到指定路径,请重新输入')
        fileLocation()
    #print(filelist)
    """打印报错"""
    """
    此模块已在文件夹路径后加/，后面的path无需再加/，并剔除非mp3文件
    """
    filelist = []
    for dirs, dirnames, files in os.walk(filePath):
        for file in files:
            if file.endswith('.mp3'):
                filelist.append(dirs + '/' + file)
    """"""
    return filePath,filelist

"""
根据正则简易更改文件名并添加信息
@Luantic
"""
def deleAndAddUrl(path,filelist):

    sign = input("请输入需要筛选的正则符号,默认为'('：")
    if sign == '':
        sign = "("
    else:
        sign = sign
    chooseSign = input("请输入数字1&2选择是否需要添加Url？1：是   2：否\n")
    if chooseSign == '1':
        Url = input("请输入URL地址:")
    else:
        Url = ''
        print("不添加URL地址")
    #path=path+"/"
    for f in filelist:
        """
        if os.path.splitext(f)[1] == ".mp3":#剔除非mp3文件修改，考虑到隐藏文件问题（MAC）
            oldname=path+os.path.splitext(f)[0]+os.path.splitext(f)[1]#文件名
            prefixname=os.path.splitext(f)[0]#文件名前缀
            prefixname=prefixname.split(sign)[0]#根据正则获取文件名
            if Url != '':
                newname = path+prefixname+'['+Url+']'+os.path.splitext(f)[1]
            else:
                newname=path+prefixname+os.path.splitext(f)[1]#新文件名
            os.rename(oldname,newname)
            print(oldname+"->"+newname)
        else:
            print("包含MAC下的.DS_Store或非MP3文件")
            continue
        """
        oldname = os.path.splitext(f)[0] + os.path.splitext(f)[1]  # 文件名
        prefixname = os.path.splitext(f)[0]  # 文件名前缀
        prefixname = prefixname.split(sign)[0]  # 根据正则获取文件名
        if Url != '':
            newname = prefixname + '[' + Url + ']' + os.path.splitext(f)[1]
        else:
            newname = prefixname + os.path.splitext(f)[1]  # 新文件名
        os.rename(oldname, newname)
        print(oldname + "->" + newname)

#ID3v1
def setMp3V1Info(filelist):
    title = input("请输入标题：[直接回车默认为WWW.CN]:")
    artise = input("请输入作者：[直接回车默认为WWW.CN]:")
    if title == '':
        title = 'WWW.CN'
    else:
        title = title
    if artise == '':
        artise = 'WWW.CN'
    else:
        artise = title
    for f in filelist:
        file = os.path.splitext(f)[0] + os.path.splitext(f)[1]
        audiofile = eyed3.load(file)

        audiofile.tag.artist = artise  # 参与者
        audiofile.tag.album = ""  # 唱片集 因为乱码将专辑清空
        # audiofile.tag.album_artist = "Various Artists"#唱片集艺术家
        #audiofile.tag.title = title  # 标题
        # audiofile.tag.track="track"
        # audiofile.tag.genre="DJBASE"#音乐类型
        audiofile.tag.comment=""
        # audiofile.tag.performer="DJBASE"
        # audiofile.tag.image_url="Users/lunatic/Desktop/timg.png"
        # audiofile.tag.track_num = 3
        audiofile.tag.save()

#ID3v2
def setMp3Info(mp3file, info):
    songFile = ID3(mp3file)
    songFile['APIC'] = APIC(  # 插入封面
        encoding=3,
        mime='image/jpeg',
        type=3,#原有的是3
        #desc=u'Cover',
        data=info['picData']
    )
    songFile['COMM'] = COMM(  # 评论
        encoding=3,
        text=info['comm']
    )
    """
    songFile['TCOP'] = TCOP(    #版权信息Copyright
        enconding=3,
        text=info['tcop']
    )
    songFile['TOAL'] = TOAL(   #原始专辑
        enconding=3,
        text=info['toal']
    )
    songFile['COMM'] = COMM(    #评论
        encoding=3,
        text=info['comm']
    )
    
    songFile['TIT2'] = TIT2(  # 插入歌名对应track
          encoding=3,
          text=info['title']
      )
    songFile['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等-artist
          encoding=3,
          text=info['artist']
      )
    songFile['TALB'] = TALB(  # 插入专辑名-album
          encoding=3,
          text=info['album']
      )
      """
    songFile.save()

def putPic(filelist):
    picPath = input("请选择封面文件（简易300PX-500PX，PNG格式）：")
    with open(picPath, 'rb') as f:
        picData = f.read()
    for mp3file in filelist:
        newname = mp3file
        songtitle = newname.split('/')[-1][:12]
        info = {'picData': picData,
                'comm': ''
                }
        setMp3Info(mp3file, info)
        print("封面插入成功")

if __name__ == '__main__':
    filePath,fileList = fileLocation()#定位目标文件
    putPic(fileList)
    setMp3V1Info(fileList)
    deleAndAddUrl(filePath,fileList)
