# coding=UTF-8
import gui
import processing

filename = "French.csv"

df = processing.readAsDF(filename)

gui.display(df)
