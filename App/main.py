from Feature_Engineering import Features
from Preprocessing import preprocess
from Model import model
import tkinter as tk
from tkinter import scrolledtext
from io import StringIO
import sys

import warnings
warnings.filterwarnings('ignore')
from Logger import setup_logging



import tkinter as tk
from tkinter import ttk

class ATMInputUI:
    def __init__(self, root , models):
        self.root = root
        self.root.title("ATM Transaction Input")

        # Define input fields
        self.create_input("IsHoliday", "boolean", row=0)
        self.create_input("Year", "dropdown", row=1, options=[2020, 2021, 2022, 2023, 2024])
        self.create_input("Month", "dropdown", row=2, options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.create_input("Date", "dropdown", row=3, options=list(range(1, 31)))
        self.create_input("DayOfWeek", "dropdown", row=4, options=list(range(1, 8)))
        self.create_input("IsWeekend", "boolean", row=5)
        self.create_input("Quarter", "dropdown", row=6, options=[1, 2, 3, 4])
        self.create_input("DayOfYear", "dropdown", row=7, options=list(range(1, 366)))
        self.create_input("PartOfMonth", "dropdown", row=8, options=[1, 2, 3])
        self.create_input("Last7Days_mean", "entry", row=9)
        self.create_input("Last30Days_mean", "entry", row=10)
        self.create_input("Difference", "entry", row=11)
        self.create_input("HolidayType", "dropdown", row=12, options=['None','Kashmir Day', 'Pakistan Day', 'Labour Day', 'Eid-ul-Fitr Day 1', 'Eid-ul-Fitr Day 2', 'Eid-ul-Fitr Day 3',
            'Eid al-Adha Day 1', 'Eid al-Adha Day 2', 'Eid al-Adha Day 3', 'Independence Day', 'Ashura', 'Eid Milad un-Nabi',
            'Iqbal Day', 'Christmas Day', 'Quaid-e-Azam Day'
        ])
        self.create_input("Event", "dropdown", row=13, options=['None' , 'Ramzan', 'Hajj', 'Muharram'])
        self.create_input("Paydays", "boolean", row=14)
        self.create_input("HolidaySequence", "entry", row=15, placeholder="WHHW")

        # Submit button
        self.model = models
        submit_button = ttk.Button(self.root, text="Submit", command=self.submit)
        submit_button.grid(row=16, column=1, pady=10)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=17, column=0, columnspan=2, pady=10)

    def create_input(self, label, input_type, row, options=None, placeholder=None):
        ttk.Label(self.root, text=label).grid(row=row, column=0, padx=10, pady=5, sticky='w')

        if input_type == "boolean":
            var = tk.BooleanVar()
            checkbutton = ttk.Checkbutton(self.root, variable=var)
            checkbutton.grid(row=row, column=1, padx=10, pady=5)
            setattr(self, f"{label.lower()}_var", var)
        elif input_type == "dropdown" and options:
            var = tk.StringVar()
            combobox = ttk.Combobox(self.root, textvariable=var, values=options)
            combobox.grid(row=row, column=1, padx=10, pady=5)
            setattr(self, f"{label.lower()}_var", var)
        elif input_type == "entry":
            entry = ttk.Entry(self.root)
            entry.grid(row=row, column=1, padx=10, pady=5)
            if placeholder:
                entry.insert(0, placeholder)
            setattr(self, f"{label.lower()}_var", entry)

    def submit(self):
        # Collect all values
        values = {
            "IsHoliday": self.isholiday_var.get(),
            "Year": self.year_var.get(),
            "Month": self.month_var.get(),
            "Date": self.date_var.get(),
            "DayOfWeek": self.dayofweek_var.get(),
            "IsWeekend": self.isweekend_var.get(),
            "Quarter": self.quarter_var.get(),
            "DayOfYear": self.dayofyear_var.get(),
            "PartOfMonth": self.partofmonth_var.get(),
            "Last7Days_mean": self.last7days_mean_var.get(),
            "Last30Days_mean": self.last30days_mean_var.get(),
            "Difference": self.difference_var.get(),
            "HolidayType": self.holidaytype_var.get(),
            "Event": self.event_var.get(),
            "Paydays": self.paydays_var.get(),
            "HolidaySequence": self.holidaysequence_var.get(),
        }

        result = self.model.infer(values)
       
        models = ['Grad Boost', 'LightGBM', 'CatBoost', 'XGBoost', 'Random Forest', 'Stacked Regressor']

        formatted_results = ""
        for model_name, model_result in zip(models, result):
            formatted_results += f'{model_name:<15}: {model_result}\n'
        print(formatted_results)

        self.result_label.config(text=formatted_results)
        
if __name__ == "__main__":
    logger = setup_logging('Forecast.log')
    ft = Features(Dataset_path=r"C:\Users\Shaikh Abdul Rafay\Desktop\cashInfo-1006.json" ,
              USD_Dataset_path= r"C:\Users\Shaikh Abdul Rafay\Downloads\USD_PKR Historical Data.csv", 
              info= False)
    pre = preprocess(ft.df)
    models = model(pre.splits)

    root = tk.Tk()
    app = ATMInputUI(root , models)

    root.mainloop()
