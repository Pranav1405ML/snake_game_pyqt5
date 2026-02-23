import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontDatabase
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
FRUIT_SIZE = 50
SNAKE_SEGMENT_LENGTH = 50

# INITIAL POSITION OF SNAKE-
snake_position_x = (WINDOW_WIDTH// 2)
snake_position_y = (WINDOW_HEIGHT// 2)

class Game_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.is_game_over = False

        # SPECIAL FONT FOR SCORE
        font_id = QFontDatabase.addApplicationFont("../DS-DIGIT.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.score_font = QFont(font_family, 30)

        # FRUIT POSITION GENERATION
        a = random.randint(1,WINDOW_WIDTH // FRUIT_SIZE - 1)
        b = random.randint(1,WINDOW_HEIGHT // FRUIT_SIZE - 1)
        self.x = a
        self.y = b

        # STORING THE SNAKE IN THE LIST
        self.snake = [(snake_position_x, snake_position_y)]
        self.current_dir = "Down"
        self.head_x, self.head_y = self.snake[0]

        self.initUI()

        # TICKING TIMER AND STATIC TO DYNAMIC TRANSFORMATION
        self.timer = QTimer(self)

        # CHANGING THE STATUS EACH TICK OF GAME CLOCK
        self.timer.timeout.connect(self.update_game_status)
        self.timer.start(100)

        # BGM
        self.player1 = QMediaPlayer()
        self.player2 = QMediaPlayer()
        self.player1.setMedia(QMediaContent(QUrl.fromLocalFile("pokemon_ringtone.wav")))  # music file
        self.player2.setMedia(QMediaContent(QUrl.fromLocalFile("mario_fail.wav")))  # gameover bgm file
        self.player1.setVolume(50)  # 0-100
        self.player2.setVolume(50)  # 0-100

        if not self.is_game_over:
            self.player1.play()

    def initUI(self):
        self.setWindowTitle("SNAKE GAME")
        self.setGeometry(200, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setStyleSheet("""
           QWidget{
             background-color: black;           
           }
        """)

    def paintEvent(self, event):        # it doesn't need a call unlike initUI
        painter = QPainter(self)
        outline1 = QPen(QColor(0,0,0))  # black outline
        outline1.setWidth(2)            # 2 pixel width
        color1 = QBrush(QColor("#09e85b"))  # green snake

        # PAINTING THE SNAKE
        painter.setPen(outline1)
        painter.setBrush(color1)
        for x, y in self.snake:
         painter.drawRect(x, y, SNAKE_SEGMENT_LENGTH,SNAKE_SEGMENT_LENGTH)

        outline2 = QPen(QColor(0, 0, 0))  # black outline
        outline2.setWidth(2)  # 2 pixel width
        color2 = QBrush(QColor("#e31224"))  # painted red fruit

        # PAINTING THE FRUIT
        painter.setPen(outline2)
        painter.setBrush(color2)
        painter.drawEllipse(self.x * FRUIT_SIZE, self.y * FRUIT_SIZE, FRUIT_SIZE, FRUIT_SIZE)

        painter.setFont(self.score_font)
        painter.setPen(QColor("#00ff00"))  # digital green
        score_text = f"Score: {len(self.snake) - 1}"
        painter.drawText(20, 50, score_text)  # adjust x, y to position

    def keyPressEvent(self, event):  # HANDLES KEYPRESSES.
        if event.key() == Qt.Key_Up:
           self.current_dir = "Up"

        elif event.key() == Qt.Key_Down:
            self.current_dir = "Down"

        elif event.key() == Qt.Key_Left:
            self.current_dir = "Left"

        elif event.key() == Qt.Key_Right:
            self.current_dir = "Right"

    def move_snake(self):

      head_x, head_y = self.snake[0]
      new_head1 = (head_x, head_y - SNAKE_SEGMENT_LENGTH)
      new_head2 = (head_x, head_y + SNAKE_SEGMENT_LENGTH)
      new_head3 = (head_x + SNAKE_SEGMENT_LENGTH, head_y)
      new_head4 = (head_x - SNAKE_SEGMENT_LENGTH, head_y)

      if self.current_dir == "Up" :
           self.snake.insert(0, new_head1)
           self.head_x, self.head_y = new_head1

      elif self.current_dir == "Down":
          self.snake.insert(0, new_head2)
          self.head_x, self.head_y = new_head2

      elif self.current_dir == "Right":
          self.snake.insert(0, new_head3)
          self.head_x, self.head_y = new_head3

      elif self.current_dir == "Left":
          self.snake.insert(0, new_head4)
          self.head_x, self.head_y = new_head4

      #  BORDER-COLLISION
      if self.head_x < 0 or self.head_x >= WINDOW_WIDTH or self.head_y < 0 or self.head_y >= WINDOW_HEIGHT:
         self.snake.pop()
         self.gameover()
         return
      # AUTOMATIC GROWTH-PREVENTION
      elif not self.x * FRUIT_SIZE == self.head_x or not self.head_y == self.y * FRUIT_SIZE:
          self.snake.pop()

    def check_collisions(self):
        # NEW FRUIT AFTER EATING ONE
        if self.x * FRUIT_SIZE == self.head_x and self.head_y == self.y * FRUIT_SIZE:
            self.move_fruit()
        # SELF-COLLISION
        for x in self.snake[1::1]:
            if x[0] == self.head_x and x[1] == self.head_y :
                self.gameover()
                break

    def move_fruit(self):
        # NEW POSITION FOR OUR FRUIT.
        # WHILE LOOP ENSURES NO OVERLAP OF SNAKE AND FOOD.
        while (self.x*FRUIT_SIZE,self.y*FRUIT_SIZE) in self.snake:
            self.x = random.randint(1, WINDOW_WIDTH // FRUIT_SIZE - 1)
            self.y = random.randint(1, WINDOW_HEIGHT // FRUIT_SIZE - 1)

    def update_game_status(self):
        # UPDATE GAME_BOARD EVERY TICK
        self.move_snake()
        self.check_collisions()
        self.update()   # REPAINT

    def gameover(self):
        # LEARNT ABOUT QMessageBox
        self.is_game_over = True
        self.player1.stop()
        self.player2.play()

        message = QMessageBox()
        message.setWindowTitle("Game Over")
        message.setText("GAMEOVER")
        message.setFont(QFont("Arial", 50, QFont.Bold))


        label = message.findChild(QLabel, "qt_msgbox_label")  # the main text label
        if label:
            # digital-clock style font
            label.setFont(self.score_font)
            label.setStyleSheet("""
                    color: #00ff00;           /* green digital color */
                    background-color: black;
                    border: 2px solid #00ff00; /* optional glowing border */
                    padding: 10px;
                """)
            label.setAlignment(Qt.AlignCenter)
            label.setText(f"GAME OVER\n SCORE: {len(self.snake)-1}")

        message.setStyleSheet(
            """
            QMessageBox{
              background-color: black;
            }
            QPushButton {
            background-color: #444444;
            color: white;
            font-weight: bold;
            min-width: 80px;
            min-height: 30px;
        }
            """
        )
        # STOP THE GAME AND THE TIMER.
        self.timer.stop()
        message.exec_()  # VERY IMP FOR EXECUTION


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game_Window()
    game.show()
    sys.exit(app.exec_())
