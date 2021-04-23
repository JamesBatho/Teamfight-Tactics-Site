
Capstone Project 1 for Springboard's Software Engineering Course

### Link to Schema Diagram

https://dbdiagram.io/d/600bb2c880d742080a37878b

a. The title of your site and a link to the URL where it is deployed

#Advanced Teamfight Tactics

###Introduction 
Greetings summoner, (or future summoner) welcome to my site. Here you'll be able to make your wildest dreams come true, well maybe not too too wild.

This site is intended to provide players of Riot's *Teamfight Tactics* with additional insight into their own gameplay and the gameplay of others. Allowing them to improve at a much more rapid pace. 

To access the site please click [here](https://adv-tft.herokuapp.com/teambuilder). Or copy: https://adv-tft.herokuapp.com/teambuilder into your address bar. 

####Impetus for Creation
This site was born out of Springboard's software engineering course as my first Capstone Project. The main goals of this project were to generate a website that pull data from an API and provides a user with basic CRUD functionality on the site. 


###Functionality
This website provides multiple features to provide a seamless user experience. Some of the highlights are:
	* The ability to create a user account
	* Allow the user to see compositions created by other users
	* Authentication and authorization for logging in and protecting certain routes
	* The ability to view statistics about the user's recent games
	* Allowing the user to create and save a new composition using Teambuilder
	* Allow the creator of a composition to edit it

###User Flow
A typical user will arrive at the anonymous homepage where they can view recent compositions created by our users and see the `Signup` and `Login` buttons. 

After clicking `Signup` the user is redirected to a signup form. Once the form is filled out and is validated the user will be redirected back to the logged-in homepage. Here they can view their own statistics and have access to the recent compositions as well as the `Teambuilder`. 

Clicking the `Teambuilder` button redirects the user to the `Teambuilder` route. Here the user can create a composition from any of the champions in set 4. Once the user hits `Save` they are redirected to the homepage where they can now see their composition. The user who created the composition can click on it to redirect to a page where they can edit and save the updated composition. Where they will be redirected back to the homepage. 

Once the user is done using the site they can click `Logout` to end their session and complete their use of the site.  

###API Information
The API used to gather player and game data is Riot's 
_____ 

This site uses a free API key provided by RIOT to developers. Unfortunately it is only valid for 24hours and must be refreshed every day in order to keep pulling player data. 

A reference for the API can be found [here](https://developer.riotgames.com/apis#tft-league-v1) 
https://developer.riotgames.com/apis#tft-league-v1 

While the Base URL for API requests uses this string:
`https://na1.api.riotgames.com/tft`

###Technologies Used
####Frontend 

This site uses Python and Flask to define the routes for the frontend. Each route uses HTML with Jinja templating, JavaScript and CSS to show the content to the user. 

#####Forms
Forms are created using Flask-WTForms and rendered using Jinja templating. 

####Backend

Communication with the database and database model creation is done through Flask SQLAlchemy. 

#####Database
This site uses Postgres and Heroku's Postgres extension to provide database functionality. 

#####Authentication and Authorization

Authentication is done using Bcrypt while Authorization is complete by using Flask's `g` object to keep track of the current user. 



###Future Site Improvements

While the site is currently functional a number of imrovements have been identified that would greatly improve the user's experience. 

In no particular order: 
* Provide additional stats about the user's games
* Allow for "liking" of comps to give them user-based ratings
* Show traits for compositions
* Allow for sorting of recent comps by: champion, likes, traits
* Generate additional new stats for team compositions such as: 
* 	Team Utility Score- based on amount of crowd control
*  Team Damage Score- based on DPS or total dmg at 10 seconds
* Generate additional stats for champions
* 	Incorporate ability use into dps 
*  Provide some tips for newer players and general strategy ideas.




e. Keep the API in there, and if you have anything to say about the API then
add some notes
f. Identify the technology stack used to create your website
g. Include anything else that you feel is important to share