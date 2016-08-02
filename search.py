import DirNav;
import threading;
import time;
import os;

results = list();
results2 = dict();#results dictionary of {result:path}
no_d_threads = 0; #no. of completed d_threads
no_f_threads = 0; #no. of completed f_threads

class SearchThread(threading.Thread):
    def __init__(self,d_or_f,path,search_string):
        threading.Thread.__init__(self);

        self.d = False;
        self.f = False;
        if d_or_f == "dir":
            self.d = True;
            print("checking : "+path+" as DIR");
        else:
            self.f = True;
            print("checking : "+path+" as FILE");

        self.path = path;
        self.search_string = search_string;
        d_threads = list(); #list of all dir checking threads
        f_threads = list(); #list of all file checking threadsthreads
        #self.dn = DirNav.DirectoryNavigator(self.path,verbose=True);
        return;

    def run(self):
        global no_f_threads;
        global no_d_threads;
        if self.d == True:
            self.in_search(self.path);
            pass;
        elif self.f == True:
            f = open(self.path,"r");
            if self.search_string in self.get_fname(self.path):
                results.append(self.path);
                no_f_threads +=1;
                return;
            elif self.file_search(f) == True:
                #results.append(self.path);
                results2[self.get_fname(self.path)] = self.path;
                no_f_threads +=1;
                return;
            else:
                no_f_threads +=1;
                return;
        return;

    def get_fname(self,path):
        dir_list = path.split("/");
        last = dir_list.pop();
        return(last);

    def in_search(self,path):
        global results;
        return;

    def file_search(self,f_handle):
        global results;
        content = f_handle.readlines();
        for line in content:
            #print(line);
            if self.search_string in line:
                return(True);
        return(False);



def search(search_string,start_path):
    #print("got : "+search_string+" and "+start_path);
    d_dict = dict(); #dictionary of {directory_name:path}
    f_dict = dict(); #dictionary of {file_name:path}
    d_threads = list(); #list of all dir checking threads
    f_threads = list(); #list of all file checking threads
    global no_d_threads;
    global no_f_threads;
    start_time = time.time();
    end_time = 0;


    if start_path == ".":
        start_path = os.getcwd();
    elif start_path == ".." or start_path == "../":
        start_path = os.getcwd()+"/../";


    dn = DirNav.DirectoryNavigator(start_path);
    dir_full = dn.get_dir_list();
    for d in dir_full.keys():
        if dir_full[d] == "dir":
            d_dict[d] = dn.get_system_path()+d;
        else:
            f_dict[d] = dn.get_system_path()+d;
    #print(d_dict);
    #print(" :: ");
    #print(f_dict);

    for d in d_dict.keys():
        dt = SearchThread("dir",d_dict[d],search_string);
        #dt.start();
        d_threads.append(dt);
    for f in f_dict.keys():
        df = SearchThread("file",f_dict[f],search_string);
        df.start();
        df.join();
        f_threads.append(df);

    while (True):
        if no_f_threads == len(f_threads):
            print(results2);
            break;
        else:
            #print("...");
            time.sleep(1);

    end_time = time.time();
    t_diff = end_time - start_time;
    print("Time taken : "+str(t_diff));
    return(results2);

if __name__ == "__main__":
    r = search("Dir","../py-scripts");
    exit();
