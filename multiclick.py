from gi.repository import GObject, Gtk, Gdk, Gedit

import re

class MultiClick(GObject.Object, Gedit.ViewActivatable):
  __gtype_name__ = "MultiClick"
  view = GObject.property(type=Gedit.View)
  
  def __init__(self):
    GObject.Object.__init__(self)
    self._handler_id = None
  
  # hook and unhook from view events
  def do_activate(self):
    # compile regexes to use for matching
    self.match_word = re.compile('^(\\w+|\\w[\\w-]*\\w)$')
    self.match_chain = re.compile('^\\w+[\\w-]*?((->|::|@|\\.|[/:.]+|[\\\\.:]+)[\\w-]*\\w+)*$')
    # retain a reference to the document
    self.doc = self.view.get_buffer()
    # bind events
    self._handler_id = self.view.connect('event', self.on_event)
  def do_deactivate(self):
    if (self._handler_id is not None):
      self.view.disconnect(self._handler_id)
      self._handler_id = None
      
  def on_event(self, view, event):
    if (event.type == Gdk.EventType._2BUTTON_PRESS):
      self.select_word()
      return(True)
    elif (event.type == Gdk.EventType._3BUTTON_PRESS):
      self.select_chain()
      return(True)
    return(False)
  
  def get_selection_iters(self):
    start = self.doc.get_iter_at_mark(self.doc.get_insert())
    end = self.doc.get_iter_at_mark(self.doc.get_selection_bound())
    if (start.get_offset() <= end.get_offset()):
      return((start, end))
    else:
      return((end, start))
  
  def is_word(self, start_iter, end_iter):
    text = self.doc.get_text(start_iter, end_iter, True)
    return(self.match_word.match(text) is not None)
    
  def is_chain(self, start_iter, end_iter):
    text = self.doc.get_text(start_iter, end_iter, True)
    return(self.match_chain.match(text) is not None)
  
  def expand_iters(self, start_iter, end_iter, test, try_count=2):
    go_back = True
    go_forward = True
    while (go_back or go_forward):
      if (go_back):
        last_offset = start_iter.get_offset()
        tries = 0
        while(True):
          if (start_iter.is_start()):
            start_iter.set_offset(last_offset)
            go_back = False
            break
          start_iter.backward_char()
          if (test(start_iter, end_iter)):
            break
          tries += 1
          if (tries >= try_count):
            start_iter.set_offset(last_offset)
            go_back = False
            break
      if (go_forward):
        last_offset = end_iter.get_offset()
        tries = 0
        while(True):
          if (end_iter.is_end()):
            end_iter.set_offset(last_offset)
            go_forward = False
            break
          end_iter.forward_char()
          if (test(start_iter, end_iter)):
            break
          tries += 1
          if (tries >= try_count):
            end_iter.set_offset(last_offset)
            go_forward = False
            break
  
  def select_word(self):
    (start_iter, end_iter) = self.get_selection_iters()
    self.expand_iters(start_iter, end_iter, self.is_word, 2)
    self.doc.select_range(start_iter, end_iter)
    
  def select_chain(self):
    (start_iter, end_iter) = self.get_selection_iters()
    self.expand_iters(start_iter, end_iter, self.is_chain, 5)
    self.doc.select_range(start_iter, end_iter)
    