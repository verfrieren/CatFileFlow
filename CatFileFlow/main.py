from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog, messagebox

from organizer import organize_folder


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CatFileFlowApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CatFileFlow - Catomatic File Organizer")
        self.geometry("850x650")
        self.minsize(700, 550)

        self.selected_folder = None

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="𑄝੭ CatFileFlow",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="automatic file organizer"
        )
        subtitle.pack(pady=5)

        self.folder_button = ctk.CTkButton(
            self,
            text="Choose Folder",
            command=self.choose_folder
        )
        self.folder_button.pack(pady=15)

        self.folder_label = ctk.CTkLabel(
            self,
            text="No folder selected"
        )
        self.folder_label.pack(pady=5)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=15)

        preview_button = ctk.CTkButton(
            buttons,
            text="Preview Sorting",
            command=self.preview
        )
        preview_button.pack(side="left", padx=5)

        sort_button = ctk.CTkButton(
            buttons,
            text="Start Sorting",
            command=self.sort
        )
        sort_button.pack(side="left", padx=5)

        self.results = ctk.CTkTextbox(
            self,
            width=750,
            height=350
        )
        self.results.pack(padx=20, pady=15, fill="both", expand=True)

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            text_color="green"
        )
        self.status_label.pack(pady=5)

    def choose_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=folder)

            self.results.delete("1.0", "end")

            self.status_label.configure(
                text="Folder selected",
                text_color="green"
            )

    def preview(self):

        if not self.selected_folder:
            messagebox.showwarning(
                "No folder selected",
                "Please select a folder first!"
            )
            return

        try:
            files = organize_folder(
                self.selected_folder,
                dry_run=True
            )

            self.show_results(files, "Preview complete")

        except (OSError, ValueError) as error:
            messagebox.showerror("Error", str(error))

    def sort(self):

        if not self.selected_folder:
            messagebox.showwarning(
                "No folder selected",
                "Please select a folder first!"
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Sorting",
            "Are you sure you want to move the files?"
        )

        if not confirmation:
            return

        try:
            files = organize_folder(
                self.selected_folder,
                dry_run=False
            )

            self.show_results(files, "Sorting complete")

        except (OSError, ValueError) as error:
            messagebox.showerror("Error", str(error))

    def show_results(self, files, status):

        self.results.delete("1.0", "end")

        if not files:
            self.results.insert(
                "end",
                "No files to organize in this folder.\n"
            )

        for file in files:

            destination = Path(file["destination"])

            try:
                target = destination.relative_to(self.selected_folder)
            except ValueError:
                target = destination

            self.results.insert(
                "end",
                f"{file['name']} -> {target} "
                f"[{file['status']}]\n"
            )

        errors = sum(
            1 for file in files
            if file["status"].startswith("Error")
        )

        if errors:
            self.status_label.configure(
                text=f"{status}! {len(files)} files, {errors} errors.",
                text_color="red"
            )
        else:
            self.status_label.configure(
                text=f"{status}! {len(files)} files processed.",
                text_color="green"
            )


if __name__ == "__main__":

    app = CatFileFlowApp()
    app.mainloop()
