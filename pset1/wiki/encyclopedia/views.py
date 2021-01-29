import json
import markdown2
import random
import re
from django import forms
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

def index(request,TITLE=None):
    q=request.GET.get('q')
    if q:
        if util.get_entry(q):
            return HttpResponseRedirect(reverse("entry",args={q}))
        else:
            list_=[title for title in util.list_entries() if q.lower() in title.lower()]
            if len(list_)>0:
                return render(request, "encyclopedia/index.html", {
                    "TITLE":"Do you mean...",
                    "entries": list_
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "TITLE":"Can't find anything...",
                    "entries": []
                })
    elif TITLE:
        return goentry(request,TITLE)
    else:
        return render(request, "encyclopedia/index.html", {
            "TITLE":"All Pages",
            "entries": util.list_entries()
        })

def goentry(request,TITLE):
    entrydetail=util.get_entry(TITLE)
    if entrydetail:
        entrydetail=entrydetail.replace('\r','')
        entrydetail=convHTML(entrydetail)
        return render(request, "encyclopedia/entry.html", {
            "entryexist":True,
            "entrytitle": TITLE,
            "entrydetailHTML": entrydetail
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entryexist":False,
            "entrytitle": TITLE+" (?)",
            "entrydetailHTML": "<h3 style='color:red'>ERROR: Entry doesn't exist.</h3>"
        })

def create(request):
    EntryTitle=request.GET.get('EntryTitle')
    if EntryTitle:
        EntryContent=request.GET.get('EntryContent')
        util.save_entry(EntryTitle,EntryContent)
        return HttpResponseRedirect(reverse("entry",args={EntryTitle}))
    else:
        return render(request, "encyclopedia/create.html", {
            "entrieslower": json.dumps([ str_.lower() for str_ in util.list_entries()])
        })

def randompage(request):
    list_=util.list_entries()
    TITLE=list_[int(random.uniform(0,len(list_)))]
    return HttpResponseRedirect(reverse("entry",args={TITLE}))

def edit(request,TITLE):
    ACT_=request.GET.get('Action')
    print(ACT_)
    if ACT_=='CANCEL':
        return HttpResponseRedirect(reverse("entry",args={request.GET.get('EntryTitle')}))
    elif ACT_=='COMFIRM':
        return create(request)
    elif ACT_=='DELET':
        util.delet_entry(TITLE)
        return HttpResponseRedirect(reverse("index"))
    else:
        entrydetail=util.get_entry(TITLE).replace('\r','')
        return render(request, "encyclopedia/edit.html", {
            "entrytitle": TITLE,
            "entrydetail": entrydetail
        })

def convHTML(entrydetail):
    temp_=entrydetail
    # ##<h4>
    for str_ in set(re.findall(r"\s*\#{2} [^\#\s]*\s",temp_)):
        i_=str_.find('## ')
        Nstr_=str_[:i_]+"<h4>"+str_[i_+3:]+"</h4>"
        temp_=temp_.replace(str_,Nstr_)
        """
        print("==========  ##  ===============")
        print([str_])
        print("-------------------------------")
        print([Nstr_])
        print("===============================")
        """
    # #<h2>
    for str_ in set(re.findall(r"\s*\# [^\#\s]*\s",temp_)):
        i_=str_.find('# ')
        Nstr_=str_[:i_]+"<h2>"+str_[i_+2:]+"</h2>"
        temp_=temp_.replace(str_,Nstr_)
        """
        print("===========  #   ==============")
        print([str_])
        print("-------------------------------")
        print([Nstr_])
        print("===============================")
        """
    # ** **<strong>
    for str_ in set(re.findall(r"\*{2}[^\*\t\n\v\r\f]*\*{2}",temp_)):
        Nstr_="<strong>"+str_.replace('**','')+"</strong>"
        temp_=temp_.replace(str_,Nstr_)
        """
        print("=========== ** ** =============")
        print([str_])
        print("-------------------------------")
        print([Nstr_])
        print("===============================")
        """
    # * <span><i>
    for str_ in set(re.findall(r"\s*\* [^\*\s]*\s+",temp_)):
        i_=str_.find('* ')
        Nstr_=str_[:i_]+"<ul><li>"+str_[i_+2:]+"</li></ul>"
        temp_=temp_.replace(str_,Nstr_)
        """
        print("============  *   =============")
        print([str_])
        print("-------------------------------")
        print([Nstr_])
        print("===============================")
        """
    temp_=temp_.replace("</ul><ul>","")
    # [](/)<a>
    for str_ in set(re.findall(r"\[[^\[\]\s]*\]\([^\(\)\s]*\)",temp_)):
        title_=str_[str_.find('[')+1:str_.find(']')]
        href_=str_[str_.find('(')+1:str_.find(')')].replace("/wiki/",'')
        Nstr_="<a href='"+ href_ +"' >"+title_+"</a>"
        temp_=temp_.replace(str_,Nstr_)
        """
        print("=========== []() ==============")
        print([str_])
        print("-------------------------------")
        print([Nstr_])
        print("===============================")
        """
    return temp_