import requests
import os
import json
import hashlib

headers={'user-agent':'mozilla/5.0'}

#download character json
url = "put character json link here"      #you need modify there
f = requests.get(url , headers = headers)
json_array = f.json()
file_name = 'Character.json'

#save character json 
with open('Character.json','w') as j:
	json.dump(json_array , j)

#make img dir
os.makedirs('img',exist_ok=True)

#initial variables
CurrentName = ''
CurrentRId = ''
CurrentCId = ''

#Using md5 to check image is avilable or not, and check if character's images is downloaded
  
def chkMD5(id1,id2,CurrentName):
	url1 = "put character ev link here"+str(id1)+"/still_"+str(id2)+"_03_01.png"  #you need modify there
	print('now trying get'+'still_'+str(id2)+'_03_01.png')
	f = requests.get(url1, headers = headers)
	if f.status_code ==200:
		#make temp png , beacause of chunck md5 is not equal to md5 of loacl png
		temppic = open('temp.png','wb')   	
		temppic.write(f.content)
		#load temp png
		tp = open('temp.png','rb')
		#initail md5 object
		currentmd5 = hashlib.md5()
		#md5 hash lib need using buffer to load data 
		fp = tp.read(8096)
		currentmd5.update(fp)
		#print('current md5 is: '+str(currentmd5.hexdigest()))
		#compare temp png 's md5 with unpublished character png's md5
		if currentmd5.hexdigest()=='716a128da717328290bb06293e98a8b9':   
			print(CurrentName+" has not published")
			return 1
		else:
			try:
				#check local image is exist or not
				f = open('img\\'+CurrentName+'\\ev\\'+CurrentName+'_03_01.png','rb') #you need modify there
				md5=hashlib.md5()
				fp = f.read(8096)
				md5.update(fp)
				print('local md5 is:   '+str(md5.hexdigest()))
				print('current md5 is: '+str(currentmd5.hexdigest()))
				if md5.hexdigest()==currentmd5.hexdigest() :
					print(CurrentName+' has already exist in img dir , pass')
					return 1
				else :
					print(CurrentName+' md5 is not mactch in local pic , start download')
					return 0
			except FileNotFoundError :
					print(CurrentName+' has not in img dir , start download')
					return 0
		return 0
	else :
		print('url is not found')
		return 1
#grab character png
def chara(id1,CurrentName):
	url1 = "put character  link here"+id1+"/chr_illust.png"            #you need modify there
	url2 = "put character  link here"+id1+"/chr_illust_p.png"          #you need modify there
	f = requests.get(url1, headers = headers)
	if f.status_code ==200:
		print(url1+" is downloading...")
		with open('img\\'+CurrentName+'\\chara\\'+CurrentName+'_chr_illust.png','wb') as fp:  
			fp.write(f.content)
	f = requests.get(url2, headers = headers)
	if f.status_code ==200:
		print(url2+" is downloading...")
		with open('img\\'+CurrentName+'\\chara\\'+CurrentName+'_chr_illust_p.png','wb') as fp:
			fp.write(f.content)

#grab events png
def ev(id1,id2,CurrentName):
	url1 = "put  ev link here"+str(id1)+"/still_"+str(id2)+"_03_0"  #you need modify there
	url2 = "put  ev link here"+str(id1)+"/still_"+str(id2)+"_05_0"  #you need modify there
	for i in range(1,7):
		f = requests.get(url1+str(i)+".png" , headers = headers)
		if f.status_code ==200:
			print(url1+str(i)+".png"+" is downloading...")
			with open('img\\'+CurrentName+'\\ev\\'+CurrentName+'_03_0'+str(i)+'.png','wb') as fp:
				fp.write(f.content)
		f = requests.get(url2+str(i)+".png" , headers = headers)
		if f.status_code ==200:
			print(url2+str(i)+".png"+" is downloading...")
			with open('img\\'+CurrentName+'\\ev\\'+CurrentName+'_05_0'+str(i)+'.png','wb') as fp:
				fp.write(f.content)
#Analyze Character.josn to find avaliable resources , and make directory to store images
for item in json_array:
	if(item['name'] == '名称未決') :
		continue
	#the character is not avaliable, increase iterator to find next character
	elif CurrentName == item['name']:
		continue
	else:
		if chkMD5(item['character_id'],item['resorce_id'],item['name'])==1:
			CurrentName = item['name']
			#the character is not avaliable, increase iterator to find next character
			for item in json_array:
				if item['name']==CurrentName:
					break
		#the character is available, and no image has existed in local directory, start create directories and download images.
		else:
			CurrentName = item['name']
			CurrentRId = item['resorce_id']
			CurrentCId = item['character_id']
			os.makedirs('img\\'+CurrentName,exist_ok=True)
			os.makedirs('img\\'+CurrentName+"\\chara",exist_ok=True)
			os.makedirs('img\\'+CurrentName+"\\ev",exist_ok=True)
			print(CurrentName+'\'s folder was created! ')
			chara(CurrentCId,CurrentName)
			ev(CurrentCId,CurrentRId,CurrentName)
	#print("resorce id: "+str(item['resorce_id'])+" name : "+str(item['name']))   for testing

print('done!')




#print(f.status_code) 

