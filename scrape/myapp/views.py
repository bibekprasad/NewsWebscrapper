from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect

def Scrape(request):
	if(request.method=="POST"):
			
	
		site=request.POST.get("site"," ")

		searchString="https://economictimes.indiatimes.com/" + site +"/"

		page=requests.get(searchString)

		soup=BeautifulSoup(page.content,"html.parser")

	# for link in soup.find_all("a"):
	# 	link_address=link.get("href")
	# 	link_name=link.string
	# 	Link.objects.create(Link_address=link_address,Link_name=link_name)

		for link in soup.find_all("article",{"class":"newslist"}):

			if(len(link.text.split(" "))>4):
				link_address="https://economictimes.indiatimes.com/"+link.a.get("href")
				link_name=link.h4.text
				Link.objects.create(Link_address=link_address,Link_name=link_name)
				

		return  HttpResponseRedirect('/')


		# except Exception as e:
		# 	raise Exception (("Only integers are allowed"))


		# except Exception as e:
		# 	message= "You violated the business logic"

	else:
		data=Link.objects.all()

	

	return render(request,"myapp/final_view.html",{"data" : data})  





def clear(request):
	Link.objects.all().delete()
	return render (request,"myapp/final_view.html")



	
