# -*- coding: utf-8 -*-
"""
lineParser.py
This module will handle one entry and extract the entry's date, poster id,
at-user id and hashtag.


@author: realhire
"""

from datetime import datetime

class lineParser:
    def extractDate(self, oneline):
        ymd = oneline.split()[1].split('-')
        hms = oneline.split()[2].split(':')
        hms = map(int, ymd + hms)
        d = datetime(*hms)
        return d

    def extractUsr(self, oneline):
        return oneline.split('/')[-1][:-1].lower()

    # User can be referred back to back.
    # @usr1@usr2 can be recognized as two usrs.
    def extractRefUsr(self, oneline):
        ret = []
        sep = oneline.split()
        for tp in sep:
            if tp[0] != '@' or len(tp) is 1:
                continue
            usr = ''
            pureNumeric = True
            for c in tp[1:]:
                if c in "# ~!@$%^&*.,<>?/':;[]}{|\+=-)(*\t\"":
                    break
                usr += c
                pureNumeric = pureNumeric and c.isdigit()
            if (len(usr) > 1 or (len(usr) is 1 and usr in "abcdefghijklmnopqrstuvwxwy")) and not pureNumeric:
                ret.append(usr.lower())
        return ret

    # Requirement: 104 chars max, cannot has consecutive hashtag.
    # Cases:
    #    #aaa#bbb -> aaa
    #    #aaa?    -> aaa
    #    #0aa     -> 0aa
    #    #1999    -> none      NOT IMPLEMENTED
    #    #aaa?bbb--> aaa
    #    #AAA and #aaa are same
    def extractHashTag(self, oneline):
        ret = []
        sep = oneline.split()
        for tp in sep:
            if tp[0] != '#' or len(tp) is 1:
                continue
            tpk = tp.split('#')[1]
            tpp = ''
            pureNumeric = True
            for c in tpk:
                if c in "# ~!@$%^&*.,<>?/':;[]}{|\+=-)(*\t\"":
                    break
                tpp += c
                pureNumeric = pureNumeric and c.isdigit()
            """Note: For input #aaa#aaa this function will return two topics."""
            if len(tpp)>1 and not pureNumeric:
                ret.append(tpp.lower())
        return ret

    def __init__(self, tline=None, uline=None, wline=None):
        try:
            self.date = self.extractDate(tline)
            self.user = self.extractUsr(uline)
            self.refuser = self.extractRefUsr(wline)
            self.hashtag = self.extractHashTag(wline)
        except:
            self.date = self.user = self.refuser = self.hashtag = None