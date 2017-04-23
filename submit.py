import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import files
from pprint import pprint
import datetime
#from datetime import datetime
from random import shuffle
import urllib
import Crypto
from Crypto.Cipher import ARC4
from google.appengine.api import memcache


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# a1_start=101;a1_end=301;a2_start=301;a2_end=401;a3_start=401;a3_end=601;a4_start=601;a4_end=701;
# a5_start=701;a5_end=801;
e1_start=801;e1_end=809;e2_start=1201;e2_end=1208;e3_start=1601;e3_end=1701;
e4_start=1701;e4_end=1702;
# t1_start=1801;t1_end=2201;t2_start=2201;t2_end=2601;
#a1_start=101;a1_end=201;a2_start=201;a2_end=301;a3_start=301;a3_end=401;a4_start=401;a4_end=501;
#a5_start=501;a5_end=601;e1_start=601;e1_end=701;e3_start=801;e3_end=901;
#e4_start=901;e4_end=1001;#t1_start=1001;t1_end=1101;t2_start=1101;t2_end=1201;e2_start=701;e2_end=801;
#t1_start=1801;t1_end=2201;t2_start=1101;t2_end=1201;
#e2_start=1201;e2_end=1601;

def getAllQuestions():
    json_temp=json.loads(open('QuestionBank_template.json').read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["videoArray"]=video_list
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                psglist=json_subs["passageArray"]
                                subs["passageArray"]=psglist
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["videoArray"]=video_list
    #ss=json.dumps(json_temp)
    return json_temp

def getAnswer(testid,qid):
    qid=int(qid)
    dirname = decrypt(testid)['path'][0]
    # if qid in range(a1_start,a1_end):
    #     a1_sentjson=json.loads(open('A1-Sentences.json').read())
    #     for key in a1_sentjson["questions"]:
    #         if int(key["id"]) == qid:
    #             for op in key["options"]:
    #                 if op[0] == "=":
    #                     return op[1:len(op)]
    # if qid in range(a2_start,a2_end):
    #     a2_readjson=json.loads(open('A2-Reading.json').read())
    #     for key in a2_readjson["passageArray"]:
    #         for psg in key["questions"]:
    #             if int(psg["id"]) == qid:
    #                 for op in psg["options"]:
    #                     if op[0] == "=":
    #                         return op[1:len(op)]
    # if qid in range(a3_start,a3_end):
    #     a3_numjson=json.loads(open('A3-Numerical.json').read())
    #     for key in a3_numjson["questions"]:
    #         if int(key["id"]) == qid:
    #             for op in key["options"]:
    #                 if op[0] == "=":
    #                     return op[1:len(op)]
    # if qid in range(a4_start,a4_end):
    #     a4_reasjson=json.loads(open('A4-Reasoning.json').read())
    #     for key in a4_reasjson["questions"]:
    #         if int(key["id"]) == qid:
    #             for op in key["options"]:
    #                 if op[0] == "=":
    #                     return op[1:len(op)]

    if qid in range(e1_start,e1_end):
        e1_readjson=json.loads(open(dirname+'/E1-Reading.json').read())
        for psg in e1_readjson["passageArray"]:
            for key in psg["questions"]:
                if int(key["id"]) == qid:
                    for op in key["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(e2_start,e2_end):
        e2_lsnjson=json.loads(open(dirname+'/E2-Listening.json').read())
        for key in e2_lsnjson["videoArray"]:
            for qn in key["questions"]:
                if int(qn["id"]) == qid:
                    for op in qn["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    # if qid in range(t1_start,t1_end):
    #     t1_readjson=json.loads(open('T1-Reading.json').read())
    #     for key in t1_readjson["passageArray"]:
    #         for qn in key["questions"]:
    #             if int(qn["id"]) == qid:
    #                 for op in qn["options"]:
    #                     if op[0] == "=":
    #                         return op[1:len(op)]
    # if qid in range(t2_start,t2_end):
    #     t2_lsnjson=json.loads(open('T2-Listening.json').read())
    #     for key in t2_lsnjson["videoArray"]:
    #         for qn in key["questions"]:
    #             if int(qn["id"]) == qid:
    #                 for op in qn["options"]:
    #                     if op[0] == "=":
    #                         return op[1:len(op)]

def getQuestionPaper(testid,qid_list):
    dirname = decrypt(testid)['path'][0]
    json_temp=json.loads(open('QP_template.json').read())
    #print qid_list
    i=0;j=0;k=0;l=0;m=0;n=0;p=0;q=0;r=0;s=0;t=0
    for qid in qid_list:
        qid=int(qid)
        # if qid in range(a1_start,a1_end):
        #       a1_sentjson=json.loads(open('A1-Sentences.json').read())
        #       for key in a1_sentjson["questions"]:
        #             logging.error("questions with sno")
        #             print(key["id"])
        #             if int(key["id"]) == qid:
        #                   #print key
        #                   json_temp["section"][0]["subsection"][0]["questions"].append(key)
        #                   json_temp["section"][0]["subsection"][0]["questions"][i]["serialno"] = qid_list[qid]
        #                   i +=1
        # if qid in range(a2_start,a2_end):
        #       a2_readjson=json.loads(open('A2-Reading.json').read())
        #       for key in a2_readjson["passageArray"]:
        #             pid=key["questions"][0]["id"]
        #             if int(pid) == qid:
        #                   json_temp["section"][0]["subsection"][1]["passage"]=key["passage"]
        #                   json_temp["section"][0]["subsection"][1]["questions"]=key["questions"]
        #                   json_temp["section"][0]["subsection"][1]["questions"][0]["serialno"] = qid_list[qid]
        # if qid in range(a3_start,a3_end):
        #       a3_numjson=json.loads(open('A3-Numerical.json').read())
        #       for key in a3_numjson["questions"]:
        #             if int(key["id"]) == qid:
        #                   json_temp["section"][0]["subsection"][2]["questions"].append(key)
        #                   json_temp["section"][0]["subsection"][2]["questions"][j]["serialno"] = qid_list[qid]
        #                   j +=1
        # if qid in range(a4_start,a4_end):
        #       a4_reasjson=json.loads(open('A4-Reasoning.json').read())
        #       for key in a4_reasjson["questions"]:
        #             if int(key["id"]) == qid:
        #                   json_temp["section"][0]["subsection"][3]["questions"].append(key)
        #                   json_temp["section"][0]["subsection"][3]["questions"][k]["serialno"] = qid_list[qid]
        #                   k +=1
        # if qid in range(a5_start,a5_end):
        #       a5_essayjson=json.loads(open('A5-Composition.json').read())
        #       for key in a5_essayjson["questions"]:
        #             if int(key["id"]) == qid:
        #                   json_temp["section"][0]["subsection"][4]["questions"].append(key)
        #                   json_temp["section"][0]["subsection"][4]["questions"][l]["serialno"] = qid_list[qid]
        #                   l += 1
        if qid in range(e1_start,e1_end):
              e1_readjson=json.loads(open(dirname+'/E1-Reading.json').read())
              for key in e1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][2]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][2]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][2]["subsection"][0]["questions"][m]["serialno"] = qid_list[qid]
                                m +=1
        if qid in range(e2_start,e2_end):
              e2_lsnjson=json.loads(open(dirname+'/E2-Listening.json').read())
              for key in e2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][0]["subsection"][0]["link"]=key["link"]
                                json_temp["section"][0]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][0]["subsection"][0]["questions"][n]["serialno"] = qid_list[qid]
                                n +=1
        if qid in range(e3_start,e3_end):
              e3_spkjson=json.loads(open(dirname+'/E3-Speaking.json').read())
              for key in e3_spkjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][0]["questions"].append(key)
                          json_temp["section"][1]["subsection"][0]["questions"][p]["serialno"] = qid_list[qid]
                          p += 1
        if qid in range(e4_start,e4_end):
              e4_wrtjson=json.loads(open(dirname+'/E4-Writing.json').read())
              for key in e4_wrtjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][3]["subsection"][0]["questions"].append(key)
                          json_temp["section"][3]["subsection"][0]["questions"][q]["serialno"] = qid_list[qid]
                          q += 1
        # if qid in range(t1_start,t1_end):
        #       t1_readjson=json.loads(open('T1-Reading.json').read())
        #       for key in t1_readjson["passageArray"]:
        #             for qn in key["questions"]:
        #                   pid=qn["id"]
        #                   if int(pid) == qid:
        #                         json_temp["section"][2]["subsection"][0]["passage"]=key["passage"]
        #                         json_temp["section"][2]["subsection"][0]["questions"].append(qn)
        #                         json_temp["section"][2]["subsection"][0]["questions"][r]["serialno"] = qid_list[qid]
        #                         r += 1
        # if qid in range(t2_start,t2_end):
        #       t2_lsnjson=json.loads(open('T2-Listening.json').read())
        #       for key in t2_lsnjson["videoArray"]:
        #             for qn in key["questions"]:
        #                   pid=qn["id"]
        #                   if int(pid) == qid:
        #                         json_temp["section"][2]["subsection"][1]["link"]=key["link"]
        #                         json_temp["section"][2]["subsection"][1]["questions"].append(qn)
        #                         json_temp["section"][2]["subsection"][1]["questions"][s]["serialno"] = qid_list[qid]
                                # s += 1
    #ss=json.dumps(json_temp)
    return json_temp

