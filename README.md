# reimagined-alexa - Restaurant Feedback Application

Imagine if feedbacks in hotels/restaurants were taken on Alexa... Just to have a look,developed one. Check out the details below.

<b>	<h4> Step 1: Setup Alexa </h4> </b>
<ol>
	<li>
		<h5>Define intents - Here we have defined 2 of them</h5>
	</li>
	<ul>
		<li> Start Intent - Executes when the alexa feedback app opens and asks user for bill no.</li>
		<li>Answer Intent - Ask Questions and accepts answers with rating of 1 to 5, yes/no, good/avg/bad and imporvemnt category depending on the question</li>
		<li>Built in Intents - Cancel, Stop, Resume, Pause and Help Intents</li>
	</ul>
	<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_intent.PNG" />
	<br/>
	
  <li> <h5>Define slots - Define words user can say i.e set up the options </h5> </li>
		<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_slot.PNG" />
		<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_slotA.PNG" />
		<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_slotB.PNG" />
		<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_slotC.PNG" />
		<img src="https://github.com/RoyKiran/reimagined-alexa/blob/master/feedback/images/alexa_slotD.PNG" />
		<br/>
		
  <li> <h5>Define endpoints - The python script is hosted on AWS Lambda. So mention the endpoints of AWS lambda. </h5> </li>
	</ol>
	<br/>
  
  <b> <h4> Step 2: Setup Dynamo DB </h4> 	</b>
  Simply create a table "skill"
  <br/>
  
  <b> <h4> Step 3: Host your code </h4> </b>
  Link Dynamo DB and Alexa to Lambda function and finally code it.
	
