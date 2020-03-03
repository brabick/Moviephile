import time

import pyodbc
import pymysql
import os
import xlrd
import re
import sys


class DatabaseSupport:
	def __init__(self):
		return

	def conn_string(self):

		self.connection = pymysql.connect(
			host="localhost",
			user="root",
			passwd="my@llure32SQL",
			db="movie_review_db",
			autocommit=True
		)
		self.cursor = self.connection.cursor()

	def insert_to_db_from_excel(self, title, year, genre):
		try:
			# Execute the inserting stored procedure
			args = [title, year, genre]
			self.cursor.callproc("insert_from_excel", args)
		except pyodbc.Error as e:
			print(e)
		self.connection.close()

	def open_workbook(self):
		loc = "movie_info.xlsx"
		wb = xlrd.open_workbook(loc)
		sheet = wb.sheet_by_index(0)
		row = 1
		wants_to_add = ['movie', 'short']
		for i in range(10001):
			if sheet.row_values(i)[1] in wants_to_add and sheet.row_values(i)[4] == 0:
				data = [sheet.row_values(i)[2], sheet.row_values(i)[5], sheet.row_values(i)[8]]
				title = sheet.row_values(i)[2][:80]
				year = sheet.row_values(i)[5][:-2]
				genre = sheet.row_values(i)[8].replace(",", ", ")
				data_list = [title, year, genre]
				print(data_list)
				row += 1
				if row % 10000 == 0:
					print(row)
			elif sheet.row_values(i)[1] not in wants_to_add and i != 0:
				break

	def open_titles(self):
		print(sys.stdout.encoding)
		f = open("titles.txt", "r", encoding="utf8")
		movie_count = 0
		decode_error_count = 0
		line_continuer = 17083
		for line in f:
			self.conn_string(self)
			try:
				movie_count = movie_count + 1
				start = line.find("title=\"")
				end = line.find("\">")
				title = line[start:end][7:]
				start1 = line.find("</i> (")
				end1 = line.find(")</li>")
				year = line[start1:end1][6:]
				new_year = year[:4]
				genre = "N/A"
				print(movie_count)
				if title is not None and year is not None and title != "" and year != "":
					print(title, new_year)
					try:
						self.insert_to_db_from_excel(self, title[:75], new_year, genre)
					except pymysql.err.InternalError:
						print("ugh")
					except pymysql.err.OperationalError:
						time.sleep(1)
						print("sleeping")


			except UnicodeDecodeError:
				print("decode error nigga")
				decode_error_count = decode_error_count + 1
				print(decode_error_count)
		self.cursor.close()


if __name__ == "__main__":
	e = DatabaseSupport
	e.open_titles(e)