def decrypt(string):
    obj=ARC4.new('rgukteltqat')
    plain = obj.decrypt(string)
    get_data = cgi.parse_qs(plain)
    return get_data

def generateQuestionPaper(testid):
    dirname = decrypt(testid)['path'][0]
    json_temp=json.loads(open('QP_template.json').read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            cnt=int(subs["count"])
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(dirname+"/"+name+".json").read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                i=0
                                for qn in subs["questions"]:
                                    subs["questions"][i]["serialno"]=i+1
                                    i +=1
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(dirname+"/"+name+".json").read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(dirname+"/"+name+".json").read())
                                psglist=json_subs["passageArray"]
                                serialno=range(0,len(psglist))
                                shuffle(serialno)
                                subs["questions"]=psglist[serialno[0]]["questions"]
                                j=0
                                for qn in subs["questions"]:
                                    subs["questions"][j]["serialno"]=j+1
                                    j +=1
                                subs["passage"]=psglist[serialno[0]]["passage"]
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(dirname+"/"+name+".json").read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(dirname+"/"+name+".json").read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                k=0
                                for qn in subs["questions"]:
                                  subs["questions"][k]["serialno"]=k+1
                                  k +=1
    #ss=json.dumps(json_temp)
    return json_temp

def getsetlink(setname):
    obj=ARC4.new('rgukteltqat')
    plain = urllib.urlencode({'path': setname})
    ciph = obj.encrypt(plain)
    # /?%s' % urllib.urlencode({'testid': setname})
    url = '/startquiz'
    return url,ciph


