
import sys
import sqlite3
import logging

class knowledge_base:

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

   # {{{ get_inherited_properties():
   # Inference based in inheritance: The idea of this is that if an object 
   # belongs to a class (indicated by an IS_A link) it inherits all the 
   # properties of that class
   def get_inherited_properties(self, src, rel, results):
      try:
         cur = self.con.cursor()    
         cur.execute("select dst from relations_n2 "
            "where src='"+str(self.object_id(src))+"' "
            "and (relation='"+rel+"' or relation='IS-A');")

         data=cur.fetchall()
         for r in data:
            dst_name=self.object_name(r["dst"])
            self.get_inherited_properties(dst_name, rel, results)
            results.append(dst_name)
       
      except sqlite3.Error, e:
         print e
         print "Error %s:" % e.args[0]
         sys.exit(1)


   # }}}

   # {{{ clean()
   def clean(self):
      try:
         cur = self.con.cursor()    
         cur.execute("delete from relations_n2;")
         self.con.commit()
         
         cur.execute("delete from concepts;")
         self.con.commit()

      except sqlite3.Error, e:
         print e
         print "Error %s:" % e.args[0]
         sys.exit(1)
   # }}}

   # {{{ object_id()
   def object_id(self, name):
      try:
         cur = self.con.cursor()    
         cur.execute("select id from concepts where name='"+name+"';")
         data=cur.fetchall()
         
         if len(data)>0:
            object_id=data[0]["id"]
         else:
            cur.execute("insert into concepts (name) values ('"+name+"');")
            self.con.commit()
            object_id=cur.lastrowid

      except sqlite3.Error, e:
         print e
         print "Error %s:" % e.args[0]
         sys.exit(1)

      return object_id
   # }}}

   # {{{ object_name()
   def object_name(self, object_id):
      try:
         cur = self.con.cursor()    
         cur.execute("select name from concepts where id='"+str(object_id)+"';")
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

      src_id=self.object_id(src) 
      dst_id=self.object_id(dst) 
     
      try:
         cur = self.con.cursor()    
         cur.execute("insert into relations_n2 "
            "(id_user, relation, src_quantifier, src, "
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

   # {{{ query_dst()
   def query_dst(self, rel, src): 
      results=[]
      try:
         # IS-A relation is implicit in all relations. 
         self.get_inherited_properties(src, rel, results)

         #When we receibe an IS-A question we add HAS-ATTRIBUTE. 
         if rel=='IS-A':
            self.get_inherited_properties(src, 'HAS-ATTRIBUTE', results)

         return results

      except sqlite3.Error, e:
         print e
         print "Error %s:" % e.args[0]
         sys.exit(1)
   # }}}




