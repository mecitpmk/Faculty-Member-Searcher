from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import dbm,pickle,os,time,requests
print(os.listdir())


"""
Changes Notes:
    Professors Informations holds as an object.
    as you know Its much easier than accessing dictionary.
"""



class Professors:
    all_prof = []
    def __init__(self,name,link,department):
        self.name = name
        self.link = link
        self.department = department
        self.informations = []
        Professors.all_prof.append(self)
    def __repr__(self):
        return self.name

class GraphicalInferface(Frame):
    def __init__(self,parent):
        """
        Notes:
            if the database available program don't have to fetch all data again from website.
        """
        self.parent=parent
        Frame.__init__(self,parent)
        self.grid()
        self.active_database=False
        self.university_links="https://www.sehir.edu.tr"
        self.initializeGUI()
        self.update()
        if "sehir_professors_infos.db.dir" in os.listdir():
            print("DATABASE IS CHECKING IF UPDATE REQUIRES OR NOT PLEASE WAIT !! ! !!! ! ")
            self.progres_info_lab.config(text="UPDATE REQUIRES CHECKING \n PLEASE WAIT! \n Don't Touch!",bg="blue")
            self.update()
            self.active_database=True
            self.DownloadDatabase()
            update_requries=self.check_update_Requirements()
            if update_requries:
                self.active_database=False
                self.progres_bar_comp.config(text="Changes Identified! Fetch Again!",bg="blue")
                self.original_settings(self.progres_bar_comp)
            else:
                self.departments_combobox.configure(values=self.all_departments)
                self.departments_combobox.current(0)
                self.selected_department=self.departments_combobox.get()
                self.progres_bar_comp.config(text=" No Update Requires \nDatabase IS ACTIVE!",bg="green")
                self.collect_informations()
    def initializeGUI(self):
        self.BIG_TEXT=Label(self,text="Sehir Faculty Member Search Engine",bg="red",fg="white",font=("Helvetica",14,"bold"),anchor=CENTER)
        self.BIG_TEXT.grid(row=0,column=0,sticky=E+W+S+N,columnspan=5)

        Label(self,text="Faculty Profile Url:").grid(row=1,column=0,padx=10,pady=10,sticky=E)
        
        self.faculty_link_entry=Entry(self,width=100)
        self.faculty_link_entry.grid(row=1,column=1,pady=10,sticky=W,padx=10,columnspan=4)
        self.faculty_link_entry.insert(0,"https://www.sehir.edu.tr/en/academics/college-of-engineering-and-natural-sciences/academic-staff")

        self.fetch_p_button=Button(self,text="Fetch Profiles",command=self.fetch_profile)
        self.fetch_p_button.grid(row=2,column=1,pady=10)

        self.progres_info_lab=Label(self,text="")
        self.progres_info_lab.grid(row=3,column=0,padx=10,pady=10,sticky=E)

        self.progress_bar=Canvas(self,bg="grey",width=356,height=20,borderwidth=3,relief="sunken")
        self.progress_bar.grid(row=3,column=1,padx=10,pady=10)

        self.progres_bar_comp=Label(self,text="0% Completed.")
        self.progres_bar_comp.grid(row=3,column=2,padx=10,pady=10)

        self.testF=Frame(self,relief=GROOVE,borderwidth=4)
        self.testF.grid(row=4,column=1,pady=15)

        Label(self.testF,text="Keywords:").grid(row=0,column=0,padx=10,pady=10,sticky=E)

        self.keyword_entry=Entry(self.testF)
        self.keyword_entry.grid(row=0,column=1,pady=10,sticky=W)

        Label(self.testF,text="Department").grid(row=0,column=2,padx=10,pady=10)
        
        self.departments_combobox=ttk.Combobox(self.testF)
        self.departments_combobox.grid(row=0,column=3,padx=10,pady=10)
        self.departments_combobox.bind("<<ComboboxSelected>>",self.department_selected)


        self.search_buttons=Button(self.testF,text="Search",width=30,command=self.find_persons)
        self.search_buttons.grid(row=1,column=0,padx=10,pady=10,columnspan=4)

        self.treeFrame=Frame(self,relief=GROOVE,borderwidth=2)
        self.treeFrame.grid(row=5,column=0,pady=10,columnspan=4,padx=10)

        self.treeView=ttk.Treeview(self.treeFrame)
        self.treeView.pack()
        

        self.treeView["columns"]=("one","two","three")

        self.treeView.column("#0")
        self.treeView.column("one")
        self.treeView.column("two")
        self.treeView.column("three")

        self.treeView.heading("#0",text="Rank")
        self.treeView.heading("one",text="Faculty Member")
        self.treeView.heading("two",text="Score")
        self.treeView.heading("three",text="Link")
        
        self.treeView.bind('<Double-Button-1>',self.double_click)

        self.all_departments=["All"]

    def double_click(self, event):
        """
        Notes:
            If in the treeview clicked twice , selenium library will show us to link which link clicked.
        """
        column = self.treeView.identify_column(event.x)
        values_row=self.treeView.item(self.treeView.focus())
        link=values_row["values"][2]
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(link)

    def fetch_profile(self):
        """
        Notes:
            Selenium web driver collect xpaths and we try to parse with BeautifulSoup library.
            We create department combobox olso this function triggers self.collect_information function to collect
            Proffessors data. Moreover, python automatically saves data to database.
        """
        if not self.active_database:
            self.progres_info_lab.config(text="Collecting Faculty Member Links..")
            self.update()
            driver = webdriver.Chrome("chromedriver.exe")
            driver.get("https://www.sehir.edu.tr/en/academics/college-of-engineering-and-natural-sciences/academic-staff")
            time.sleep(1.5)
            try:
                driver.find_element_by_xpath("/html/body/form/div[11]/div/div[8]/div/div/div/div/button").click()
            except :pass
            elem = driver.find_element_by_xpath("//*")
            html_doc = elem.get_attribute("outerHTML")
            self.soup = BeautifulSoup(html_doc, 'html.parser')
            self.procces_soup(self.soup)
            self.all_departments.sort()
            self.departments_combobox.configure(values=self.all_departments)
            self.departments_combobox.current(0)
            self.selected_department=self.departments_combobox.get()
            driver.quit()
            self.collect_informations()
            self.UploaddatabaseSystem()
        else:pass    
    def procces_soup(self,soup_obj):
        """
        Notes:
            This function collect all professors name,  departmand and link Thanks to BeautifulSoup
            It automatically collect informations with a list and thanks to for loop python iterate them.
        
        Returns {dict} - all_users {PROFESSORS_NAME : {DEPARTMENT_:DEPARTMENT , LINK : CORRESPONDING TEACHER LINK.}}
        """
        names=soup_obj.find_all(class_="academic-staff-name")
        departments=soup_obj.find_all(class_="academic-staff-department")
        links=soup_obj.find_all(class_="academic-staff-category-inside")
        members=[b.get("href") for a in links for b in a.find_all("a")]
        for a in range(len(names)):
            name=names[a].text
            department=departments[a].text
            link=members[a]
            if department not in self.all_departments:
                self.all_departments.append(department)
            Professors(name=name,department=department,link=f'{self.university_links}{link}')

    def collect_informations(self):
        """
        Notes:
            In this function if the database available progress bar automatically fully loaded. If not:
            Python automatically identify available persons number and its increases progress bar loading also loading text.
            Besides that, python collect professors information like 
                                        {PROF. AYŞE SOYSAL:['Manhattan','Signal Processing',17/1/2012/]}
        """
        if not self.active_database:
            total=360 # BAR LENGHT!
            progress=30 # WHEN PROFILE LINKS COLLECTED IT WILL MOVE 30
            completed=20 # %20 COMPLETED WHEN LINKS COLLECTED
            comp_total=100-completed # %80 HAVE TO FILL.
            compl_move=comp_total/(len(Professors.all_prof))
            self.progress_bar.create_rectangle(0,0,progress,30,fill="green")
            self.progres_bar_comp.configure(text=(f'{str(completed)}%Completed!'))
            self.update()
            self.progres_info_lab.config(text="Fetching Profiles..")
            self.user_and_keywords={}
            bar_move=(total-progress)/len(Professors.all_prof)
            for user in Professors.all_prof:
                # user_link = user.link
                req = requests.get(user.link,verify=False)
                new_soup=BeautifulSoup(req.content,'html.parser')
                informations=new_soup.find_all(class_="academic-staff-detail-content sub-page-content")
                spl=informations[0].text.split()
                spl=informations[0].text.split()
                new_list=[a.strip(",.") for a in spl]
                user.informations = new_list
                completed+=compl_move
                progress+=bar_move
                self.progres_bar_comp.configure(text=f'{str(round(completed,2))}%Completed!')
                self.progress_bar.create_rectangle(0,0,progress,30,fill="green")
                self.update()
            self.progres_info_lab.configure(text="Database Created!",bg="green")
        else:
            self.progres_info_lab.configure(text="LOADED FULLY!",bg="green")
            for a in range(1,362):
                self.progress_bar.create_rectangle(0,0,a,30,fill="green")
                self.update()
    def department_selected(self,event):
        """
        Notes:
            In this function python identify which department selected. It is important to specify criteria searching.        
        """

        combobox_event=event.widget
        self.selected_department=combobox_event.get()
    
    def eveluate_without_department(self):
        """
        Notes:
            If the department doesnot match with the given criteria(department) python will not append to the new list
        
        Returns - [list] -> Only professors name  Ex. ['ASST. PROF. MEHMET BAYSAN']
        """
        criterias_user=[]
        for user in Professors.all_prof:
            department = user.department
            if self.selected_department == "All":
                criterias_user.append(user)
            elif department == self.selected_department:
                criterias_user.append(user)
        return criterias_user
    def find_persons(self):
        """
        Notes:
            In this function python will try to match user information , if the information match like Given criteria, and searching words;
            For Example : words is california and python will create dictionary like :{Professors:Counter_How_Much_Time_In_Information}
            Python will append it to dictionary and after that python will standardization automatically.
            Max value will be 1.0 others will be rated with the propotion.
            This function also triggers self.add_to_treeView() function to show user ranks, name, score, links.
        """
        given_key=self.keyword_entry.get()
        if len(Professors.all_prof) == 0:
            self.progres_bar_comp.configure(text="Fetch Profile First!",bg="yellow")
            self.original_settings(self.progres_bar_comp)
        elif given_key == "" :
            self.progres_bar_comp.configure(text="Incomplete Info",bg="red")
            self.original_settings(self.progres_bar_comp)
        else:
            new_dictionary={}
            criterias_user=self.eveluate_without_department()
            for user in criterias_user:
                for get_words in user.informations:
                    if given_key.lower() == get_words or given_key.capitalize() == get_words or given_key.upper() == get_words:
                        if user not in new_dictionary:
                            new_dictionary.setdefault(user,1)
                        else:new_dictionary[user]+=1
            if len(new_dictionary) != 0:
                maximum=max(new_dictionary.values())
                maximum=(maximum,1)
                scores={}
                for key,value in new_dictionary.items():
                    current_sc=(value*maximum[1])/maximum[0]
                    scores[key]=round(current_sc,2)
                self.new_score={member:score for member, score in sorted(scores.items(), key=lambda x : x[1],reverse=True)}
                print(self.new_score)
                self.add_to_treeView()
            else:
                self.progres_info_lab.configure(text="NOTHING FOUND!",bg="red")
                self.original_settings(self.progres_info_lab)
                self.clear_treeview()
    def original_settings(self,given_label):
        self.after(1500,lambda: given_label.configure(text="",bg="SystemButtonFace"))
    def add_to_treeView(self):
        """
        Notes:
            In this function python will append trees Profesors Rank,Name,Score,Links automatically.
            Becase we create before dictionary and python will capture data from there.
        """
        self.clear_treeview()
        counter=1
        for member,score in self.new_score.items():
            self.treeView.insert("",counter,text=counter,values=(member,str(score),member.link))
            counter+=1
    def clear_treeview(self):
        """
        Notes:
            If the treeview loaded before this function remove all datas from
            Treeview.
        """
        for i in self.treeView.get_children():
            self.treeView.delete(i)
    def UploaddatabaseSystem(self):
        """
        Notes:
            All the information will uploading to sehir_professors_infos.db
            When the program run again , we don't have to collect all data again.
        """
        database=dbm.open("sehir_professors_infos.db","c")
        database['ProfessorInfo']=pickle.dumps(Professors.all_prof)
        database['Departmans']=pickle.dumps(self.all_departments)
        database.close()
    def DownloadDatabase(self):
        """
        Notes:
            If the python identify database is available it will capture data from sehir_professors_infos.db
            And we don't have to deal with collect data again from websites..
        """
        database=dbm.open("sehir_professors_infos.db","c")
        Professors.all_prof=pickle.loads(database['ProfessorInfo'])
        self.all_departments=pickle.loads(database['Departmans'])
        database.close()
    def check_update_Requirements(self):
        """
        Notes:
            This function carries crucial role. First, python reach every people's link from databases and collect their words again.
            and create dictionary again. e.g {ALI_CAKMAK:[words..]} if the created dictionary doesnot match with the databases dictionary
            Python recognize profiles HAVE TO fetch AGAIN.  If match, databases dictionary will uses.
        Returns:
            [boolean] -- True or False relative the condition
        """
        check_changes = []
        for user in Professors.all_prof:
            req=requests.get(user.link,verify=False)
            new_soup=BeautifulSoup(req.content,'html.parser')
            informations=new_soup.find_all(class_="academic-staff-detail-content sub-page-content")
            spl=informations[0].text.split()
            new_list=[a.strip(",.") for a in spl]
            check_changes.append(user.informations == new_list)
        if all(check_changes):
            return False
        else:
            return True

if __name__ == "__main__":
    root=Tk()
    root.title("Sehir Search Engine")
    run_gui=GraphicalInferface(root)
    root.mainloop()





