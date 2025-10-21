import random
import os
import time
from PIL import Image

elements = {
    "Sb": "antymon",
    "As": "arsen",
    "N": "azot",
    "Ba": "bar",
    "Bi": "bizmut",
    "Br": "brom",
    "Cl": "chlor",
    "Cr": "chrom",
    "Hg": "cyna",
    "Zn": "cynk",
    "P": "fosfor (bialy)",
    "Al": "glin",
    "I": "jod",
    "Si": "krzem",
    "Mg": "magnez",
    "Mn": "mangan",
    "Cu": "miedz",
    "Ni": "nikiel",
    "Pb": "olow",
    "K": "potas",
    "Hg": "rtec",
    "S": "siarka",
    "Na": "sod",
    "Ag": "srebro",
    "O": "tlen",
    "Ca": "wapn",
    "C": "wegiel",
    "H": "wodor",
    "Fe": "zelazo"
}

pictures_folder = "pictures"

def show_image(symbol):
    path = os.path.join(pictures_folder, f"{symbol}.png")
    if os.path.exists(path):
        img = Image.open(path)
        img.show()
    else:
        print(f"Obrazek dla {symbol} nie znaleziony.")

def is_correct_answer(user_answer, correct_symbol, correct_name):
    user_answer = user_answer.lower().strip()

    # Reject single-letter answers if symbol is more than one letter
    if len(user_answer) == 1 and len(correct_symbol) > 1:
        return False

    # Accept "fosfor" for "fosfor (bialy)"
    accepted_names = [correct_name.lower()]
    if correct_name == "fosfor (bialy)":
        accepted_names.append("fosfor")

    # Accept correct symbol
    accepted_symbols = [correct_symbol.lower()]

    def simple_typo_check(ans, correct):
        if ans == correct:
            return True
        if abs(len(ans) - len(correct)) > 1:
            return False
        mismatch = sum(1 for a, b in zip(ans, correct) if a != b) + abs(len(ans) - len(correct))
        return mismatch <= 1

    for sym in accepted_symbols:
        if simple_typo_check(user_answer, sym):
            return True
    for name in accepted_names:
        if simple_typo_check(user_answer, name):
            return True
    return False

def timestamp_filename(filename):
    import datetime
    base, ext = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}{ext}"

def quiz():
    repetition_file = "for_repeating.txt"
    repeat_mode = False
    repeat_questions = []
    if os.path.exists(repetition_file):
        resp = input("Czy powtórzyć błędne pytania z poprzedniej sesji? (t/n): ").strip().lower()
        if resp == 't':
            repeat_mode = True
            with open(repetition_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            repeat_questions = [tuple(line.strip().split("::")) for line in lines if "::" in line]
            # Rename the old repeat file so it won't be detected again
            new_name = timestamp_filename(repetition_file)
            os.rename(repetition_file, new_name)

    use_images = input("Czy chcesz quiz z obrazkami? (t/n): ").strip().lower() == 't'

    question_limit = 0
    while True:
        qlim = input("Ile pytań chcesz? (0 dla nieograniczonej liczby): ").strip()
        try:
            question_limit = int(qlim)
            if question_limit >= 0:
                break
        except ValueError:
            pass
        print("Podaj 0 lub liczbę całkowitą większą lub równą zero.")

    correct = 0
    mistakes = 0
    wrong_questions = []

    if repeat_mode:
        question_pool = repeat_questions
    else:
        question_pool = list(elements.items())

    asked_count = 0

    print("\nQuiz uruchomiony.")
    if question_limit == 0:
        print("Naciśnij Enter, aby kontynuować lub 'C' aby zakończyć i zobaczyć wyniki.\n")
    else:
        print(f"Quiz ograniczony do {question_limit} pytań.\n")

    while True:
        if not question_pool:
            print("Brak pytań do powtórki. Kończę quiz.")
            break
        if question_limit > 0 and asked_count >= question_limit:
            print(f"Osiągnięto limit {question_limit} pytań.")
            break

        if question_limit == 0:
            user_input = input("Naciśnij Enter lub 'C' aby zakończyć: ").strip().lower()
            if user_input == 'c':
                break

        symbol, element_name = random.choice(question_pool)
        if repeat_mode:
            question_pool.remove((symbol, element_name))

        asked_count += 1
        mode = random.choice(["name_to_symbol", "symbol_to_name"])

        if use_images and mode == "name_to_symbol":
            print(f"Który pierwiastek ma ten symbol? {element_name}")
            show_image(symbol)
            answer = input("Wpisz symbol: ").strip()
            if is_correct_answer(answer, symbol, element_name):
                print("Poprawne!\n")
                correct += 1
            else:
                print(f"Niepoprawne. Poprawny symbol to {symbol} dla {element_name}.\n")
                mistakes += 1
                wrong_questions.append((symbol, element_name))
                if not repeat_mode:
                    question_pool.append((symbol, element_name))

        else:
            if mode == "name_to_symbol":
                print(f"Podaj symbol dla pierwiastka: {element_name}")
                answer = input("Wpisz symbol: ").strip()
                if is_correct_answer(answer, symbol, element_name):
                    print("Poprawne!\n")
                    correct += 1
                else:
                    print(f"Niepoprawne. Poprawny symbol to {symbol} dla {element_name}.\n")
                    mistakes += 1
                    wrong_questions.append((symbol, element_name))
                    if not repeat_mode:
                        question_pool.append((symbol, element_name))

            else:
                print(f"Który pierwiastek ma ten symbol: '{symbol}'?")
                answer = input("Wpisz nazwę pierwiastka: ").strip()
                if is_correct_answer(answer, symbol, element_name):
                    print("Poprawne!\n")
                    correct += 1
                else:
                    print(f"Niepoprawne. Poprawna nazwa to {element_name} dla {symbol}.\n")
                    mistakes += 1
                    wrong_questions.append((symbol, element_name))
                    if not repeat_mode:
                        question_pool.append((symbol, element_name))

    total = correct + mistakes
    if total == 0:
        print("Nie udzielono żadnych odpowiedzi.")
    else:
        perc_correct = (correct / total) * 100
        print(f"\nPodsumowanie quizu:")
        print(f"Liczba poprawnych odpowiedzi: {correct}")
        print(f"Liczba błędnych odpowiedzi: {mistakes}")
        print(f"Procent poprawnych odpowiedzi: {perc_correct:.2f}%")

        if mistakes > 0:
            print("\nPytania, które wymagały powtórki:")
            for sym, name in wrong_questions:
                print(f"{sym} :: {name}")
            # Save wrong questions to the for_repeating.txt file for next session
            with open(repetition_file, "w", encoding="utf-8") as f:
                for sym, name in wrong_questions:
                    f.write(f"{sym}::{name}\n")
            print(f"Błędne pytania zapisano w pliku: {repetition_file}")
        else:
            print("Gratulacje! Wszystkie odpowiedzi poprawne.")

if __name__ == "__main__":
    quiz()
