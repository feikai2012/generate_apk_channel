#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os,sys,hashlib
import getopt
import json
#源文件目录
inrootdir = ""
#输出文件目录
outrootdir = ""
#创建空列表
apklist = []
#创建空字符串json
jsonStr = ""
def Channel(chan):
    #print chan
    
    # 空文件 便于写入此空文件到apk包中作为channel文件每个渠道一行
    src_empty_file = 'info/xx.txt'
    # 创建一个空文件（不存在则创建）
    f = open(src_empty_file, 'w') 
    f.close()
    # 获取当前目录中所有的apk源包
    src_apks = []
    # python3 : os.listdir()即可，这里使用兼容Python2的os.listdir('.')
    for file in os.listdir(inrootdir):
        
        if os.path.isfile(os.path.join(inrootdir,file)):
            extension = os.path.splitext(os.path.join(inrootdir,file))[1][1:]
            if extension in 'apk':
                src_apks.append(os.path.join(inrootdir,file))
                
                for src_apk in src_apks:
                    # file name (with extension)
                    src_apk_file_name = os.path.basename(src_apk)
                    # 分割文件名与后缀
                    temp_list = os.path.splitext(src_apk_file_name)
                    # name without extension
                    src_apk_name = temp_list[0]
                    # 后缀名，包含.   例如: ".apk "
                    src_apk_extension = temp_list[1]
        
                    # 创建生成目录,与文件名相关
                    output_dir = outrootdir+'/output_' + src_apk_name + '/'
                    # 目录不存在则创建
                    if not os.path.exists(output_dir):
                           os.mkdir(output_dir)
					
                    target_apk = output_dir + src_apk_name + "-" + chan + src_apk_extension 
                    shutil.copy(src_apk, target_apk)
                    # zip获取新建立的apk文件
                    zipped = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
                    # 初始化渠道信息
                    empty_channel_file = "META-INF/channelname_{channel}".format(channel = chan)
                    # 写入渠道信息
                    zipped.write(src_empty_file, empty_channel_file)
                    # 关闭zip流
                    zipped.close()
					
                data = {}
                data['md5'] = GetFileMd5(target_apk)
                data['filename'] = src_apk_name + "-" + chan + src_apk_extension
                data['status'] = 1
                data['msg'] = 'success'
					
                apklist.append(data)
            else:
                 data = {}
                 data['md5'] = 0
                 data['filename'] = ''
                 data['status'] = 0
                 data['msg'] = 'nofind apkfile'
                 apklist.append(data)
        else:
             print 'unfind files'

def Version():
    print '1.0.0.1'


def Usage():
    print 'usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '--chan: qudao option '
    print '--filename: file md5 info '

#################MD5信息获取方法######################

#大文件的MD5值
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()    
#####################################################
def waitForExit(prompt = None):
	if prompt:
		print(prompt)
	raw_input()
	exit(0)


##############################################
def main(argv):
	cur_dir = os.path.dirname(__file__)
	#print('start build\n=======================')
	try:
		opts, args = getopt.getopt(argv[1:], 'hvmoc:', ['output=', 'foo=', 'fre='])
	except getopt.GetoptError, err:
		print('exctpion detected\n!!!!!!!!!!!!!!!!')
		print str(err)
		Usage()
		sys.exit(2)
		
	for o, a in opts:
		if o in ('-h', '--help'):
			Usage()
			sys.exit(2)
		elif o in ('-v', '--version'):
			Version()
			sys.exit(1)
		elif o in ('-c', '--chan'):
			Channel(argv[2])
			jsonStr = json.dumps(apklist)
			print jsonStr
			sys.exit(2)
		elif o in ('-m', '--filename'):
			data['md5']=GetFileMd5(argv[2])
			data['status']=0
			jsonStr = json.dumps(data)
		else:
			print 'unknon option'

	
	print('end build\n=======================')
	print('Done!')

##############################################
if __name__ == '__main__':
	try:
		main(sys.argv)
	except Exception,e:
		print(e)
		#traceback.print_exc()
	#finally:
	#	print 'Done!'
