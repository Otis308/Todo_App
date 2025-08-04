from datetime import datetime

class task:
    def __init__(self, id, title, description, created_at, due_date, status, owner):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__created_at = created_at
        self.__due_date = due_date
        self.__status = status
        self.__owner = owner

    def get_id(self):
        return self.__id
    def set_id(self, value):
        if (value >=  0):
            self.__id = value
        else: 
            print("Error!")
    def __repr__(self):
        return f"<Task {self.get_id()}: {self.__title} - {'Done' if self.__completed else 'Pending'}>"
    
    def get_title(self):
        return self.__title
    def set_title(self, value):
        self.__title = value
    
    def get_decription(self):
        return self.__description
    def set_decription(self, value):
        self.__description = value
    
    def get_create_at(self):
        return self.__created_at
    def set_create_at(self, value):
        self.__created_at = value
    
    def get_due_date(self):
        return self.__due_date
    def set_due_date(self, value):
        self.__due_date = value
    
    def get_status(self):
        return self.__status
    def set_status(self, value):
        self.__status = value
    
    def get_own(self):
        return self.__owner
    def set_own(self, value):
        self.__owner = value

    def input_info(self):
        self.__title       = input("Enter task title: ") 
        self.__description = input("Enter task description: ") 
        self.__due_date    = input("Enter due date (YYYY-MM-DD): ")
        self.__status      = input("Enter task status (Done, Wip, Pen): ")
        self.__owner       = input("Enter task owner: ") 
    
    def show_info(self):
        print(f"*** TASK {self.__id} ***")
        print(f"Title: {self.__title}")
        print(f"Description: {self.__description}")
        self.__created_at = datetime.now()
        print(f"Creation date: {self.__created_at}")
        print(f"Due date: {self.__due_date}")
        print(f"Status: {self.__status}")
        print(f"Owner: {self.__owner}")


    