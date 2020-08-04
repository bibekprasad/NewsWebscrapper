from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect
import nltk
nltk.download("stopwords")
nltk.download('punkt')	
import heapq
import re

# def Scrape(request):
# 	if(request.method=="POST"):
			
	
# 		site=request.POST.get("site"," ")


# 		if(site=="news"):

# 			searchString="https://economictimes.indiatimes.com/" + site +"/"

# 			page=requests.get(searchString)

# 			soup=BeautifulSoup(page.content,"html.parser")

# 		# for link in soup.find_all("a"):
# 		# 	link_address=link.get("href")
# 		# 	link_name=link.string
# 		# 	Link.objects.create(Link_address=link_address,Link_name=link_name)

# 			for link in soup.find_all("article",{"class":"newslist"}):

# 				if(len(link.text.split(" "))>4):
# 					link_address="https://economictimes.indiatimes.com/"+link.a.get("href")
					
# 					summary=Summary(link_address)

					
# 					link_name=link.h4.text

# 			Link.objects.create(Link_address=link_address,Link_name=link_name)	

# 			return  HttpResponseRedirect('/')
# 	else:
# 		data=Link.objects.all()	
		

# 	return render(request,"myapp/final_view.html",{"data" : data})  		




		# if(site=="stocks"):

		# 	searchString="https://economictimes.indiatimes.com/markets/" + site +"/news"

		# 	page=requests.get(searchString)

		# 	soup=BeautifulSoup(page.content,"html.parser")

		# 	for link in soup.find_all("div",{"class":"eachStory"}):

		# 		if(len(link.text.split(" "))>4):
		# 			link_address="https://economictimes.indiatimes.com/"+link.a.get("href")
					
		# 			summary=Summary(link_address)

					
		# 			# page1=requests.get(link_address)
		# 			# soup1=BeautifulSoup(page1.content,"html.parser")


		# 			# paragraph=" "
		# 			# for tex in soup1.find_all("div",{"class":"Normal"}):

		# 			# 	paragraph +=tex.text
					
		# 			link_name=link.h4.text
		








		
		
		#print(paragraph)		

		

		# except Exception as e:
		# 	raise Exception (("Only integers are allowed"))


		# except Exception as e:
		# 	message= "You violated the business logic"

	

	

	# return render(request,"myapp/final_view.html",{"data" : data})  



def Scrape(request):
	if(request.method=="POST"):
			
	
		site=request.POST.get("site"," ")

		if(site=="news"):

			searchString="https://economictimes.indiatimes.com/" + site +"/"

			page1=requests.get(searchString)

			soup1=BeautifulSoup(page1.content,"html.parser")
			
			for link in soup1.find_all("article",{"class":"newslist"}):

				if(len(link.text.split(" "))>4):
					link_address="https://economictimes.indiatimes.com/"+link.a.get("href")
					

					summary=Summary(link_address)

					link_name=link.h4.text
					
					Link.objects.create(Link_address=link_address,Link_name=link_name,Summary=summary)

			
			return  HttpResponseRedirect('/')		
			
		



		if(site=="stocks"):

			searchString2="https://www.livemint.com/market/stock-market-news"

			page2=requests.get(searchString2)
			
			soup2=BeautifulSoup(page2.content,"html.parser")
			
			
			for link in soup2.find_all("h2",{"class":"headline"}):
				
				link_address="https://www.livemint.com/market/stock-market-news"+link.a.get("href")

				#summary=Summary(link_address)

					#link_name=link.h4.text
				link_name=link.text

				Link.objects.create(Link_address=link_address,Link_name=link_name,Summary=summary)

			return  HttpResponseRedirect('/')	









			


		# except Exception as e:
		# 	raise Exception (("Only integers are allowed"))


		# except Exception as e:
		# 	message= "You violated the business logic"

	else:
		data=Link.objects.all()

	

	return render(request,"myapp/final_view.html",{"data" : data})  






def Summary(link_address):
	page1=requests.get(link_address)
	soup1=BeautifulSoup(page1.content,"html.parser")


	paragraph=" "

	for tex in soup1.find_all("div",{"class":"Normal"}):
		paragraph +=tex.text



	#Preprocessing	
	paragraph=re.sub(r'\n'," ",paragraph)

	clean_text=paragraph.lower()
	clean_text=re.sub(r"\W"," ",clean_text)
	clean_text=re.sub(r"\d"," ",clean_text)
	clean_text=re.sub(r"\s+"," ",clean_text)
	

	sentences=nltk.sent_tokenize(paragraph)
	stopwords=nltk.corpus.stopwords.words("english")


	#histogram
	word2count={}

	for word in nltk.word_tokenize(clean_text):
		if word not in stopwords:
			if word not in word2count.keys():
				word2count[word]=1
			else:
				word2count[word]+=1


	



	#weighted Histogram

	for key in word2count.keys():
		word2count[key]=(word2count[key]/max(word2count.values()))
	#sentence value

	sent2score={}
	for sentence in sentences:
  		for word in nltk.word_tokenize(sentence.lower()):
  			if word in word2count.keys():
  				if (len(sentence.split(" "))<25):
   					if sentence not in sent2score.keys():
   						sent2score[sentence]=word2count[word]
   					else:
   						sent2score[sentence]+=word2count[word]


	best_sentences=heapq.nlargest(8,sent2score,key=sent2score.get)


	return (best_sentences)





def clear(request):
	Link.objects.all().delete()
	return render (request,"myapp/final_view.html")



	