def getsets():
    ELTset = []
    QATset = []
    for root,dirs,files in os.walk("."):
        for dirname in dirs:
            if "ELTset" in dirname:
                qset = {}
                qset["name"] = dirname
                qset["fullName"] = "ELT Test " + dirname[-1]
                # print "dirname:::::::::::" + qset["fullName"]

                qset["id"] = ""
                qset["link"] = ""
                ELTset.append(qset)
                # print "------------------------------------------------------------------"
                print ELTset.sort()
            elif "QATset" in dirname:
                qset = {}
                qset["name"] = dirname
                qset["fullName"] = "QAT Test " + dirname[-1]
                # print "dirname:::::::::::" + qset["fullName"]
                qset["id"] = ""
                qset["link"] = ""
                QATset.append(qset)
    return ELTset,QATset


class UserAudio(ndb.Model):
    user = ndb.StringProperty(indexed=True)
    # blob_key = blobstore.BlobReferenceProperty()
    blob1 = ndb.BlobKeyProperty(indexed=True)
    time=ndb.DateTimeProperty(auto_now_add=True)

class DataModel(db.Model):
	url = db.StringProperty(required=True)
	blob = blobstore.BlobReferenceProperty(required=True)

class User(ndb.Model):
    """Sub model for storing user activity."""
    name = ndb.StringProperty(indexed=True)
    emailid = ndb.StringProperty(indexed=True)
    pin = ndb.StringProperty(indexed=True)
    testctime=ndb.DateTimeProperty(auto_now=True)

