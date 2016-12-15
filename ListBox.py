import npyscreen


class ListBox(npyscreen.MultiLineEditableBoxed):
    
    def __init__(self,  *args, **kwargs):
        self._contained_widget.ALLOW_CONTINUE_EDITING=False
        super(ListBox, self).__init__(*args, **kwargs)
        if not('formklass' in kwargs):
            raise 'formklass is None'    
        self.form = kwargs['formklass']()
        self.entry_widget.set_up_handlers()
        self.entry_widget.handlers.update({
            ord('i'):   self.h_insert_value,
            ord('d'):   self.h_remove_channel
        })
        
        pass
        
    def h_insert_value(self, ch):
        self.form.edit()
        if hasattr(self.form, 'result'):
            self.entry_widget.values.insert(self.entry_widget.cursor_line,self.form.result)
            self.entry_widget.display()
        return #self.entry_widget.h_insert_next_line(ch)
        
    def h_remove_channel(self, ch):
        return self.entry_widget.h_delete_line_value(ch)
    
