#!/bin/python

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, timedelta, datetime
from jinja2 import Template 

class Mailer(object):

    def mail_stuff(self, bad_clusters):
        address_to = 'myaddress@test.com'
        address_from = 'kubewatcher@test.com'
        recipients = ['ryan_wright@test.com']
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "NotReady Nodes Detected"
        msg['From'] = address_from
        msg['To'] = ", ".join(recipients)
        
        text = "Please use an HTML compatible email client to view this message"
        html = ("""
        <html> 
         <head>
	 </head>
          <body>
            <h1>Nodes in NotReady State For Over 5 Minutes<h1><br>
    	
    	{% for context in bad_clusters %}
	    
            <div>
	    <table style="align: center; font-family: Arial, Helvetica;">
    	  <tr>
    	  <th>{{context["context"]}}<th>
    	  </tr>
    	{% for node in context["nodes"]%}
    	  <tr>
    	  <td>{{ node }}</td>
    	  </tr>
    	{% endfor %}
    
    	</table>
	</div>
    	{% endfor %}
    	</body>
        </html> 
        """)
        
        template = Template(html)
	rendered_html = template.render(bad_clusters = bad_clusters)
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(rendered_html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        
        try:
	    s = smtplib.SMTP('mailrelay.test.com')
            s.sendmail(address_from, recipients, msg.as_string())
            s.quit()
	
	except:
            print >> sys.stderr, 'Mail connection error ' + str(datetime.now())
            #print("mail connection error")
	    pass
	    