class userDetails(ndb.Model):
    rollno = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)    
    email=ndb.StringProperty(indexed=True)
    # phno = ndb.StringProperty(indexed=True)    
    testctime = ndb.DateTimeProperty(auto_now=True)
    learningcenter =  ndb.StringProperty(indexed = True)
    batch = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed =True)
    # street = ndb.StringProperty(indexed=True)
    # city = ndb.StringProperty(indexed=True)
    # state = ndb.StringProperty(indexed=True)
    # pincode = ndb.StringProperty(indexed=True)
    

class TestDetails(ndb.Model):
    email=ndb.StringProperty(indexed=True) 
    test= ndb.BooleanProperty(default=False)
    teststime=ndb.DateTimeProperty(auto_now_add=True) 
    delays=ndb.FloatProperty(indexed=True)
    testend= ndb.BooleanProperty(default=False)
    lastPing = ndb.DateTimeProperty(auto_now_add=True)
    score = ndb.IntegerProperty(indexed = True)
    learningcenter = ndb.StringProperty(indexed=True) 
    testId = ndb.BlobProperty(indexed=True) 
    admin = ndb.StringProperty(indexed=True)
    #useraudiolink =ndb.StringProperty(indexed=True)

class Response(ndb.Model):
    """Sub model for representing question details"""
    useremailid = ndb.StructuredProperty(User)
    submittedans = ndb.StringProperty(indexed = True)
    responsetime = ndb.FloatProperty(indexed = True)
    q_score = ndb.IntegerProperty(indexed = True)
    q_status = ndb.StringProperty(indexed = True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    currentQuestion=ndb.StringProperty(indexed = True)
    examid = ndb.BlobProperty(indexed=True)
    serialno=ndb.IntegerProperty(indexed=True)

class Randomize(ndb.Model):
    user1=ndb.StringProperty(indexed = True)
    serialno=ndb.IntegerProperty(indexed= True)
    qno=ndb.StringProperty(indexed = True)    
    examid = ndb.BlobProperty(indexed=True)


class EssayTypeResponse(ndb.Model):
    """Sub model for storing user response for essay type questions"""
    useremailid = ndb.StringProperty(indexed = True)
    qid = ndb.StringProperty(indexed = True)
    ansText = ndb.StringProperty(indexed = True)
    qattemptedtime = ndb.FloatProperty(indexed = True)

class UploadRedirect(webapp2.RequestHandler):
    def post(self):
        upload_url=blobstore.create_upload_url('/upload_audio');
        self.response.write(upload_url)
        #self.redirect("/upload_audio")

class AudioUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            #filename=self.request.get("audio-blob");
            #blobstore_key=blobstore.create_gs_key(filename)
            #blobkey=blobstore.BlobKey(blobstore_key)
            user = users.get_current_user()
            if user:
                upload = self.get_uploads()[0]
                #uname=str(users.get_current_user().email())
                user_audio = UserAudio(user=user.email(), blob_key=upload.key())
                user_audio.put()
                #print str(filename)
                #logging.error("upload value")
                # self.redirect('/view_audio/%s' % upload.key())
                #self.response.write("Uploaded success")
        except Exception,e:
            traceback.print_exc()
            logging.error("error occured.."+str(e))
            self.response.write("Record not saved")
# [END audio_handler]

# [START download_handler]
class ViewAudioHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, audio_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            resource = str(urllib.unquote(audio_key))
            blob_info = blobstore.BlobInfo.get(resource)
            self.send_blob(blob_info,save_as=True)
            self.response.write(str(key))
# # [END download_handler]   

class homepage(webapp2.RequestHandler):
    """  handles rendering of index page """
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
        
class uploadStudents(webapp2.RequestHandler):
    """  handles rendering of index page """
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('uploadStudents.html')
        self.response.write(template.render())

class Dashboard(webapp2.RequestHandler):
    def get(self):
        template= JINJA_ENVIRONMENT.get_template('dashboard.html')
        ELTsets,QATsets = getsets() #identifies and gets the folder names of question sets
        #currentDate =  "2017-03-06"        
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            userrow=userDetails.query(userDetails.email==user.email()).get()
            template=None
            if userrow is not None:
                rows = TestDetails.query(TestDetails.email == user.email()).fetch()
                elt_list,qat_list = {},{}
                for row in rows:
                    examid = row.testId
                    details = AdminDetails.query(AdminDetails.examid == examid).fetch()
                    setname = details[0].setname
                    testTime =  row.teststime
                    currentTime = datetime.datetime.now()
                    
                    if ((testTime -  currentTime >= 0) and (testTime - currentTime <= datetime.timedelta(minutes = 5))):
                        link,ids = getsetlink(examid)
                    if "ELT" in setname:
                        if len(ELTsets) != 0:
                            for i in range(len(ELTsets)):
                                if setname == ELTsets[i]["name"]:
                                    ELTsets[i]["examid"] = examid
                                    ELTsets[i]["toolTipDate"] = testTime.date().strftime("%A %d. %B %Y")
                                    ELTsets[i]["link"] = link
                                    # if row.testend:
                                    #     ELTsets[i]["score"] = row.score
                                    #     ELTsets[i]["status"] = "End"

                                    # else:
                                    #     currTime = datetime.datetime.now()
                                    #     deltaTime = (currTime - row.lastPing).total_seconds()
                                    #     if(deltaTime > 65.0):
                                    #         row.delays = row.delays + deltaTime - 60.0
                                    #         timeSpent = (currTime - row.teststime).total_seconds() - row.delays
                                    #         if timeSpent < 0:
                                    #             ELTsets[i]["status"] = "Start"
                                    #         else:
                                    #             ELTsets[i]["status"] = "In Progress"
                                    #             ELTsets[i]["timeleft"] = round((60*60-timeSpent)/60);
                                    elt_list[examid] = ELTsets[i]           
        




                   
                    

                    # logging.info(currentDate)
                     # eMailId = TestDetails.query(TestDetails.email == user.email()).get()      
                    # tempDate = currentDate
                    # for i in range(len(ELTsets)) :
                    # ELTsets[i] ["date"] = tempDate
                    # ELTsets[i] ["toolTipDate"] = tempDate.date().strftime("%A %d. %B %Y")
                    # tempDate +=  datetime.timedelta(days = 1)


                # if len(ELTsets) != 0:
                #     for i in range(len(ELTsets)):
                #         if ELTsets[i]["date"].date() - datetime.datetime.now().date() == datetime.timedelta(days = 0) :
                #             link,examid = getsetlink(ELTsets[i]["name"])
                #             memcache.add(key="examid", value=examid, time=360000)
                #             query = TestDetails.query(TestDetails.email==user.email()).get()
                #             if query is not None:
                #                 query.testId = memcache.get(key="examid")
                #                 query.put()
                #             ELTsets[i]["link"] = link

                #         row = TestDetails.query(TestDetails.email == user.email()).get()
                #         if row and row.testend:
                #             ELTsets[i]["score"] = row.score
                #             ELTsets[i]["status"] = "End"
                #         elif row is not None:
                #             currTime = datetime.datetime.now()
                #             deltaTime = (currTime - row.lastPing).total_seconds()
                #             if(deltaTime > 65.0):
                #                 row.delays = row.delays + deltaTime - 60.0
                #             timeSpent = (currTime - row.teststime).total_seconds() - row.delays
                #             if timeSpent < 0:
                #                 ELTsets[i]["status"] = "Start"
                #             else:
                #                 ELTsets[i]["status"] = "In Progress"
                #                 ELTsets[i]["timeleft"] = round((60*60-timeSpent)/60);



                # if len(QATsets) != 0:
                #     QATsets[0]["link"] = "/startquiz"




                template_values = {"ELTsets":elt_list,"QATsets":qat_list}
                template= JINJA_ENVIRONMENT.get_template('dashboard.html')
                self.response.write(template.render(template_values))
            else:
                template= JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render())



