# 'Request' example added jjk  11/20/98

import win32ui
import dde
import time

# MT4|QUOTE!SPT_GLD
serv = dde.CreateServer()
serv.Create( "TestClient" )

conv = dde.CreateConversation( serv )
servicename = "testserv"

conv.ConnectTo( servicename, "top" )
#conv.Exec( "DoSomething" )
#conv.Exec( "DoSomethingElse" )

conv.ConnectTo( "RunAny", "ComputeStringLength" )
s = 'abcdefghi'
sl = conv.Request( s )
print 'length of "%s" is %s' % ( s, sl )




# Which items are available? (1)
strItem = "item" # SPT_GLD"

# I can't set a DDE-Timeout so I have to
# create my own timeout I will loop for 60 secs
startTime = time.time() + 20
answer = 'N\\A\x00'
timeOutCounter = 0
while ( answer == 'N\\A\x00' and startTime > time.time() ):
    timeOutCounter = timeOutCounter + 1;
    print "%d. try to retrieve valid funds for the internet" % timeOutCounter
    try:
        answer = conv.Request( strItem )
        win32ui.PumpWaitingMessages( 0, -1 )
    except:
        # if the timeout is reached abort here if not,
        # it will get into the next while loop
        if ( startTime < time.time() ):
            printLog( "\n\nERROR: Request failed." )
            ddeClient.Shutdown()
else:
    print 'answer is:%s' % answer
sys.exit()


'''
 Stuart Hungerford wrote:

 > Anyone out there have some example code
 > they can share with us?

 Stuart,

 I've been playing around with DDE control of a data-aquisition
 application called Windmill, which is supposed to work together with VBA
 and other MS stuff. I'd rather use Python 'cause (usual reasons).

 It took some trial and error to get the code going because of the rather
 terse doc's and my almost complete ignorance with respect to DDE.

 Here's my code:  (I hope the tabs are conserved)

 8<----------------------------------------------------
'''
# proof of concept of DDE control of Windmill
# Implements closed-loop control on top of Windmill demo 'DDEpanel'
import win32ui
import dde
import time
import re

# delays are needed to stop Windmill's DDEpanel from crashing :-(
def waitamoment():
    time.sleep( 0.2 )

# servicename of the data-aquisition process
servicename = "mt4"

# create a DDE client and start conversation
# this stuff is weird to me and I can't find a good reference
s = dde.CreateServer()

# what's the use of the string argument here?
s.Create( "" )
wm = dde.CreateConversation( s )

print "start test"

# get available channel names; connect to 'System' service
wm.ConnectTo( servicename, "System" )
reply = wm.Request( "Channels" )
# I'm not sure why I should use the token \011
reply = re.split( '\011', reply )

# find the index of an interesting variable
tindex = reply.index( "Tank_Level" )
sedindex = reply.index( "SedimentLevl" )

# choose other DDE service to get and set channel values
wm.ConnectTo( servicename, "Data" )
waitamoment()

# switch application to 'manual' mode
wm.Poke( "Auto", "0" )
waitamoment()

# sample control loop
for i in range( 20 ):
  # get data
  settings = wm.Request( 'AllChannels' )

  # split reply and extract some specific levels
  settings = re.split( '\011', settings )
  Tank_level = float( settings[tindex] )
  Sed_level = float( settings[sedindex] )

  # implement level control
  if ( Tank_level < 15 ) :
   wm.Poke( "Prod_Inlet", "1" )
   wm.Poke( "Prod_Outlet", "0" )
  if ( Tank_level > 16 ) :
   wm.Poke( "Prod_Inlet", "0" )
   wm.Poke( "Prod_Outlet", "1" )

  # sediment level control
  if ( Sed_level > 0.6 ):
   wm.Poke( "Sed_Outlet", "1" )
  if ( Sed_level < 0.55 ):
   wm.Poke( "Sed_Outlet", "0" )

  waitamoment()

# reset demo application mode to auto
wm.Poke( "Auto", "1" )
waitamoment()

# break DDE link
s.Destroy()

'''
 8<----------------------------------------------------
 --
 John van der Koijk.
 --
 J.F. van der Koijk Ph.D. -- TNO Institute of Industrial Technology

 PO Box 5073, 2600 GB, Delft, The Netherlands
 Phone +31 15 2608833, Fax +31 15 2608846
'''
