#!/usr/bin/python 

import os
import time
import json
import subprocess
from mailer import Mailer
from datetime import date, timedelta

class Kube_interface(object):
    
    def __init__(self):
        self.old_nodes_data = []

    def load_clusters(self):
        context=[]
        mydirectory = os.path.dirname(__file__)
        with open(mydirectory + "/" + 'lab_cluster.txt', 'r' ) as f:
            for linenewline in f:
                line = linenewline[:-1] 
                context.append(line)
            return context

    def pull_kube_json(self, context_list):        
        json_data_list = []

        for c in context_list:
            my_dict={}
            try: 
                kubecontext="kubectl config use-context" + " " + c
                #kubecontext="kubectl config use-context" + " " + c
                process = subprocess.Popen(kubecontext.split(), stdout=subprocess.PIPE)
                output, context_err = process.communicate()
            
                my_dict["context"] = c
                kubenodes="kubectl get nodes -o json"
                process = subprocess.Popen(kubenodes.split(), stdout=subprocess.PIPE)
                nodeoutput, error = process.communicate()
            except:
                print >> sys.stderr, 'Cluster ' + c + 'Connection Error ' + str(datetime.now()) 
                pass

            data = json.loads(nodeoutput)
            my_dict["json"] = data
            json_data_list.append(my_dict)
        return json_data_list
        
    def packager(self, json_data_list):
    # Wrangle JSON output from kubectl 
        clusters = []
	bad_clusters = []
	for jsondata in json_data_list:
	    mydict = {}
	    mydict["context"] = jsondata["context"]
	    nodes = []
            
	    for s in jsondata["json"]["items"]:
                if s["status"]["conditions"]:
                    counter = 0
		    for n in s["status"]["conditions"]:
			if n["status"] == "Unknown":
		           
			    while counter == 0:
                                nodes.append(s["metadata"]["name"])
			        counter += 1
            mydict["nodes"]=nodes
	    clusters.append(mydict)
        
	# Maybe if I was a rockstar the dict would only have bad nodes, but it doesn't
	for cluster in clusters:
	    if cluster["nodes"]:
		bad_clusters.append(cluster)
		    
	        
	return bad_clusters

    def checking_nodes_down(self, new_nodes_data):
    # store data first. Ran again it checks new data against old data and any nodes NotReady are placed into the return dict
        bad_cluster = {}
	bad_clusters_list = []

	if not self.old_nodes_data:
	    self.old_nodes_data = new_nodes_data
	    return 

        for old_data in self.old_nodes_data:
	    counter = 0 
            context_count=0
            for new_data in new_nodes_data:
                print("new_data output--------") 
                print(new_data)
	        if old_data["context"] == new_data["context"]:
                    if context_count == 0:
                        print("running past context count")
                        bad_cluster["nodes"] = []
    	                for old_node in old_data["nodes"]:
		            for new_node in new_data["nodes"]:
		                if old_node == new_node:
			            if counter == 0: 
			                bad_cluster["context"] =  new_data["context"]
				        counter += 1
				    bad_cluster["nodes"].append(new_node)
                        context_count+=1
                    bad_clusters_list.append(bad_cluster)
        print("the total list------")
        print(bad_clusters_list)
        return bad_clusters_list


if __name__ == "__main__":
    mailthing = Mailer()
    interface = Kube_interface()
    
    while True: 
        #load file lines into list
        contexts = interface.load_clusters()
        
	#use context list to pull JSON data
	data = interface.pull_kube_json(contexts)
	#parse through JSON data and make a nice dictionary with keys = nodes, context.Bad nodes only
	bad_clusters = interface.packager(data)
	
        if bad_clusters:

            #This is the same dictionary structure as bad_clusters that can be loaded into emai
	    clusters_that_stay_down = interface.checking_nodes_down(bad_clusters)
	    # The first run cluster_that_stay_down is a None type. Check for this before trying to go further
	    if clusters_that_stay_down:
                #Mail the stuff 
                mailthing.mail_stuff(clusters_that_stay_down)
	else:
	    pass

	time.sleep(1)
    
    

    
