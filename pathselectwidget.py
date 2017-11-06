'''
@author grcanosa
        http://github.com/grcanosa
A Path Selection widget for jupyter notebooks.        
'''
import os
import ipywidgets as widgets

class PathSelectWidget():
    def __init__(self,name=None):
        self._path_name = name
        self._show_hidden_files = False
        self._curr_path = os.getcwd()
        self._w_select_path = widgets.Select(options=[".",".."],value=".")
        self._w_text_curr_path = widgets.Text(value = self._curr_path)
        self._fill_options()
        self._w_button_go_current_path = widgets.Button(description="Go to current path!")
        self._w_check_hidden_files = widgets.Checkbox(value=False,description="Show Hidden Files")
        self._box_widgets()
        self._observe_all()
        
        
    def _observe_all(self):
        self._w_select_path.observe(self._on_select,names="value")
        self._accordion.observe(self._on_accordion_fold)
        self._w_button_go_current_path.on_click(self._on_current_path_click)
        self._w_check_hidden_files.observe(self._on_hidden_files_check,names="value")
        
    def _box_widgets(self):
        help_menu = widgets.HBox([self._w_button_go_current_path,self._w_check_hidden_files])
        vbox1 = widgets.VBox([widgets.Label("Current Path:"),self._w_text_curr_path,help_menu],layout=widgets.Layout(width="60%"))
        vbox2 = widgets.VBox([widgets.Label("Select:"),self._w_select_path],layout=widgets.Layout(width="40%"))
        self._box = widgets.HBox([vbox1,vbox2])
        self._w_text_curr_path.layout.width = "95%"
        self._w_select_path.layout.width = "95%"
        self._accordion = widgets.Accordion(children = [self._box])
        self._accordion.set_title(0,"Path Selection: "+("" if self._path_name is None else self._path_name))
        
    
    def _fill_options(self):
        if os.path.isdir(self._curr_path):
            options = [".",".."]
            dirs = []
            files = []
            if self._show_hidden_files:
                dirs = [p+"/" for p in os.listdir(self._curr_path) if os.path.isdir(os.path.join(self._curr_path,p))]
                files = [p for p in os.listdir(self._curr_path) if not os.path.isdir(os.path.join(self._curr_path,p))]
            else:
                dirs = [p+"/" for p in os.listdir(self._curr_path) if (os.path.isdir(os.path.join(self._curr_path,p)) and p[0] != ".")]
                files = [p for p in os.listdir(self._curr_path) if (not os.path.isdir(os.path.join(self._curr_path,p)) and p[0] != ".")]
            dirs.sort()
            files.sort()
            options = options + dirs + files
            self._w_select_path.options = options
        else:
            self._w_select_path.options=[".",".."]
        self._w_select_path.value = '.'
        
    def _set_new_path(self):
        self._w_text_curr_path.value = self._curr_path
        
    
    def _on_select(self,change):
        new_val = change["new"]
        if new_val == ".":
            self._set_new_path()
        elif new_val == "..":
            self._curr_path = os.path.dirname(os.path.abspath(self._curr_path))
        else:
            self._curr_path = os.path.join(self._curr_path,new_val)
        self._fill_options()
        
    def _on_accordion_fold(self,change):
        if change["name"] == "selected_index":
            if change["new"] == None:
                self._accordion.set_title(0,"Selected path: "+self._curr_path if self._path_name is None else self._path_name+": "+self._curr_path)
            else:
                self._accordion.set_title(0,"Path Selection: "+("" if self._path_name is None else self._path_name))
    
    def _on_current_path_click(self,change):
        self._curr_path = os.getcwd()
        self._fill_options()
        self._set_new_path()
        
    def _on_hidden_files_check(self,change):
        self._show_hidden_files = change["new"]
        self._fill_options()
    
    def get_path(self):
        return self._curr_path
        
    def get_widget(self):
        return self._accordion
        
 
class MultiFileSelectionWidget():
    def __init__(self,filenames):
        self._filenames = filenames
        self._create_widgets()

    def _create_widgets(self):
        self._widgets = [PathSelectWidget(f) for f in self._filenames]
        self._vbox = widgets.VBox([w.get_widget() for w in self._widgets])
    
    def get_paths(self):
        return {f:p.get_path() for f,p in zip(self._filenames,self._widgets)}
    
    def get_widget(self):
        return self._vbox
        
if __name__ == "__main__":        
    #TEST
    from IPython.display import display
    pw = PathSelectWidget("my_file")
    display(pw.get_widget())
    mf = MultiFileSelectionWidget(["f1","f2"])
    display(mf.get_widget())
