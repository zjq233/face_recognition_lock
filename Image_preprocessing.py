import cv2,math,os

#计算两眼距离函数
def Distance(p1,p2):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	return math.sqrt(dx*dx+dy*dy)

'''
定义人脸图像的几何变换函数，一共5个参数，第一个为要变换的图片;
第二，三个参数分别为左眼和右眼的坐标;
第四个参数为左眼睛到图像边界的距离与图片长宽之比，默认都为0.;
第五个参数为处理后图像的大小,默认为（150，150）
'''

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (150,150)):
	offset_h = math.floor(float(offset_pct[0]) * dest_sz[0])
	offset_v = math.floor(float(offset_pct[1]) * dest_sz[1])
	eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
#求旋转角度，并将弧度转角度
	rotation=180/math.pi*math.atan2(float(eye_direction[1]),float(eye_direction[0]))
#求两眼之间的距离
	dist = Distance(eye_left, eye_right)
 #求原图片（或旋转后图片）与处理后图像缩放的比例
	reference = dest_sz[0] - 2.0*offset_h
	scale = float(dist)/float(reference)
 #求图像旋转的变换矩阵
	M = cv2.getRotationMatrix2D( eye_left,rotation,1)
 #求出旋转后的图像
	image1=cv2.warpAffine(image,M,image.shape)
#求出最终图像起点在旋转后图像的坐标
	crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
#求出最终图像在旋转后图像所在区域长和宽
	crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
#剪裁出有效最终图像在旋转后图像的区域
	image2=image1[int(crop_xy[1]):int(crop_xy[1]+crop_size[1]),int(crop_xy[0]):int(crop_xy[0]+crop_size[0])]
#缩放图像到设定的大小
	image3 = cv2.resize(image2, dest_sz)
#返回处理完成的图像
	return image3

#返回数列第一个值，用于下面函数筛选
def takeSecond(elem):
	return elem[0]
#定义函数为进行单张图片的归一化处理函数
def yuchuli(image):
	#用眼睛检测分类器
	eyeCascade= cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
	  #读为灰度图像
	img_numpy = cv2.imread(image,0)
	   #图像直方图均衡化处理
	dst = cv2.equalizeHist(img_numpy)
	   #眼睛检测
	eyes = eyeCascade.detectMultiScale(dst)
	eye=[]
		#获取有效的眼睛坐标和处理
	if len(eyes)==2:
		eye.append((math.floor((eyes[0,0]+eyes[0,2]/2)),math.floor((eyes[0,1]+eyes[0,3]/2))))
		eye.append((math.floor((eyes[1,0]+eyes[1,2]/2)),math.floor((eyes[1,1]+eyes[1,3]/2))))
		eye.sort(key=takeSecond)
		image1=CropFace(dst,eye[0],eye[1],offset_pct=(0.2,0.2), dest_sz=(150,150))
		return 1,image1
    else:
        return 0,0

#图像的批量归一化处理函数
def Guiyi(path1):
   #人脸库所在路径并一张一张的图片读取
	path = path1
	imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
	print(len(imagePaths))
	for imagePath in imagePaths:
		try:
			image=yuchuli(imagePath)
			#保存图像
			cv2.imwrite(('new'+imagePath[9:]),image)
		except:
			pass
'''
if __name__ == '__main__':
    image=yuchuli('User.4.25.jpg')
    while(1):
        cv2.imshow('img1', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
'''