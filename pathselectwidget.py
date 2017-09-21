import os
import ipywidgets as widgets

class PathSelectWidget():
    def __init__(self,name=None):
        self._path_name = name
        self._curr_path = os.getcwd()
        self._w_select_path = widgets.Select(options=[".",".."],value=".")
        self._w_text_curr_path = widgets.Text(value = self._curr_path,layout=widgets.Layout(width="50%"))
        self._fill_options()
        self._w_select_path.observe(self._on_select,names="value")
        self._box_widgets()
        
    def _box_widgets(self):
        vbox1 = widgets.VBox([widgets.Label("Current Path:"),self._w_text_curr_path],layout=widgets.Layout(width="50%"))
        vbox2 = widgets.VBox([widgets.Label("Select:"),self._w_select_path])
        self._box = widgets.HBox([vbox1,vbox2])
        self._w_text_curr_path.layout.width = "90%"
        self._accordion = widgets.Accordion(children = [self._box])
        self._accordion.set_title(0,"Path Selection: "+("" if self._path_name is None else self._path_name))
        self._accordion.observe(self._on_accordion_fold)
    
    def _fill_options(self):
        if os.path.isdir(self._curr_path):
            options = [".",".."]
            options = options +[p+"/" for p in os.listdir(self._curr_path) if os.path.isdir(os.path.join(self._curr_path,p))]
            options = options +[p for p in os.listdir(self._curr_path) if not os.path.isdir(os.path.join(self._curr_path,p))]
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
        
        
#TEST
from IPython.display import display
pw = PathSelectWidget("my_file")
display(pw.get_widget())
mf = MultiFileSelectionWidget(["f1","f2"])
display(mf.get_widget())
