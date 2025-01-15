
# def initializeGUI():
#     root = tk.Tk()
#     root.title("Voice Assistant")
#     root.geometry("400x300")

#     title = tk.Label(root, text="Voice Assistant", font=("Helvetica", 16))
#     title.pack(pady=20)

#     status_label = tk.Label(root, text="Listening...", font=("Helvetica", 12))
#     status_label.pack(pady=10)

#     def startListening():
#         threading.Thread(target=continuousListening, daemon=True).start()

#     start_button = tk.Button(root, text="Start Listening", command=startListening, font=("Helvetica", 14))
#     start_button.pack(pady=10)

#     # Exit button
#     exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 14))
#     exit_button.pack(pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     initializeGUI()