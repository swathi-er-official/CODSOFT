"""This module provides access to some objects used or maintained by the
interpreter and to functions that interact strongly with the interpreter"""

import sys

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, \
    QPushButton, QHBoxLayout, QStackedWidget, QGridLayout, QLineEdit, QGroupBox, \
    QApplication, QRadioButton, QCheckBox

from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from PyQt6 import QtWidgets  #can be used to create Desktop Graphical User Interfaces

"""To update the quiz data questions and answers  and Total Score"""
class QuizPage(QWidget):
    def __init__(self, question, answers, question_type, quiz_data,
                 pages, show_total_score_window):
        super().__init__()
        self.question = question
        self.answers = answers
        self.question_type = question_type
        self.quiz_data = quiz_data
        self.pages = pages
        self.show_total_score_window = show_total_score_window
        self.initUI()

    def initUI(self):
        self.question_label = QLabel(self.question)
        # self.question_type_label = QLabel(self.question_type)
        self.answer_buttons = []
        self.button_to_answer = {}
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.question_label, 0, 0, 1, 2)

        if self.question_type == 'multiple_answer': #if multiple answers checkboxes created and updated
            for i, answer in enumerate(self.answers):
                button = QCheckBox(answer['answer'])
                button.toggled.connect(lambda _, answer=answer: self.update_total_score(answer))
                button.answer = answer
                self.answer_buttons.append(button)
                self.button_to_answer[button] = answer
                grid_layout.addWidget(button, i + 1, 0)
                grid_layout.setRowStretch(i + 1, 1)

        elif self.question_type == 'single_answer':  #if single answer radio button created and updated
            for i, answer in enumerate(self.answers):
                button = QRadioButton(answer['answer'])
                button.toggled.connect(lambda _, answer=answer: self.update_total_score(answer))
                button.answer = answer
                self.answer_buttons.append(button)
                self.button_to_answer[button] = answer
                grid_layout.addWidget(button, i + 1, 0)
                grid_layout.setRowStretch(i + 1, 1)

        self.setLayout(grid_layout)

    def handle_button(self, answer):
        if self.question_type == 'single_answer':
            num_checked = sum([button.isChecked() for button in self.answer_buttons])
            if num_checked > 1:
                for button in self.answer_buttons:
                    button.setEnabled(False)
            else:
                for button in self.answer_buttons:
                    button.setEnabled(True)

        elif self.question_type == 'multiple_answer':
            num_checked = sum([button.isChecked() for button in self.answer_buttons])
            if num_checked == 2:
                self.answer_buttons[answer].setChecked(True)
                for button in self.answer_buttons:
                    if not button.isChecked():
                        button.setEnabled(False)
            else:
                for button in self.answer_buttons:
                    button.setEnabled(True)

    def set_answers(self, answers):  # Set answers
        self.answers = answers
        for i, answer in enumerate(answers):
            self.answer_buttons[i].setText(answer['answer'])
            self.answer_buttons[i].setChecked(False)
            self.button_to_answer[self.answer_buttons[i]] = answer
            self.answer_buttons[i].show()

        # Hide any extra buttons
        if len(answers) < len(self.answer_buttons):
            for i in range(len(answers), len(self.answer_buttons)):
                self.answer_buttons[i].hide()

        self.total_score = 0

    def update_total_score(self, answer):
        if answer['is_correct']:
            if self.question_type == 'single_answer':
                self.total_score = 20  # 20 marks for a single correct answer
            else:
                self.total_score = 0
            if self.question_type == 'multiple_answer':
                correct_options = [answer['answer'] for answer in self.answers if answer['is_correct']]
                selected_options = [button.text() for button in self.answer_buttons if button.isChecked()]
                incorrect_options = set(selected_options) - set(correct_options)
                # update score based on partial or full answer
                if not incorrect_options and len(correct_options) == len(selected_options):
                    self.total_score = 20  # 10 marks for each correct checkbox option
                elif incorrect_options and len(incorrect_options) != len(correct_options):
                    self.total_score = 10  # 10 marks for partial answer

    def get_total_score(self):
        return self.total_score

