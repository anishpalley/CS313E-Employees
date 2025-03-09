"""
Student information for this assignment:

Replace Anish Palley with your name.
On my/our honor, Anish Palley and <FULL NAME>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: ap65675
UT EID 2:
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self._performance = INITIAL_PERFORMANCE
        self._happiness = INITIAL_HAPPINESS
        self._salary = salary
    @property
    def name(self):
        """
        @property for name
        """
        return self.__name
    @property
    def manager(self):
        """
        @property for manager
        """
        return self.__manager
    @property
    def happiness(self):
        """
        @property for happiness
        """
        return self._happiness
    @property
    def performance(self):
        """
        @property for performance
        """
        return self._performance
    @property
    def salary(self):
        """
        @property for salary
        """
        return self._salary
    @happiness.setter
    def happiness(self, value):
        if value < PERCENTAGE_MIN:
            self._happiness = PERCENTAGE_MIN
        elif value > PERCENTAGE_MAX:
            self._happiness = PERCENTAGE_MAX
        else:
            self._happiness = value

    @performance.setter
    def performance(self, value):
        if value < PERCENTAGE_MIN:
            self._performance = PERCENTAGE_MIN
        elif value > PERCENTAGE_MAX:
            self._performance = PERCENTAGE_MAX
        else:
            self._performance = value
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self._salary = value
    @abstractmethod
    def work(self):
        """
        @abstractmethod for work
        """
    def interact(self, other):
        """
        Employee interact method
        """
        if other.name not in self.relationships:
            self.relationships[other.name] = 0
        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness+=1
        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] +=1
        else:
            self.relationships[other.name] -=1
            self.happiness -=1
    def daily_expense(self):
        """
        Employee daily expense method
        """
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE
    def __str__(self):
        returned = ""
        returned += self.name + '\n' + '\t'
        returned += "Salary: $"+str(self.salary)+'\n'+ '\t'
        returned += "Savings: $"+str(self.savings)+"\n"+ '\t'
        returned += "Happiness: "+str(self.happiness)+"%"+"\n"+ '\t'
        returned += "Performance: "+str(self.performance)+"%"
        return returned

class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def work(self):
        num = random.randint(-5,5)
        self._performance = self._performance + num
        if num <= 0:
            self._happiness -=1
            for employee in self.relationships:
                self.relationships[employee] -= 1
        else:
            self._happiness +=1
class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """
    def work(self):
        num = random.randint(-15,15)
        self.performance += num
        if num<=0:
            self.happiness-=2
        else:
            self.happiness+=1
    def interact(self,other):
        super().interact(other)
        if self.manager == other:
            if other.happiness>HAPPINESS_THRESHOLD:
                if self.performance>=TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                    self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary = self.salary//2
                self.happiness -= 5
                if self.salary <= 0:
                    self.is_employed = False




class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """
    def work(self):
        num = random.randint(-10,10)
        self.performance += num
        if num >= 0:
            self.happiness+=1
    def interact(self,other):
        super().interact(other)
        if self.manager == other:
            if other.happiness > HAPPINESS_THRESHOLD:
                if self.performance >= PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                    self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness-=1
