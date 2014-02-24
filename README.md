Residents of Katan
==================

This is a version of the board game Settlers of Catan built in python using the pygame graphics module. It was originally created as my term project for CMU's 15-112.  

Built using pygame 1.9.2 for mac, Python 2.7 32 bit. 

To run using terminal, cd into "Katan v0.5.py"'s parent folder, then enter: 
python2.7-32 "Katan v0.5.py"


Instructions
============

Basic rules of Catan can be found here: http://www.catan.com/files/downloads/soc_rv_rules_091907.pdf 

Warning: not all rules implemented, but more are on the way 2/23/14.  

Splash Screen Instructions:
---------------------------

Click on a Player to type a new name. 

It automatically clears the name when you click on the box. 

Set any player’s name to “” (which happens the first time you click the player’s name automatically) if you don’t want them to play. 

Use the left and right arrow keys to set the color. 


Main game
------------
###Objective: 

Get 10 victory points.
    
###How do you get victory points?  

1 settlement = 1 victory point 
        
1 city = 2 victory points
        
1 victory point development card = 1 victory point
    

###How do you build settlements? 

Click on an empty vertex. There must be 1 vertex in between every building.  After the initialization rounds, there must be a road leading to the vertex. 

###How do build roads? 

Click on an edge between 2 vertexes. There must be a road leading to the vertex or it must be adjacent to one of your buildings.

###What are the initialization rounds? 

When the game starts, every player gets 2 free settlements. Player 1 places one of each, then Player 2, until the last player. The last player then places his second road and settlements immediately after their first and the order reverses. The players get one of each resource their second settlement is on.  Then the game starts.

###What are the dice for?

The sum of the dice determines which hexagons produce resources that turn. Every player with a settlement adjacent to the hexagon gets 1 of the hexagon’s resource, every player with a city adjacent to the hexagon gets 2 of the hexagon’s resource. If you roll a 7 every player with more than 7 resources in their hand must discard half their resources (randomly done automatically by the computer), and you must move the robber. 

###Why do resources matter?

Building and buying dev cards cost resources:
    
    Road            1 Brick 1 Wood  

    Settlement      1 Brick 1 Wood 1 Sheep 1Wheat 
    
    City            2 Wheat 3 Stone 

    DevCard         1 Sheep 1 Stone 1 Wheat

###What is the robber?


It stops a hex from producing, even when the hex's number is rolled. 

###What are development cards?

Development cards or dev cards are special cards that give you a certain capability. They are as follows (the number of them in the parenthesis):

Soldier(14): move the robber

Victory Point(5): 1 victory point 

Monopoly(2): Every player must give you all of a given resource that you pick(it is the same for all players).

Road Builder(2): 2 free roads

Year of Plentey(2): 2 of a resource of your choice

When you buy a devcard it gives you a randomly selected devcards out of the dev cards remaining. 

###Key:    

The circles on vertexes that are solid are settlements. Their color is the player they belong to.

The circles on vertexes that have white circles in them are cities.

Red = Brick

Dark green = Wood

Light green = Sheep

Gray = stone

Gold = wheat

Yellow = desert. 

The number in the center of the hexagon is the sum of the dice that makes that hex produce. 

The solid black circle is the robber.

All the players in order are in a box on the left about the resource list.  The current player is boxed. 

The time left in the turn is above the player box.

###Controls:

Click on a vertex to build a settlement, or a city on top of a settlement 

Click on an edge between 2 vertices to build a road 

Click on a resources to trade it with the bank 

Click on “Buy” to buy a dev card 

Click on “Use” to use a dev card or see how many you have

One in the “select a development card” screen, click on a card to use it