# check login is now being used to display userdetails from userddetails table

class checklogin(webapp2.RequestHandler):
    """ handles authentication and redirects to quiz page """
    def get(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            ss=Response.query(Response.useremailid.emailid==user.email()).get()
            if ss is None:
                Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
            sp=userDetails.query(userDetails.email==user.email()).get()
            template=None
            template_values = {}
            if sp is not None:
                template_values["name"] = sp.name
                template_values["emailid"] = sp.email
                template_values["rollno"] = sp.rollno
                template_values["campus"] = sp.learningcenter
            template= JINJA_ENVIRONMENT.get_template('userdetails.html')
            self.response.write(template.render(template_values))

class logout(webapp2.RequestHandler):
    """ handles authentication and redirects to quiz page """
    def get(self):
        logout_url = users.create_logout_url("/")
        self.redirect(logout_url)
        return

class getquizstatus(webapp2.RequestHandler):
    """ handling status of quiz sends a json file of responses"""
    def post(self):
        user = users.get_current_user()
        if user:
            # check if candidate is resuming the test
            r1 = Randomize.query(Randomize.user1==user.email()).fetch()
            if r1:
                isRandomized = True
                qid_list={}
                for data in r1:
                    qid_list[int(data.qno)] = data.serialno
                json_data=getQuestionPaper(memcache.get(key="examid"), qid_list)
            else:
                isRandomized = False
                json_data=generateQuestionPaper(memcache.get(key="examid"))
                # logging.info(json_data)
            # print json_data;
            # TODO
            # New json_data returned from the question bank if is randomized is false
            # Else list of question ID should be fetched from randomize table
            # pass the question IDs list to the question bank to get json_data

            #json_data = json.loads(open('quizdata.json').read())
            for key in json_data:
                if  key == "section":
                    section = json_data[key]
                    for s in  section:
                        for key in s:
                            if key == "subsection":
                                for subs in s[key]:
                                    for key in subs:
                                        if key == "questions":
                                            for q in subs[key]:
                                                if not isRandomized:
                                                    r = Randomize(user1 = user.email(), serialno = q['serialno'], qno=q["id"],examid=memcache.get("examid"))
                                                    r.put()
                                                else:
                                                    r = Randomize.query(Randomize.user1 == user.email(),
                                                                        Randomize.qno == q["id"]).get()
                                                q1 = Response.query(Response.useremailid.emailid==user.email(),
                                                                    Response.currentQuestion==q["id"]).order(-Response.time).get()
                                                if q1:
                                                    q["responseAnswer"]=q1.submittedans
                                                    q["responseTime"]=q1.responsetime
                                                    q["status"]=q1.q_status

            td = TestDetails.query(TestDetails.email==user.email()).get()
            if td:
                if td.testend:
                    json_data['quizStatus'] = 'END'
                else:
                    json_data['quizStatus'] = 'INPROGRESS'
            else:
                json_data['quizStatus'] = 'START'

        ss=json.dumps(json_data)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)

