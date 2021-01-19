from lixin1 import Inquiry
import os

username = [  # list the student ID for inquiry
    "171910101",
    "181910101",
    "191910101",
]

if not os.path.exists('./grades/'):
    os.mkdir('./grades/')
for student in username:
    inquiry = Inquiry(student)
    grade_book = inquiry.run()
    grade_book.to_excel(f"./grades/Transcripts_{student}.xlsx", index=False)
