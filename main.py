import customtkinter as ctk
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import filedialog

from tools.pricing import growth_chart, download

ctk.set_appearance_mode("Light") # Modes: "Light", "Dark", "System"
ctk.set_default_color_theme("dark-blue") # Themes: "blue", "green", "dark-blue"

class GrowthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Growth Chart")
        self.geometry("1600x900")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=400)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        ## Title
        self.title_label = ctk.CTkLabel(self.sidebar, text="Investment Visualization", font=("Arial", 30, "bold"))
        self.title_label.pack(padx=50, pady=25)

        # Tickers Label
        self.ticker_label = ctk.CTkLabel(self.sidebar, text="Enter Tickers Below:", font = ("Arial", 16))
        self.ticker_label.pack(pady=10)

        ## Frame for ticker entries
        ticker_frame = ctk.CTkFrame(self.sidebar)
        ticker_frame.pack(pady=10)
        self.scroll_frame_entries = [ctk.CTkEntry(ticker_frame, width=150) for _ in range(10)]
        for i, entry in enumerate(self.scroll_frame_entries):
            entry.grid(row=i//2, column=i%2, padx=10, pady=5)

        ## Interval
        self.interval_frame = ctk.CTkFrame(self.sidebar)
        self.interval_frame.pack(pady=20)
        self.interval_label = ctk.CTkLabel(self.interval_frame, text="Interval: ", font=("Arial", 16))
        self.interval_label.grid(row=0, column=0, padx=10)
        self.interval_select = ctk.CTkOptionMenu(self.interval_frame, values=["Daily", "Monthly", "Quarterly"], state="readonly")
        self.interval_select.grid(row=0, column=1)
        
        ## Frame for dates
        self.start_frame = ctk.CTkFrame(self.sidebar)
        self.start_frame.pack()

        ## Start and end labels
        self.start_label = ctk.CTkLabel(self.start_frame, text="Start", font = ("Arial", 16))
        self.start_label.grid(row=0, column=1)
        self.end_label = ctk.CTkLabel(self.start_frame, text="End", font = ("Arial", 16))
        self.end_label.grid(row=0, column=2)

        days = []
        for d in range(1,32):
            days.append(str(d))
        self.day_label = ctk.CTkLabel(self.start_frame, text="Day:", font=("Arial", 16))
        self.day_label.grid(row=1, column=0, padx=10, pady=2.5)
        self.day_entry = ctk.CTkOptionMenu(self.start_frame, values=days)
        self.day_entry.grid(row=1, column=1)
        self.end_day = ctk.CTkOptionMenu(self.start_frame, values=days)
        self.end_day.set(str(datetime.now().day))
        self.end_day.grid(row=1, column=2, padx=10)

        months = []
        for m in range(1, 13):
            months.append(str(m))
        self.month_label = ctk.CTkLabel(self.start_frame, text="Month:", font=("Arial", 16))
        self.month_label.grid(row=2, column=0, padx=10, pady=2.5)
        self.month_entry = ctk.CTkOptionMenu(self.start_frame, values=months)
        self.month_entry.grid(row=2, column=1)
        self.end_month = ctk.CTkOptionMenu(self.start_frame, values=months)
        self.end_month.set(str(datetime.now().month))
        self.end_month.grid(row=2, column=2)

        years = []
        for y in range(1970, 2026):
            years.append(str(y))
        self.year_label = ctk.CTkLabel(self.start_frame, text="Year:", font=("Arial", 16))
        self.year_label.grid(row=3, column=0, padx=10, pady=2.5)
        self.year_entry = ctk.CTkOptionMenu(self.start_frame, values=years)
        self.year_entry.grid(row=3, column=1)
        self.year_entry.set("2024")
        self.end_year = ctk.CTkOptionMenu(self.start_frame, values=years)
        self.end_year.set(str(datetime.now().year))
        self.end_year.grid(row=3, column=2) 

        ## Growth chart button
        self.growth_button = ctk.CTkButton(self.sidebar, text="Growth Chart", font=("Arial", 16), command=self.run_growth)
        self.growth_button.pack(pady=30)

        ## Download button
        self.download_button = ctk.CTkButton(self.sidebar, text="Download Data", font=("Arial", 16), command=self.run_download)
        self.download_button.pack(pady=15)

        ## Appearance Mode and color
        self.appearance_frame = ctk.CTkFrame(self.sidebar)
        self.appearance_frame.pack(side="bottom", pady=10)

        self.appearance_label = ctk.CTkLabel(self.appearance_frame, text="Appearance", font=("Arial", 16))
        self.appearance_label.grid(row=0, column=0, padx=10, pady=5)
        self.appearance_mode = ctk.CTkOptionMenu(self.appearance_frame, values=["Light", "Dark", "System"], font=("Arial", 16), command=self.change_appearance_mode_event)
        self.appearance_mode.grid(row=0, column=1, padx=10)

        # Description
        self.description_frame = ctk.CTkFrame(self)
        self.description_frame.grid(row=0, column=1, sticky="nsew", padx=20)

        self.description1 = ctk.CTkLabel(self.description_frame, font=("Arial", 20), text="Create a growth chart using the information on the left!")
        self.description1.pack(pady=10)
        self.description2 = ctk.CTkLabel(self.description_frame, font=("Arial", 16), text="The chart below provides a visual for the cumulative return of your specific investments.")
        self.description2.pack(pady=10)

        # Chart
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)


    def run_growth(self):
        # Get tickers
        tickers = [entry.get().upper() for entry in self.scroll_frame_entries]
        for i in reversed(tickers):
            if i == "":
                tickers.remove(i)

        # Get interval
        interval = self.interval_select.get()

        # Get time frame
        day = self.day_entry.get()
        month = self.month_entry.get()
        year = self.year_entry.get()
        day2 = self.end_day.get()
        month2 = self.end_month.get()
        year2 = self.end_year.get()

        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
          widget.destroy()
        
        # Create and place the chart
        fig = growth_chart(tickers, day, month, year, day2, month2, year2, interval)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)

    def run_download(self):
        # Get tickers
        tickers = [entry.get().upper() for entry in self.scroll_frame_entries]
        for i in reversed(tickers):
            if i == "":
                tickers.remove(i)

        # Get interval
        interval = self.interval_select.get()

        # Get time frame
        day = self.day_entry.get()
        month = self.month_entry.get()
        year = self.year_entry.get()
        day2 = self.end_day.get()
        month2 = self.end_month.get()
        year2 = self.end_year.get()

        # Download data frame
        info = download(tickers, day, month, year, day2, month2, year2, interval)

        # Ask for filepath
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save as")

        # Convert to csv
        info.to_csv(file_path, index=False)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = GrowthApp()
    app.mainloop()