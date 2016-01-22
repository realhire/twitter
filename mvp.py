# -*- coding: utf-8 -*-
"""
mvp.py
Find Twitter MVP and check whether their topic overlap with their follower/sub
scribers; topic

@author: realhire
"""

from graphBuilder import graphBuilder

i = 21
print "Gathering day ", str(i) + "'s data"
m = graphBuilder("tc30.txt")
print "Build the graph, all nodes included..."
m.processReplyRetweetHashtag()
print "Find today's MVP:..."
m.todayTopTenMVP()
for mvp in m.MVP:
    print mvp, ':\tTopic: ', m.G.node[mvp]

""" ''' Singer Trey '''
interestedUser = 'songzyuuup'
print "Now we are interested in", interestedUser
print "This account's topics are:", list(m.G.node[interestedUser])
print "Filter out all user not connected to", interestedUser
m.connection_filter(interestedUser, removeTargetUser=True)
print "outputing target file..."
m.outputToGexf("Day"+str(i)+"MVP"+interestedUser+".gexf")
print "MVP connection info analyzed complete. Results in", m.outfile
"""

