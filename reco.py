from PIL import Image
import math
import time
COUNT_WHITE=3
COUNT_LENGTH=100
NUM_BLOCK=50

def black_white(img,pixels):
	for row in range(img.size[0]):
		for line in range(img.size[1]):
			if pixels[row,line][0]<100 or pixels[row,line][1]<100 or pixels[row,line][2]<100 :
				pixels[row,line]=(0,0,0)
			else:
				pixels[row,line]=(255,255,255)
	img.save('tt1.jpg')
def rotate(img,pixels):
	line=img.size[1]//2
	row=1
	while not (pixels[row,line][0]==0 and pixels[row-1,line][0]==255):
		row+=1
	row_orig,line_orig=row,line
	row_final,line_final=0,0
	flag=0
	while 1:
		flag_1=0
		line-=1
		if not pixels[row,line][0]:
			while not pixels[row,line][0]:
				row-=1
			row+=1
		else:
			row_final=row
			count=0
			t=row
			while pixels[row,line][0]:
				count+=1
				row-=1
				if count>COUNT_WHITE:
					count_1=0
					row=t
					while pixels[row,line][0]:
						count_1+=1
						row+=1
						#print(row,line,pixels[row,line])
						if count_1>COUNT_WHITE:
							line_final=line-1
							flag=1
							flag_1=1
							break
				if flag_1:
					break
		if flag:
			break
	row_d,line_d=0,0
	flag=0
	row,line=row_orig,line_orig
	while 1:
		flag_1=0
		line+=1
		if pixels[row,line][0]:
			count=0
			row_d=row
			while pixels[row,line][0]:
				count+=1
				row+=1
				if count>COUNT_WHITE:
					line_d=line-1
					flag=1
					break
		if flag:
			break
		else:
			while not pixels[row,line][0]:
				row-=1
			row+=1
	#print('d:',row_d,line_d)

	digree=math.atan((row_d-row_final)/(line_d-line_final))*180/math.pi
	print(row_final,line_final,row_d,line_d,digree)
	img=img.rotate(-digree)
	return img

def get_border(img,pixels):
	row=0
	result=[]
	img.save('tt2.jpg')
	flag_b=0
	while row<img.size[0]:
		line=1
		count=0
		flag=0
		line_start=0
		while line<img.size[1]:
			if pixels[row,line][0]==0 and pixels[row,line-1][0]==255:
				count=0
				flag=1
				line_start=line
			count+=1
			if pixels[row,line][0]==255 and pixels[row,line-1][0]==0:
				if count>COUNT_LENGTH and flag:
					result.append({
						'row_start':row,
						'line_start':line_start,
						'line_end':line,
						'length':count
						})
					if len(result)>1:
						if 0.9*result[-2]['line_end']>result[-1]['line_end']:
							print(result)
							flag_b=1
							for i in range(len(result)-2,0,-1):
								if 0.9*result[i]['line_end']>result[i-1]['line_end']:
									result=result[i:-1]
									break
							result=result[:-1]
			if flag_b:
				break
			line+=1
		if flag_b:
			break
		row+=1
	line_start=min(item['line_start'] for item in result)
	line_end=max(item['line_end'] for item in result)
	#print(line_start,line_end)
	line=img.size[1]-1
	result=[]
	flag_b=0
	while line>0:
		row=1
		count=0
		flag=0
		row_start=0
		while row<img.size[0]:
			if pixels[row,line][0]==0 and pixels[row-1,line][0]==255:
				count=0
				flag=1
				row_start=row
			count+=1
			if pixels[row,line][0]==255 and pixels[row-1,line][0]==0:
				if count>COUNT_LENGTH and flag:
					result.append({
						'row_start':row_start,
						'row_end':row,
						'line_start':line,
						'length':count
						})
					if len(result)>1:
						if 0.9*result[-2]['row_end']>result[-1]['row_end']:
							print(result)
							flag_b=1
							for i in range(len(result)-2,0,-1):
								if 0.9*result[i]['row_end']>result[i-1]['row_end']:
									result=result[i:-1]
									break
							result=result[:-1]
			if flag_b:
				break
			row+=1
		if flag_b:
			break
		line-=1
	row_start=min(item['row_start'] for item in result)
	row_end=max(item['row_end'] for item in result)
	#print(row_start,row_end)
	return {
	'row_start':row_start,
	'row_end':row_end,
	'line_start':line_start,
	'line_end':line_end
	}

def reco(img,pixels):
	b=get_border(img,pixels)
	#line_start=max(item['line_start'] for item in b)
	#line_end=min(item['line_end'] for item in b)
	#lenth=min(item['length'] for item in b)
	#row_start=b[0]['row_start']
	row_start=b['row_start']
	row_end=b['row_end']
	line_start=b['line_start']
	line_end=b['line_end']
	#block_length=(line_end-line_start+1)/(NUM_BLOCK+2)
	block_length=(line_end-line_start+row_end-row_start)/(2*(NUM_BLOCK+2))
	b_length=round(block_length)
	#print(row_start,line_start,line_end,lenth,block_length,b_length)
	print(row_start,line_start,row_end,line_end,block_length,b_length)
	result=''
	mini=b_length*b_length//2
	for line in range(1,NUM_BLOCK+1):
		top=round(line_start+line*block_length)
		for row in range(1,NUM_BLOCK+1):
			left=round(row_start+row*block_length)
			#print(left,top)
			count_w,count_b=0,0
			for i in range(b_length):
				for j in range(b_length):
					if pixels[left+i,top+j][0]:
						count_w+=1
					else:
						count_b+=1
				if count_w>mini:
				#if count_w>mini*1.5:
					result+='1'
					break
				if count_b>=mini:
				#if count_b>mini*0.5:
					result+='0'
					break
			if True:
				if count_w<mini+1 and count_b<mini:
					print(mini,left,top,count_w,count_b)
	return result


if __name__=='__main__':
	start_time=time.time()
	#img=Image.open('test/007.png')
	img=Image.open('img1.jpg')
	img=img.rotate(-90)
	pixels=img.load()
	black_white(img,pixels)
	img=rotate(img,pixels)
	pixels=img.load()
	res=reco(img,pixels)
	print(res,len(res))
	end_time=time.time()
	print('%.2f'%(end_time-start_time))