"""To load quiz data and buttons"""
class QuizWidget(QWidget):
    quiz_finished = pyqtSignal()

    def __init__(self, quiz_data):
        super().__init__()
        self.quiz_data = quiz_data
        self.pages = []
        self.initUI()

    def initUI(self):
        for data in self.quiz_data:
            page = QuizPage(data['question'], data['answers'], data['question_type'], quiz_data, self.pages,
                            self.show_total_score_window)
            self.pages.append(page)

        self.stacked_widget = QStackedWidget()
        for page in self.pages:
            self.stacked_widget.addWidget(page)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.handle_prev)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.handle_next)
        self.finish_button = QPushButton("Finish")
        self.finish_button.clicked.connect(self.finish_quiz)
        self.play_button = QPushButton("Play Again")
        self.play_button.clicked.connect(self.play_quiz)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addWidget(self.finish_button)
        buttons_layout.addWidget(self.play_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.show_page(0)

    def show_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        if index == len(self.pages) - 1:
            self.finish_button.show()
            self.play_button.show()
        else:
            self.finish_button.hide()
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.pages) - 1)
        self.play_button.setEnabled(index >= len(self.pages) - 1)

        # Update answer choices
        answers = self.pages[index].answers
        self.pages[index].set_answers(answers)

    def handle_prev(self):
        index = self.stacked_widget.currentIndex()
        self.show_page(max(index - 1, 0))

    def handle_next(self):
        index = self.stacked_widget.currentIndex()
        self.show_page(min(index + 1, len(self.pages) - 1))

    def finish_quiz(self):
        total_score = sum(page.get_total_score() for page in self.pages)
        self.total_score_window = TotalScoreWindow(total_score, quiz_data)
        self.total_score_window.show()
        # self.quiz_finished.emit()

    def play_quiz(self):
        index = self.stacked_widget.currentIndex()
        self.show_page(max(index - 4, 0))

    def show_total_score_window(self):
        total_score = sum(page.get_total_score() for page in self.pages)
        self.total_score_window = TotalScoreWindow(total_score, quiz_data)
        self.total_score_window.show()

"""Score Window Display"""
class TotalScoreWindow(QtWidgets.QMainWindow):
    def __init__(self, total_score, quiz_data):
        super().__init__()
        self.quiz_data = quiz_data
        self.setWindowTitle("Total Score Window")
        self.setGeometry(100, 100, 300, 200)

        # create total score label
        total_score_label = QtWidgets.QLabel(f"Total Score: {total_score}", self)
        total_score_label.setGeometry(50, 50, 200, 50)

        # create central widget
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(QtWidgets.QVBoxLayout())
        central_widget.layout().addWidget(total_score_label)
        self.setCentralWidget(central_widget)

        self.performance_label = QLabel(self)
        self.performance_label.setVisible(True)
        self.performance_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.performance_label.setStyleSheet("color: purple")


        if total_score == 100:
            self.performance_label.setText("Very Good ")
        elif total_score >= 50:
            self.performance_label.setText("Good")
        else:
            self.performance_label.setText("Poor")

        correct_answers = []
        for data in quiz_data:
            for answer in data['answers']:
                if answer['is_correct']:
                    correct_answers.append(answer['answer'])
                    self.result_label = QtWidgets.QLabel(f"Correct answer(s): {', '.join(correct_answers)}")
                    self.result_label.show()

