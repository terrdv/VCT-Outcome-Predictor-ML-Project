from tkinter import *
import customtkinter
import pandas as pd
from PIL import Image, ImageTk
from model.predictor import finalpred_rfc, finalpred_logreg, getdf
from plots import pie, barplot
customtkinter.set_appearance_mode("dark")  # Modes: "system" (default), "dark", "light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (default

selectedTeams = []
app = customtkinter.CTk()
teammap = pd.read_csv('vct_2025/matches/team_mapping.csv')

app.title("VCT Prediction App")
app.geometry("1280x720")
app.iconbitmap("greenblue.ico")

# Configure main window for responsive layout
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=3)  # Main content area
app.grid_columnconfigure(1, weight=0)  # Button scroll area

# Main content frame
main_frame = customtkinter.CTkFrame(app, fg_color="transparent")
main_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=20)
main_frame.grid_rowconfigure(3, weight=1)  # Plots area
main_frame.grid_columnconfigure(0, weight=1)

# Button scroll frame
buttonscroll = customtkinter.CTkScrollableFrame(app, width=480, height=720)
buttonscroll.grid(row=0, column=1, sticky="nsw", padx=(10, 20), pady=20)

for col in range(3):
    buttonscroll.grid_columnconfigure(col, weight=1)

# Main content widgets
label = customtkinter.CTkLabel(main_frame, text="Select Teams", font=("Arial", 24))
label.grid(row=0, column=0, pady=(0, 20), padx=20, sticky="ew")

predict_button = customtkinter.CTkButton(main_frame, text="Predict \n TeamA vs TeamB", command=lambda: pred_button(), width=200, height=50, state="disabled")
predict_button.grid(row=1, column=0, pady=30, padx=20)

rfcpred_label = customtkinter.CTkLabel(main_frame, text="", font=("Arial", 16))
rfcpred_label.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

logreg_pred_label = customtkinter.CTkLabel(main_frame, text="", font=("Arial", 16))
logreg_pred_label.grid(row=2, column=0, pady=(50, 10), padx=20, sticky="ew")

# Plot frame
plot_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
plot_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=0,)
plot_frame.grid_rowconfigure(0, weight=1)
plot_frame.grid_columnconfigure(0, weight=1)
plot_frame.grid_columnconfigure(1, weight=1)

plot1 = customtkinter.CTkLabel(plot_frame, text="", font=("Arial", 12), compound="top", anchor="w")
plot2 = customtkinter.CTkLabel(plot_frame, text="", font=("Arial", 12), compound="top", anchor="e")

def open_plot(plot, plott):
    current_plot1 = customtkinter.CTkImage(light_image=plot, dark_image=plot, size=plot.size)
    current_plot2 = customtkinter.CTkImage(light_image=plott, dark_image=plott, size=plott.size)

    plot1.configure(image=current_plot1, font=("Arial", 12))
    plot1.grid(row=0, column=0, pady=20, padx=(10, 10), sticky="nsew")
    plot2.configure(image=current_plot2, font=("Arial", 12))
    plot2.grid(row=0, column=1, pady=20, padx=(10, 10), sticky="nsew")

def select_teams(name):
    if name not in selectedTeams and len(selectedTeams) < 2:
        selectedTeams.append(name)
        if len(selectedTeams) == 1:
            predict_button.configure(text=f"Predict \n {selectedTeams[0]} vs TeamB")
        else:
            predict_button.configure(text=f"Predict \n {selectedTeams[0]} vs {selectedTeams[1]}")
            predict_button.configure(state="normal")
        print(f"Selected Teams: {selectedTeams}")

def pred_button():
    rfcpred = finalpred_rfc(selectedTeams[0], selectedTeams[1])
    rfcpred_label.configure(text=rfcpred, font=("Arial", 16))
    logreg_pred = finalpred_logreg(selectedTeams[0], selectedTeams[1])
    logreg_pred_label.configure(text=logreg_pred, font=("Arial", 16))
    predict_button.configure(text="Reset Prediction", command=reset_pred, state="normal")
    label.configure(text="Predicted Match Outcome", font=("Arial", 24))
    #make pie chart
    open_plot(pie(selectedTeams[0], selectedTeams[1], getdf(selectedTeams[0], selectedTeams[1])),
              barplot(selectedTeams[0], selectedTeams[1], getdf(selectedTeams[0], selectedTeams[1])))

def reset_pred():
    global selectedTeams, logreg_pred_label, rfcpred_label
    rfcpred_label.configure(text="", font=("Arial", 16))
    logreg_pred_label.configure(text="", font=("Arial", 16))
    selectedTeams = []
    predict_button.configure(text="Predict \n TeamA vs TeamB", state="disabled")
    predict_button.configure(command=pred_button)
    label.configure(text="Select Teams", font=("Arial", 24))
    
    plot1.grid_forget()
    plot2.grid_forget()

for i in range (len(teammap)):
    team_name = teammap.iloc[i]['Full Name']
    team_button = customtkinter.CTkButton(buttonscroll, text=team_name, command=lambda t=teammap.iloc[i]['Abbreviated']: select_teams(t))
    team_button.grid(row=i // 3, column=i % 3, padx=10, pady=10)

app.mainloop()