class getResult(webapp2.RequestHandler):
    """ get result for entire quiz """
    def get(self):
        totalscore=0
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            q1= Response.query(Response.useremailid.emailid==user.email())
            q1=q1.order(Response.serialno,-Response.time)
            questionresponses_dict = {}
            question_records=[]
            totalscore=0
            s1="0"
            for q in q1:
                if q.responsetime is not None:
                    if q.currentQuestion != s1 :
                        s1=q.currentQuestion
                        #totalscore=q.responsetime+q.q_score
                        question = {"user":user.nickname(),"submittedans":q.submittedans, "q_score":q.q_score,"currentQuestion":s1,"responsetime":q.responsetime}
                        question_records.append(question)
            questionresponses_dict["question"]=question_records
            questionresponses_dict["totalscore"]=totalscore
            ss=json.dumps(questionresponses_dict)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

class getScore(webapp2.RequestHandler):
    """ get score for entire quiz """
    def get(self):
        score=0
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            q1= Response.query(Response.useremailid.emailid==user.email())
            q1.fetch()
            q1= Response.query(Response.useremailid.emailid==user.email())
            q1.fetch()
            for q in q1:
                score=score+1
            template_values = {
                'p': q1,
                'score1':score,
                }
            template = JINJA_ENVIRONMENT.get_template('testresult.html')
            self.response.write(template.render(template_values))

