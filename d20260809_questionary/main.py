import questionary

selected = questionary.select(
    "test select?",
    choices=[
        "option 1",
        "option 2",
        "option 3",
    ],
).ask()

print(f"You selected: {selected}")

selected_checkbox = questionary.checkbox(
    "test checkbox?",
    choices=[
        "option 1",
        "option 2",
        "option 3",
    ],
).ask()

print(f"You selected: {selected_checkbox}")

answer_text = questionary.text("What is your name?").ask()

print(f"Hello, {answer_text}!")

answer_confirm = questionary.confirm("Do you want to continue?").ask()

print(f"You answered: {answer_confirm}")
