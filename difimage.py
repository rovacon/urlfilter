# -*- coding: utf-8 -*-
import Image
import ImageChops
import os,sys


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
   
def calc_similar(li, ri):
    return hist_similar(li.histogram(), ri.histogram())

def similar_percent(file1,file2):
    #打开两个图片
    if not os.path.exists(file1) or not os.path.exists(file2):
        return 0
    im1=Image.open(file1)
    im2=Image.open(file2)
    #print im.format,im.size,im.mode
    #去除页首和页尾
    #box=(0,225,1080,1800)dd
    #image1 = im1.crop(box)
    #image2 = im2.crop(box)
    #计算两图相似度百分比
    percent=calc_similar(im1,im2)
    print percent
    return percent

#MAX = ImageChops.invert(image2)  
#MAX=ImageChops.subtract(image1, image2, 1, 0) 
#Image.blend(image1,MAX,0.5).show()  
#region = region.transpose(Image.ROTATE_180)
#im.paste(region, box)
#ImageChops.darker(image1, image2).show()
#if percent<0.8:
#    #如果差异大于20%即输出合成图片
#    invert = ImageChops.invert(image2)
#    mix=Image.blend(image1,invert,0.5)
#    #a=ImageChops.subtract(image1, image2,1,0)
#    #a.show()
#    #保存合成图片
#    mix.save("Z:\\luohg\\"+line.rsplit(".",1)[0]+".jpg")
#region.show()
#out.show()


def get_urlkey(url):
    keylist=[]
    baseurl,query=urllib.splitquery(url)
    if not query:
        return url,""
    else:
        querylist=query.split('&')
        querylist.sort()
        urlkey=baseurl+"?"
        for attr in querylist:
            if attr:
               keylist.append(attr)
               key=attr.split('=')[0]
               urlkey+=key+"&"
        return urlkey,keylist

def run_url(url,fd):
     global filter_result,line_num
     origin_url=url
     html=fd
     filter=[]
     notfilter=[]
     urlkey,keylist=get_urlkey(origin_url)
     if not keylist:
        return 0
     if urlkey in have_run:
        return 0
     origin_file=str(line_num)+"origin"
     cmd = 'bin/phantomjs examples/urlfilter.js \"'+origin_url+'\" '+origin_file
     #print cmd
     if os.system(cmd) !=0:
        print "can not download origin image"
        sys.exit()
     page_html=open('html/'+str(line_num)+'.html','w')
     page_html.write("<table><tr><td>"+origin_url+"</td><td>similar_percent</td></tr>")
     for attr in keylist:
        testurl=origin_url.replace(attr,'')
        key=attr.split('=')[0]
        filename=str(line_num)+key
        if os.system('bin/phantomjs examples/urlfilter.js \"'+testurl+'\" '+filename) !=0:
           print "can not download image"
           sys.exit()
        percent=similar_percent('png/'+origin_file+'.png','png/'+filename+'.png')
        if percent<0.9 :
           notfilter.append(key)
        elif float(percent)>0:
           filter.append(key)
        if percent != 0:
           with open('html/'+filename+'.html','w') as pnghtml:
               pnghtml.write("<body><table border='1'><tr><td>"+origin_url+"</td><td>similar_percent:"+str(percent)+"</td></tr><tr><td>origin</td><td>key</td></tr><tr><td><img src='../png/"+origin_file+".png'></td><td><img src='../png/"+filename+".png'></td></tr></body>")
               page_html.write("<tr><td>"+key+"</td><td><a href="+filename+".html>"+str(percent)+"</a></td></tr>")
     page_html.write("</table>")
     page_html.close()
     filter_result=filter_result | set(filter) -set(notfilter)
     html.write("<tr><td><a href='html/"+str(line_num)+".html'>"+origin_url+"</a></td><td>"+','.join(filter)+"</td><td>"+','.join(notfilter)+"</td></tr>")
     have_run.append(urlkey)

#import urlparse
import urllib
global filter_result,line_num,have_run
line_num=0
filter_result=set()
have_run=[]
html=open('result.html','w')
html.write("<body><table border='1'><tr><td>origin_url</td><td>can filter</td><td>can not filter</td>")
with open('urllist.txt','r') as f:
    for line in f.readlines():
        line_num+=1
        origin_url=line.strip()
        run_url(origin_url,html)
html.write("<tr><td>"+','.join(filter_result)+"</td></tr></table></body>")
html.close()