class submitAnswer(webapp2.RequestHandler):
    """ submting question response , sends a json file of response"""
    def post(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            # quiz timer code starts here
            # this part will check the delay and compute the time taken
            td=TestDetails.query(TestDetails.email==user.email()).get()
            if td and not td.testend:
                validresponse="false"
                status=""
                errortype=""
                q_status=""
                score=0
                type=""
                logging.error("printing json values");
                vals = json.loads(cgi.escape(self.request.body))
                vals = vals['jsonData']
                currentQuestion =vals['id']
                submittedans = vals['responseAnswer']
                responsetime = vals['responseTime']
                # opening  json file of quizdata
                #logging.error(currentQuestion,submittedans)
                currentQuestion=int(currentQuestion)
                if submittedans == "skip":
                    validresponse="true"
                    q_status="skip"
                # elif currentQuestion in range(a5_start,a5_end):
                #     q_status="submitted"
                #     status="success"
                #     validresponse="true"
                elif currentQuestion in range(e3_start,e3_end):
                    r=UserAudio.query(UserAudio.user==user.email()).get()
                    if r :
                        q_status="submitted"
                        status="success"
                        validresponse="true"
                    else :
                        q_status="submitted"
                        status="success"
                        validresponse="true"
                elif currentQuestion in range(e4_start,e4_end):
                    q_status="submitted"
                    status="success"
                    validresponse="true"
                else :
                    q_status="submitted"
                    status="success"
                    validresponse="true"
                    cans=getAnswer(memcache.get(key="examid"),currentQuestion)
                    if cans == submittedans:
                        score = 1
                if validresponse=="true":
                    global status
                    status="success"
                    if q_status!="skip":
                        q_status="submitted"
                else:
                    global status
                    status="error"
                    global errortype

                # creating json file for error response
                # placing in to the database
                n1=int(currentQuestion)
                data=Response(examid=memcache.get("examid"),serialno=n1,useremailid=User(emailid=user.email(),name=user.nickname()),currentQuestion=str(currentQuestion),submittedans=submittedans,responsetime=responsetime,q_status=q_status,q_score=score)
                data.put()

                # added time taken based on the timer
                obj = {u"status":status , u"q_status":q_status, u"validresponse":validresponse, u"qid":currentQuestion}

            else:
                obj = {u"testEnd" : True}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

# this class is to get the ping requests every minute
class storetime(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        # todo handle user is None by forwarding to sign in?
        if user:
            duration = 60 * 60
            td = TestDetails.query(TestDetails.email==user.email()).get()
            if td is None:
                TestDetails(email=user.email(),test=True,delays=0.0).put()
                obj = {u"timeSpent":0, u"timeRemaining":duration, u"quizStatus": u"INPROGRESS"}
            else:
                if not td.testend:
                    currTime = datetime.datetime.now()
                    deltaTime = (currTime - td.lastPing).total_seconds()
                    if(deltaTime > 65.0):
                        td.delays = td.delays + deltaTime - 60.0
                        td.put()
                    timeSpent = (currTime - td.teststime).total_seconds() - td.delays

                    if timeSpent >= duration:
                        td.testend = True
                        quizStatus = u"END"
                    else:
                        quizStatus = u"INPROGRESS"
                    obj = {u"timeSpent" : timeSpent, u"quizStatus": quizStatus, u"timeRemaining" : duration - timeSpent}
                    td.lastPing = currTime
                    td.put()
                else:
                    obj = {u"quizStatus":u"END"}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

class AutosaveEssay(webapp2.RequestHandler):
    """ saving essay writing response"""
    def post(self):
        user = users.get_current_user()
        vals = json.loads(cgi.escape(self.request.body))
        vals = vals['jsonData']
        qid = vals['currentQuestion']
        ans = vals['draft']
        qattemptedtime = vals['responsetime']
        # print(vals)
        logging.error("This is an error message that will show in the console")
        data1 = EssayTypeResponse.query(EssayTypeResponse.useremailid == user.email(),
                                        EssayTypeResponse.qid == qid).get()
        # print(user.email())
        # print(qid)

        if data1:
            data1.qattemptedtime=qattemptedtime
            data1.ansText = ans
            data1.put()

        else:
            data = EssayTypeResponse(useremailid=user.email(),
                                     qid=qid,
                                     qattemptedtime=qattemptedtime,
                                     ansText = ans,
                                     )
            data.put()

        ss=json.dumps(vals)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)

class registrationdataHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            userDetails(name=self.request.get('name'),email=user.email(),rollno=self.request.get('rollno'),learningcenter=self.request.get('learningcenter'),batch = self.request.get('batch'),section = self.request.get('section')).put()
            self.redirect("/dashboard")
        else:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)

