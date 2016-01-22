# -*- coding: utf-8 -*-
"""
graphBuilder.py
This class will process one day's data and build graph information
Node: Twitter user, top ten hashtag are used as the nodes attribute
Edge: Reply and retweet. Each reply/retweet increase edge weight by 1.


@author: realhire
"""

import collections
import os.path
import networkx as nx

from lineParser import lineParser

class graphBuilder:
    def __init__(self, infile):
        assert os.path.isfile(infile)
        self.infile = infile
        self.G = nx.Graph()
        self.todayTopic = None
        self.MVP = None

    def processReplyRetweetHashtag(self, topicDict=None):
        if not topicDict:
            print "processReplyRetweetHashtag: topic dict is none. all topics are included."
        with open(self.infile, "r") as f:
            linenum = 0
            while 1:
                oneline = f.readline()
                if not oneline:
                    break
                linenum += 1
                if len(oneline) is 0 or oneline[0] is not 'T':
                    continue
                tline = oneline
                uline = f.readline()
                wline = f.readline()
                lp = lineParser(tline, uline, wline)
                self.G.add_node(lp.user)

                self.G.add_nodes_from(lp.refuser)
                for refusr in lp.refuser:
                    if not self.G.has_edge(lp.user, refusr):
                        self.G.add_edge(lp.user, refusr, weight=1)
                    else:
                        self.G[lp.user][refusr]['weight'] += 1

                for ht in lp.hashtag:
                    if topicDict and not topicDict.has_key(ht):
                        continue
                    nx.set_node_attributes(self.G, ht, {lp.user:True})

    def todayTopTenMVP(self):
        assert self.G
        ret = sorted([(v, k) for k, v in dict(self.G.degree(self.G.nodes())).items()])[-10:]
        ret.reverse()
        print ret
        self.MVP = [tup[1] for tup in ret]

    def todayTopTenHashtag(self):
        with open(self.infile, "r") as f:
            linenum = 0
            hashtags = collections.Counter()
            while 1:
                oneline = f.readline()
                if not oneline:
                    break
                linenum += 1
                if len(oneline) is 0 or oneline[0] is not 'T':
                    continue
                tline = oneline
                uline = f.readline()
                wline = f.readline()
                lp = lineParser(tline, uline, wline)
                if not len(lp.hashtag):
                    continue
                for ht in lp.hashtag:
                    hashtags[ht] += 1
            self.todayTopic = dict(hashtags.most_common(30))


    def degree_filter(self, degreeMin, degreeMax):
        removeList = []
        for nd in self.G.nodes():
            dg = self.G.degree(nd)
            if dg < degreeMin or dg > degreeMax:
                removeList.append(nd)
        self.G.remove_nodes_from(removeList)

    def topic_filter(self, topicDict):
        removeList = []
        self.processReplyRetweetHashtag(topicDict)
        for nd in self.G.nodes():
            if not len(self.G.node[nd]):
                removeList.append(nd)
        self.G.remove_nodes_from(removeList)

    def connection_filter(self, targetUser, removeTargetUser=False):
        neighbor = self.G.neighbors(targetUser)
        print targetUser, "has", len(neighbor), "neighbors"
        removeList = []
        for nd in self.G.nodes():
            if not nd in neighbor:
                removeList.append(nd)
        self.G.remove_nodes_from(removeList)
        if removeTargetUser:
            self.G.remove_node(targetUser)

    def outputToGexf(self, outfilename=None):
        if not outfilename:
            outfilename = self.infile.split('.')[0] + '.gexf'
        self.outfile = outfilename
        nx.write_gexf(self.G, outfilename)