"""Welcome and Rules Page"""
class Rules(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QUIZ GAME")
        grid = QGridLayout()

        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-weight:bold")
        self.name_label_box = QLineEdit()
        self.error_label = QLabel(self)
        self.error_label.setVisible(True)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.error_label.setStyleSheet("color: red")

        self.welcome_label = QLabel("Welcome")
        self.welcome_label.setStyleSheet("font-weight:bold")
        rules_group = QGroupBox("Rules")
        rules_group.setStyleSheet("font-weight:bold")
        rule_grid = QGridLayout()
        rule_label = QLabel(
            "20 Marks for each correct answers.\n10 Marks for each answers in multiple choice answers.\n"
            "No Negative Mark")
        rule_label.setStyleSheet("color:red; font-weight:bold")
        rule_grid.addWidget(rule_label, 2, 0)
        rules_group.setLayout(rule_grid)
        grid.addWidget(rules_group, 3, 0)

        self.stacked_widget = QStackedWidget()
        grid.addWidget(self.stacked_widget, 6, 0, 1, 2)

        start_button = QPushButton("START")
        start_button.setStyleSheet("font-weight:bold")
        start_button.clicked.connect(self.start_quiz)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_label_box, 0, 1)
        grid.addWidget(self.welcome_label, 1, 0)
        grid.addWidget(start_button, 4, 0, 1, 2)
        grid.addWidget(self.error_label, 1, 1)

        self.setLayout(grid)

        self.quiz_widget = None
        self.name_label_box.textChanged.connect(self.name_change)

    """print name infront of Welcome"""
    def name_change(self):
        name = self.name_label_box.text()
        on_name_change = "<span style='color:darkviolet;font-weight:bold;'>{}</span>".format(name)
        self.welcome_label.setText("Welcome-{}".format(on_name_change))

    def start_quiz(self):
        if self.name_label_box.text():
            self.error_label.setVisible(False)
            self.setup_quiz()
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.error_label.setText("Please enter your name.")   # print error if name is not mentioned

    def setup_quiz(self):
        if self.quiz_widget:
            self.stacked_widget.removeWidget(self.quiz_widget)
        self.quiz_widget = QuizWidget(quiz_data)
        self.quiz_widget.quiz_finished.connect(self.show)
        self.stacked_widget.addWidget(self.quiz_widget)
        self.quiz_widget.show()


quiz_data = [
    {
        'question': 'Which two of these programming languages are compiled?(Select any two)',
        'question_type': 'multiple_answer',
        'answers': [
            {'answer': 'Python', 'is_correct': False},
            {'answer': 'Java', 'is_correct': True},
            {'answer': 'Ruby', 'is_correct': False},
            {'answer': 'JavaScript', 'is_correct': False},
            {'answer': 'C++', 'is_correct': True},
        ]
    },
    {
        'question': 'What is the capital of France?',
        'question_type': 'single_answer',
        'answers': [
            {'answer': 'Paris', 'is_correct': True},
            {'answer': 'London', 'is_correct': False},
            {'answer': 'Madrid', 'is_correct': False},
            {'answer': 'Berlin', 'is_correct': False},
        ]
    },
    {
        'question': 'What is the currency of Japan?',
        'question_type': 'single_answer',
        'answers': [
            {'answer': 'Yen', 'is_correct': True},
            {'answer': 'Dollar', 'is_correct': False},
            {'answer': 'Pound', 'is_correct': False},
            {'answer': 'Euro', 'is_correct': False},
        ]
    },
    {
        'question': 'What is the largest country in South America?',
        'question_type': 'single_answer',
        'answers': [
            {'answer': 'Brazil', 'is_correct': True},
            {'answer': 'Argentina', 'is_correct': False},
            {'answer': 'Peru', 'is_correct': False},
            {'answer': 'Colombia', 'is_correct': False},
        ]
    },

    {
        'question': 'Which two of these animals lay eggs?(Select any Two)',
        'question_type': 'multiple_answer',
        'answers': [
            {'answer': 'Cow', 'is_correct': False},
            {'answer': 'Dog', 'is_correct': False},
            {'answer': 'Kangaroo', 'is_correct': True},
            {'answer': 'Elephant', 'is_correct': False},
            {'answer': 'Platypus', 'is_correct': True},
        ]
    },
]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rule = Rules()
    rule.show()
    sys.exit(app.exec())
