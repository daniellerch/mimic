
import sys
import sqlite3
import logging
from language.globals import IS_A_RELATION, HAS_ATTRIBUTE_RELATION

class Concept:

    # {{{ __init__()
    def __init__(self, name):

        self.kb=KnowledgeBase()

        try:
            cur = self.kb.con.cursor()     
            cur.execute("select id, gender from concepts where name='"+name+"';")
            data=cur.fetchall()
            
            if len(data)>0:
                concept_id=data[0]["id"]
                gender=data[0]["gender"]
            else:
                cur.execute("insert into concepts (name) values ('"+name+"');")
                self.kb.con.commit()
                concept_id=cur.lastrowid
                gender='m'

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        self.id=concept_id
        self.name=name
        self.gender=gender
    # }}}

    # {{{ set_gender()
    def set_gender(self, gender='m'):

        name=self.name
        try:
            cur = self.kb.con.cursor()     
            cur.execute("select gender, gender_score \
                from concepts where id='"+str(self.id)+"';")
            data=cur.fetchall()
            
            if len(data)>0:
                if data[0]["gender"]==gender:
                    cur.execute("update concepts set gender_score=gender_score+1 \
                        where id='"+str(self.id)+"';")
                elif data[0]["gender_score"]>0:
                    cur.execute("update concepts set gender_score=gender_score-1 \
                        where id='"+str(self.id)+"';")
                else:
                    cur.execute("update concepts set gender='"+gender+"', \
                        gender_score=1 where id='"+str(self.id)+"';")

                self.kb.con.commit()

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return
    # }}}

    # {{{ get_gender()
    def get_gender(self):
        return self.gender
    # }}}


class Source:
    """
    Source of the information. It can be a user or a resource as for example
    Wikipedia or a learning package

    Attributes:
        id:    identifier of the source
        name: name of the source
    """

    # {{{ __init__()
    def __init__(self, name):

        self.kb=KnowledgeBase()

        # MASTER is a special user that can not be modified. This user is
        # used to teach the system.
        if name=='MASTER':
            self.id=0
            self.name='MASTER'
            return

        try:
            cur = self.kb.con.cursor()     
            cur.execute("insert into knowledge_source \
                         (name) values ('"+name+"');")
            id_user=cur.lastrowid
            self.kb.con.commit()
            self.id=id_user
            self.name=name

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)
    # }}}

    # {{{ set_name()
    def set_name(self, name):

        if name=='MASTER':
            self.id=0
            self.name='MASTER'
            return

        try:
            cur = self.kb.con.cursor()
            # we do not want to overwrite MASTER, that is id=0
            cur.execute("update knowledge_source set name='"+name+"' \
                         where id='"+str(self.id)+"' and id!=0;")
            self.kb.con.commit()
            self.name=name

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)
    # }}}


class KnowledgeBase:

    # {{{ __init__()
    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self):
        try:
            self.con = sqlite3.connect('knowledge.db')
            self.con.row_factory = self._dict_factory

        except sqlite3.Error, e:
            logging.debug(e)
            logging.debug(e.args[0])
            sys.exit(1)
    # }}}
 
    # {{{ __del__()
    def __del__(self):
        self.con.close()
    # }}}

    # {{{ get_parent_concepts():
    def get_parent_concepts(self, src, results=[]):
        """Follow IS_A_RELATION links and prepare a list with all the parent
        concepts. This list is useful because the child concepts inherit
        the properties of the parents."""
        try:
            cur = self.con.cursor()
            q = "select dst from relations_n2 " \
                "where src='"+str(self.concept_id(src))+"' " \
                "and relation='"+IS_A_RELATION+"';"
            print q
            cur.execute(q)
    
            data=cur.fetchall()
            for r in data:
                dst_name=self.concept_name(r["dst"])
                self.get_parent_concepts(dst_name, results)
                results.append(dst_name)
         
        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return results
    # }}}

    # {{{ get_properties():
    def get_properties(self, src_list, rel):

        src_sql = "c1.name in ('"+"', '".join(src_list)+"')"
        try:
            cur = self.con.cursor()
            q = "select c2.name dst " \
                "from relations_n2 r, concepts c1, concepts c2 " \
                "where "+src_sql+" and r.relation='"+rel+"' " \
                "and r.src=c1.id and r.dst=c2.id;"
            print q
            cur.execute(q)

            data=cur.fetchall()
            prop=[]
            for r in data:
                prop.append(r["dst"])
            return prop         

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return None
    # }}}

    # {{{ clean()
    def clean(self):
        try:
            cur = self.con.cursor()     
            cur.execute("delete from relations_n2;")
            cur.execute("delete from concepts;")
            cur.execute("delete from knowledge_source where id!=0;")
            self.con.commit()

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)
    # }}}

    # {{{ concept_id()
    def concept_id(self, name):
        try:
            cur = self.con.cursor()     
            cur.execute("select id from concepts where name='"+name+"';")
            data=cur.fetchall()
            
            if len(data)>0:
                concept_id=data[0]["id"]
            else:
                cur.execute("insert into concepts (name) values ('"+name+"');")
                self.con.commit()
                concept_id=cur.lastrowid

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return concept_id
    # }}}

    # {{{ concept_name()
    def concept_name(self, concept_id):
        try:
            cur = self.con.cursor()     
            cur.execute("select name from concepts where id='"+str(concept_id)+"';")
            data=cur.fetchall()
            
            if len(data)>0:
                return data[0]["name"]

        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return ""
    # }}}

    # {{{ add_2n_relation()
    def add_2n_relation(self, idu, rel, src_q, src, dst_q, dst):

        src_id=self.concept_id(src) 
        dst_id=self.concept_id(dst) 
      
        try:
            cur = self.con.cursor()     
            cur.execute("insert into relations_n2 "
                "(id_knowledge_source, relation, src_quantifier, src, "
                " dst_quantifier, dst) values "
                "('"+str(idu)+"','"+rel+"','"+src_q+"','"+str(src_id)+"', "
                " '"+dst_q+"','"+str(dst_id)+"');"
                )

            self.con.commit()
            
        except sqlite3.Error, e:
            print e
            print "Error %s:" % e.args[0]
            sys.exit(1)
    # }}}

    # {{{ query_2n_relation()
    def query_2n_relation(self, rel, src): 
        
        src_list = self.get_parent_concepts(src, results=[])
        src_list.append(src)
        result = list(src_list)

        #When we receibe an IS-A question we add also HAS-ATTRIBUTE relation. 
        prop=[]
        if rel==IS_A_RELATION:
            prop = self.get_properties(src_list, HAS_ATTRIBUTE_RELATION)

        prop += self.get_properties(result, rel)
        if rel==IS_A_RELATION:
            prop += result

        if src in prop:
            prop.remove(src)

        return prop
    # }}}