class startquiz(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            ss=Response.query(Response.useremailid.emailid==user.email()).get()
            if ss is None:
                Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
            sp=userDetails.query(userDetails.email==user.email()).get()
            template=None
            if sp is not None:
                template= JINJA_ENVIRONMENT.get_template('quiz.html')
                self.response.write(template.render())
            else:
                template= JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render())

class registration(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render())
        else:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
			
class WamiHandler(webapp2.RequestHandler):
    def post(self):
        user= users.get_current_user()
        if user:
            type = self.request.headers['Content-Type']
            blob_file_name = files.blobstore.create(mime_type=type, _blobinfo_uploaded_filename=self.get_name())
            with files.open(blob_file_name, 'a') as f:
                f.write(self.request.body)
            f.close()
            files.finalize(blob_file_name)
            blob_key = files.blobstore.get_blob_key(blob_file_name)
            UserAudio(blob1=blob_key,user=user.email()).put()
            logging.info("client-to-server: type(" + type +") key("  + str(blob_key) + ")")
			
		
    def get_name(self):
        name = "output.wav"
        params = cgi.parse_qs(self.request.query_string)
        if params and params['name']:
            name = params['name'][0];
        return name
            
class endtest(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            val = json.loads(cgi.escape(self.request.body))
            val = val['jsonData']
            # print(val)
            logging.error("error in finalScore")
            testend = val['testend']
            score = val['finalScore']
            spklink = val['spklink']
            # print(testend)
            data1 = TestDetails.query(TestDetails.email == user.email()).get()
            userdata=userDetails.query(userDetails.email == user.email()).get()
            learningcenter=userdata.learningcenter
            # print(user.email())      
            if data1:
                data1.testend = testend
                data1.score = score
                data1.learningcenter = learningcenter
                data1.testId = memcache.get(key= "examid")
                #data1.useraudiolink = spklink
                data1.put()          

application = webapp2.WSGIApplication([
    ('/', homepage),
    ('/checklogin',checklogin),
    ('/dashboard',Dashboard),
    ('/uploadStudents',uploadStudents),
    # ('/adminScreen1',AdminScreen1),
    ('/startquiz', startquiz),
    ('/savepersonaldata',registrationdataHandler),
    ('/registration',registration),
    ('/submitanswer', submitAnswer),
    ('/getResult', getResult),
    ('/getquizstatus', getquizstatus),
    ('/getScore', getScore),
    ('/autosaveEssay', AutosaveEssay),
    ('/uploadredirect',UploadRedirect),
    ('/upload_audio', AudioUploadHandler),
    ('/view_audio/([^/]+)?', ViewAudioHandler),
    ('/testtime',storetime),
	('/audio',WamiHandler),
    ('/endtest',endtest),
    ('/logout',logout),
], debug=True)
