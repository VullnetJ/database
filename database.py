import sys
from PyQt5 import QtWidgets, QtGui
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

app = QtWidgets.QApplication(sys.argv)

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Create a table widget to display the records in the User table
table = QtWidgets.QTableWidget()
table.setRowCount(session.query(User).count())
table.setColumnCount(2)
table.setHorizontalHeaderLabels(['Name', 'Email'])

# Populate the table with the records from the User table
records = session.query(User).all()
for i, record in enumerate(records):
    name_item = QtWidgets.QTableWidgetItem(record.name)
    email_item = QtWidgets.QTableWidgetItem(record.email)
    table.setItem(i, 0, name_item)
    table.setItem(i, 1, email_item)

# Create a button to save data to the database
save_button = QtWidgets.QPushButton("Save")
save_button.clicked.connect(lambda: save_data_to_db(table, session))

# Create a layout to hold the table and button
layout = QtWidgets.QVBoxLayout()
layout.addWidget(table)
layout.addWidget(save_button)

# Create a main window and set the layout as the central widget
window = QtWidgets.QMainWindow()
central_widget = QtWidgets.QWidget()
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

# Show the main window
window.show()

sys.exit(app.exec_())

def save_data_to_db():
    name = name_input.text()
    email = email_input.text()

    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()

    # Refresh the table widget to display the new record
    table.setRowCount(session.query(User).count())
    latest_record = session.query(User).all()[-1]
    name_item = QtWidgets.QTableWidgetItem(latest_record.name)
    email_item = QtWidgets.QTableWidgetItem(latest_record.email)
    table.setItem(table.rowCount() - 1, 0, name_item)
    table.setItem(table.rowCount() - 1, 1, email_item)

    save_button = QtWidgets.QPushButton("Save")
    save_button.clicked.connect(save_data_to_db)

    # Commit the changes to the database
    session.commit()