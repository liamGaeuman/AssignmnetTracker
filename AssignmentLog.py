"""
Author: LIam Gaeuman
Date: 12/11/20
This is my python final project.
It is an assignment tracker that can do many cool things.
"""
from breezypythongui import EasyFrame
import pandas as pd
import pickle

class AssignmentWindow(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "Liam's Assignment log and tracker")

        self.assignments = {"|name|": [], "|due date|": [], "|difficulty|": [], "|class|": [], "|status|":[]}
        
        self.addLabel(row = 0, column = 0, text = "Assignment name")
        self.addLabel(row = 0, column = 1, text = "Assignment due date")
        self.addLabel(row = 0, column = 2, text = "Assignment difficulty")
        self.addLabel(row = 0, column = 3, text = "class name")
        self.addLabel(row = 0, column = 4, text = "status")
        
        self.assName = self.addTextField("assignment", 1, 0)
        self.assDate = self.addTextField("xx/xx/xxxx", 1, 1)
        self.assDificulty = self.addTextField("1-10", 1, 2)
        self.assClass = self.addTextField("class name", 1, 3)
        self.assComplete = self.addCheckbutton("complete", 1, 4)

        self.addButton(text = "enter assignment", row = 2, column = 0, command = self.createAssignment)
        self.addButton(text = "edit assignment", row = 2, column = 1, command = self.editAssignment)
        self.addButton(text = "remove assignment", row = 2, column = 2, command = self.removeAssignment)
        self.addButton(text = "save changes", row = 2, column = 3, command = self.pickleIT)
        self.addButton(text = "print selected", row = 2, column = 4, command=  self.printSelected)

        self.outputArea = self.addTextArea("", row = 3, column = 0, columnspan = 5, width = 80, height = 15)

        self.addButton(text = "show all", row = 4, column = 0, command  = self.showAll)
        self.addButton(text = "Filter", row = 5, column = 0, command  = self.filterIT)
        self.filterDate = self.addCheckbutton("due date", 4, 1)
        self.filterDifficulty = self.addCheckbutton("difficulty", 4, 2)
        self.filterClass = self.addCheckbutton("class", 4, 3)
        self.filterStatus = self.addCheckbutton("status", 4, 4)

        self.filterDateField = self.addTextField("", 5, 1)
        self.filterDifficultyField = self.addTextField("", 5, 2)
        self.filterClassField = self.addTextField("", 5, 3)
        self.filterStatusField = self.addTextField("", 5, 4)
        
        #this is my try and except
        
        try:
            self.unPickle()
        except FileNotFoundError:
            print("It is okay")
            
        self.showAll()
        self.message = ""
        self.messageTitle = ""
        self.selected = ""
        self.editing = False
        self.removing = False
        
    def showMessage(self):
        """Displays message based on global variables that are contantly being changed before the method is called"""
        self.messageBox(title = self.messageTitle, message = self.message)

    def pickleIT(self):
        """This method pickles the dataframe. It does not pickle the pandas dataframe but only the dictionary"""
        pickle_out = open("assignments.pickle","wb")
        pickle.dump(self.assignments, pickle_out)
        pickle_out.close()
        self.messageTitle = "success"
        self.message = "You have saved changes"
        self.showMessage()
        

    def unPickle(self):
        """This method opens the pickled file"""
        pickle_in = open("assignments.pickle", "rb")
        self.assignments = pickle.load(pickle_in)
        pickle_in.close()

    
    def createAssignment(self):
        """This method create an assignemnt. It first checks for conditions"""
        if self.assName.getText() == "assignment" or self.assName.getText() == "":
            self.message = "invalid assignment name given!"
            self.messageTitle = "Be more careful!"
            self.showMessage()
            return

        elif self.checkName() == True:
            self.message = "That name already exits! You can edit it though."
            self.messageTitle = "Be more careful!"
            self.showMessage()
            return
        
        else:
            name = self.assName.getText()
            
        if self.assDate.getText() == "xx/xx/xxxx" or self.assDate.getText() == "":
            dueDate = "N/A"
        else:
            dueDate = self.assDate.getText()
        
        if self.assDificulty.getText() == "1-10" or self.assDificulty.getText() == "":
            difficulty = "N/A"
        else:
            difficulty = self.assDificulty.getText()

        if self.assClass.getText() == "class name" or self.assClass.getText() == "":
            schoolClass = "N/A"
        else:
            schoolClass = self.assClass.getText()
            
        if self.assComplete.isChecked():
            status = "complete"
        else:
            status = "incomplete"
            
        self.assignments["|name|"].append(name)
        self.assignments["|due date|"].append(dueDate)
        self.assignments["|difficulty|"].append(difficulty)
        self.assignments["|class|"].append(schoolClass)
        self.assignments["|status|"].append(status)
        

    def printSelected(self):
        """This method prints whatever is displayed on the text area"""
        file = open("assignment" + str(self.selected) + ".txt", 'w')
        file.write(self.outputArea.getText())
        self.messageTitle = "success"
        self.message = "You have printed to assignment" + str(self.selected) + ".txt"
        self.showMessage()
        
              
    def showAll(self):
        """This displays the pandas dataframe on the textarea"""
        df = pd.DataFrame(self.assignments)
        self.outputArea.setText(df)

    
    def filterIT(self):
        """This method filters the assignmetns usuing pandas filtering methods"""
        
        df = pd.DataFrame(self.assignments)
        MiniList = []

        #This is where I applied something we have not learned in class. This is filtering with pandas
        
        if self.filterDate.isChecked():
            A = df['|due date|'] == str(self.filterDateField.getText()) 
            MiniList.append(A)
        if self.filterDifficulty.isChecked():
            B = df['|difficulty|'] == str(self.filterDifficultyField.getText())
            MiniList.append(B)
        if self.filterClass.isChecked():
            C = df['|class|'] == str(self.filterClassField.getText())
            MiniList.append(C)
        if self.filterStatus.isChecked():
            D = df['|status|'] == str(self.filterStatusField.getText())
            MiniList.append(D)

        if len(MiniList) == 1:
            filt = MiniList[0]
        elif len(MiniList) == 2:
            filt = MiniList[0] & MiniList[1]
        elif len(MiniList) == 3:
            filt = MiniList[0] & MiniList[1] & MiniList[2]
        elif len(MiniList) == 4:
            filt = A & B & C & D
        else:
            self.messageTitle = "Hey!"
            self.message = "You have not checked any of the filter boxes!"
            self.showMessage()
            return
        
        self.outputArea.setText(df.loc[filt])


    def checkName(self):
        """This method checks to see if the name exits already"""
        for i in self.assignments["|name|"]:
            if self.assName.getText() == i:
                return True

        
    def editAssignment(self):
        """This method prepares an assignment for editing"""
        if self.editing == True:
            self.edit()
            return
        if self.assName.getText() == "assignment" or self.assName.getText() == "":
            self.message = "invalid assignment name given!"
            self.messageTitle = "BOI!"
            self.showMessage()
            return
        count = 0
        for i in self.assignments["|name|"]:
            if self.assName.getText() != i:
                count += 1
        if count == len(self.assignments["|name|"]):
            self.messageTitle = "Error!"
            self.message = "That Assignemnt does not exist yet."
            self.showMessage()
            return
        else:
            self.messageTitle = "Okay"
            self.message = "The details will be pulled up. Make the desired changes and press edit assignemnt again to submit"
            self.showMessage()
            self.editing = True

            df = pd.DataFrame(self.assignments)

            self.assignment_name = self.assName.getText()
            
            name = (df['|name|'] == str(self.assName.getText()))

            self.outputArea.setText(df.loc[name])
            

    def edit(self):
        """This method edits the assignment"""
        # use a loop to find the names index, then pop the index of that list every positon and replace it
        index_count = 0
        for name in self.assignments["|name|"]:
            if name == self.assignment_name:
                break
            else:
                index_count += 1
        self.assignments["|name|"].pop(index_count)
        self.assignments["|due date|"].pop(index_count)
        self.assignments["|difficulty|"].pop(index_count)
        self.assignments["|class|"].pop(index_count)
        self.assignments["|status|"].pop(index_count)
        self.assignments["|name|"].insert(index_count, self.assName.getText())
        self.assignments["|due date|"].insert(index_count, self.assDate.getText())
        self.assignments["|difficulty|"].insert(index_count, self.assDificulty.getText())
        self.assignments["|class|"].insert(index_count, self.assClass.getText())
        if self.assComplete.isChecked():
            status = "complete"
        else:
            status = "incomplete"
        self.assignments["|status|"].insert(index_count, status)
        self.editing = False
        self.messageTitle = "success"
        self.message = "you have editied the assignment: " + str(self.assName.getText()) + "."
        self.showMessage()
        
    
    def removeAssignment(self):
        """This methods prepares an assignment for removal"""
        if self.removing == True:
            self.remove()
            return
        # use a loop to find the names index, then pop the index of that list every positon.
        #for name in self.assignments["|name|"]
        self.messageTitle = "okay"
        self.message = "select the assignment you want to delete then press remove assignment again"
        self.showMessage()
        self.removing = True

    def remove(self):
        """This method removes an assignment"""
        if self.assName.getText() == "assignment" or self.assName.getText() == "":
            self.message = "invalid assignment name given!"
            self.messageTitle = "BOI!"
            self.showMessage()
            return
        count = 0
        for i in self.assignments["|name|"]:
            if self.assName.getText() != i:
                count += 1
        if count == len(self.assignments["|name|"]):
            self.messageTitle = "Error!"
            self.message = "That Assignemnt does not exist yet."
            self.showMessage()
            return
        index_count = 0
        for name in self.assignments["|name|"]:
            if name == self.assName.getText():
                break
            else:
                index_count += 1
        self.assignments["|name|"].pop(index_count)
        self.assignments["|due date|"].pop(index_count)
        self.assignments["|difficulty|"].pop(index_count)
        self.assignments["|class|"].pop(index_count)
        self.assignments["|status|"].pop(index_count)
        self.messageTitle = "success"
        self.message = "you have deleted " + str(self.assName.getText())
        self.showMessage()
        self.removing = False
        
def main():
    AssignmentWindow().mainloop()

if __name__ == '__main__':
    main()

