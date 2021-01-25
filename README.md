# SLU Course Viewer
 Auto export grades in Shanghai Lixin University of Accounting and Finance from the data center

![](https://img.shields.io/badge/tests-2021.1.19%20%E2%9C%94-green)

![](https://img.shields.io/badge/dependencies-Python%203.7-blue)

## Introduction

**Student 2021 version**

The university does not provide a tool to export all your grades. And, you need to manually copy courses from webpage to your MS Excel(R) book. Therefore, I provide a tool to complete this task.

**Notes:** The university will update new scores to data center HALF A YEAR later than to the course system.

## Usage

1. Set the program as current folder, and run `pip install -r requirements`.
2. Ensure you have connected to the computer network in Shanghai Lixin University of Accounting and Finance. **If you connect with proxies, this program does not work because it doesn't trust your system proxies.**
3. Open `main_public.py`, and fill student IDs you want to inquire in the `username` Python list.
4. Run `main_public.py`.
5. Get your transcripts in the `grades` folder.

