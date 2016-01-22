# -*- coding: utf-8 -*-
"""
socialGamers.py
This part is designed to support the data found in Section 4.A of the report.

@author: realhire
"""

from graphBuilder import graphBuilder

gamerTopic = {'140mafia': 2634, 'spymaster': 2304, 'vampirebite': 0}

i = 21
print "Gathering day ", i, "'s data..."
m = graphBuilder("tc21.txt")
print "apply topic filer and build the graph..."
m.topic_filter(gamerTopic)
print "outputing target file..."
m.outputToGexf()
print "socialGamer info analyzed complete. Results in", m.outfile


'''
# This part is a demonstration of topic collector and degree filter
print "find today's top ten topic in: ", m.infile, "..."
m.todayTopTenHashtag()
print "Today's top ten hashtags are: ", m.todayTopic
print "processing reply, retweet and hashtag: ", m.infile, "..."
m.processReplyRetweetHashtag(m.todayTopic)
degreeRange = [0, float("inf")]
print "filter out nodes not in degree range: [", degreeRange[0], ", ", degreeRange[1], "]..."
m.degree_filter(*degreeRange)
print "outputing target file..."
m.outputToGexf()
print "graph builder finised. Results in ", m.outfile
'''
