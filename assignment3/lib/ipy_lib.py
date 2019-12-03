'''
Created on 30 Jan. 2012
Finished on 6 Feb. 2012

Improvements:
 - 1 Mar. 2012 to 2 Mar. 2012: fixed a rare threading related crash
 - 3 Mar. 2012 to 5 Mar. 2012: fixed a bug in showing names of the barchart
 - 17 Mar. 2012 to 18 Mar. 2012: fixed not running on Linux
 - 31 Jul. 2012 to 31 Jul. 2012: added UserInput and 'privatised' most classes and imports
 - 1 Aug. 2012 to 2 Aug. 2012: fixed another bug with showing names of the barchart and a bug with displaying text in othello
 - 4 Aug. 2012 to 4 Aug. 2012: fixed bug with opening a file and fixed functionality of closing the window
 - 6 Aug. 2012 to 7 Aug. 2012: fixed multiple windows crashing the UI, reverted change to UserInput with this change
 - 21 Aug. 2012 to 21 Aug. 2012: adjusted naming from JAVA to Python convention, changed UserInput to a function that returns all input, added Life interface
 - 22 Aug. 2012 to 22 Aug. 2012: added scrollbar to othello, snake and life interfaces, added type checking and exceptions for all input
 - 2 Sep. 2012 to 2 Sep. 2012: fixed another bug with names of the barchart, allowed ints to be given to floats, fixed spelling
 - 13 Sep. 2012 to 13 Sep. 2012: fixed more spelling, added functionality for multiple answers per question
 - 27 Sep. 2012 to 27 Sep. 2012: changed multiple answers from array to arbitrary arguments list, added exception if argument list is empty
 - 6 Dec. 2012 to 6. Dec. 2012: fixed resets of auto alarm speed by adding a timer
 - 2 Oct. 2013 to 3. Oct. 2013: fixed ranged errors, fixed closing bug in Windows and Linux when only calling ask_user or file_input,
                                fixed typos, added Escape as window closer, fixed window not getting focus when started, added Mac support (!)
 - 9 Oct. 2013 to 9. Oct. 2013: fixed get_event (Mac version) to properly give refresh events
 - 12 Nov. 2014 to 12. Nov. 2014: fixed OS X to not use PIL anymore and instead of images draw some simple shapes
 - 21 Nov. 2014 to 21. Nov. 2014: fixed OS X BarChartUI to properly show bar names without calling show
 - 15 May. 2015 to 15 May. 2015: added user interfaces for programming for economy -- Sebastian
 - 22 Jun. 2015 to 22 Jun. 2015: fixed asking twice for file_input on Windows -- Gerben

@author: Gerben Rozie
@author: Sebastian Osterlund
'''
import Tkinter as _tk
import Dialog as _Dialog
import tkFileDialog as _tkFileDialog
import tkMessageBox as _tkMessageBox
import Queue as _Queue
import threading as _threading
import time as _time
import os as _os
import random as _random
import sys as _sys

have_mpl = False
try:
    import matplotlib as mpl
    if _sys.platform == 'linux' or _sys.platform == 'linux2':
        mpl.rcParams['backend'] = 'QT4Agg'
    import pylab as plt
    if _sys.platform == 'linux' or _sys.platform == 'linux2':
        plt.switch_backend('QT4Agg') # Use QT4 for linux. Bug in TK.
    have_mpl = True
except ImportError:
    print "Could not import matplotlib. HouseMarketUserInterface and StockMarketUserInterface have been disabled."
import time as _time
import datetime as _datetime
import pickle as _pickle
import urllib2, urllib, json 

YAHOO_URL = 'https://query.yahooapis.com/v1/public/yql'
	
class _IPyException(Exception):
    def __init__(self, value):
        self.parameter = value
    
    def __str__(self):
        return repr(self.parameter)

def _verify_int(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, int):
        value = "%s not an int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)

def _verify_float(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, float):
        if not isinstance(value_var, int):
            value = "%s is not a float or int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
            raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)

def _verify_str(value_var, string_var):
    if not isinstance(value_var, basestring):
        value = "%s is not a string for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)

def _verify_bool(value_var, string_var):
    if not isinstance(value_var, bool):
        value = "%s is not a boolean for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)

def _verify_input(value_var, string_var, minimum=None, maximum=None):
    if minimum is None:
        minimum = float('-inf')
    if maximum is None:
        maximum = float('inf')
    if value_var >= minimum:
        if value_var <= maximum:
            return
    value = "%s is out of bounds, expected range: %s to %s, got: %s" % (string_var, minimum, maximum, value_var)
    raise _IPyException(value)

class _OthelloReplayHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class _BarChartHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, bar_index):
        self.bar_index = bar_index

class _BarChartNameHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, bar_index, bar_name):
        self.bar_index = bar_index
        self.bar_name = bar_name

class _SnakeHolder(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class _LifeHolder(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    _ui_factory = None
    
def file_input():
	"""This function lets the user select a file to use for input.
	Returns the file contents in a string.
	"""
	
	global _ui_factory
	f = _AskInput(_ui_factory.mainroot).f
	if f == '':
		return None
	return str(_sys.stdin.read())

def ask_user(question, *options):
	"""Ask the user a question.
	Parameters:
	- question: the string to ask the user
	- options: arbitrary list of arguments (at least 1)
	Returns the chosen option by the user or None if nothing was chosen (e.g. hit Escape).
	"""
	
	if len(options) == 0:
		value = "User needs to be able to select at least 1 answer"
		raise _IPyException(value)
	global _ui_factory
	return _AskUser(_ui_factory.mainroot, question, options).answer


class _Factory():
	def __init__(self):
		self.mainroot = _tk.Tk()
		self.mainroot.withdraw()
		self.mainroot.update()

class _AskInput(object):
	def __init__(self, mainroot):
		root = _tk.Toplevel(mainroot)
		root.withdraw()
		self.f = _tkFileDialog.askopenfilename(parent=root)
		if self.f is not '':
			_sys.stdin = file(self.f)
		root.destroy()

class _AskUser(object):
	def __init__(self, mainroot, question, options):
		root = _tk.Toplevel(mainroot)
		root.withdraw()
		dg = _Dialog.Dialog(None,
		title="",
		text=question,
		default=0,
		bitmap=_tkMessageBox.QUESTION,
		strings=options)
		self.answer = options[dg.num]
		root.destroy()

class OthelloReplayUserInterface(object):
	def __init__(self, scale=1.0):
		"""This class starts the OthelloReplayUserInterface.
		Constants:
		- NUMBER_OF_ROWS
		- NUMBER_OF_COLUMNS
		- EMPTY
		- WHITE
		- BLACK
		
		Parameters for the class: (none)
		
		Optional parameters:
		- scale: 0.25 to 1.0
		"""
		
		_verify_float(scale, 'Scale', 0.25, 1.0)
		global _ui_factory
		self.othello_replay = _Othello(_ui_factory.mainroot, scale)
		self.NUMBER_OF_ROWS = _Othello.NUMBER_OF_ROWS
		self.NUMBER_OF_COLUMNS = _Othello.NUMBER_OF_COLUMNS
		self.EMPTY = _Othello.EMPTY
		self.WHITE = _Othello.WHITE
		self.BLACK = _Othello.BLACK
	
	def place(self, x, y, color):
		"""Place an Othello piece (defined by 'color') on the given X and Y coordinates.
		"""
		
		_verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
		_verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
		# 0 = empty, 1 = white, 2 = black, 3 = white_t, 4 = black_t
		_verify_int(color, 'Color', 0, 4)
		self.othello_replay.place(x, y, color)
	
	def place_transparent(self, x, y, color):
		"""Place a semi-transparent Othello piece (defined by 'color') on the given X and Y coordinates.
		"""
		
		_verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
		_verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
		# 0 = empty, 1 = white_t, 2 = black_t (before next step in code)
		_verify_int(color, 'Color', 0, 2)
		if color == self.EMPTY:
			self.place(x, y, self.EMPTY)
		else:
			self.place(x, y, color+2)
	
	def clear(self):
		"""Clears the display.
		Note: this does not clear the text area!
		"""
		
		self.othello_replay.clear()
	
	def show(self):
		"""Show the changes made to the display (i.e. after calling place or clear).
		"""
		
		self.othello_replay.show()
	
	def print_(self, text):
		"""Print text to the text area on the display.
		This function does not add a trailing newline by itself.
		"""
		
		
		_verify_str(text, "Text")
		self.othello_replay.print_(text)
	
	def clear_text(self):
		"""Clears the text area on the display.
		"""
		
		self.othello_replay.clear_text()
	
	def wait(self, ms):
		"""Let your program wait for an amount of milliseconds.
		
		This function only guarantees that it will wait at least this amount of time.
		If the system, i.e., is too busy, then this time might increase.
		- Python time module.
		"""
		
		_verify_int(ms, "Waiting time", 0)
		self.othello_replay.wait(ms)
	
	def close(self):
		"""Closes the display and stops your program.
		"""
		
		self.othello_replay.close()
	
	def stay_open(self):
		"""Force the window to remain open.
		Only has effect on Mac OS to prevent the window from closing after the execution finishes.
		
		Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
		"""
		
		global _ui_factory
		_ui_factory.mainroot.mainloop()

class _Othello(object):
	#one cannot prevent users from editing 'constants', as constants simply do not exist in Python
	NUMBER_OF_ROWS = 8
	NUMBER_OF_COLUMNS = 8
	EMPTY = 0
	WHITE = 1
	BLACK = 2
	
	r = 20
	g = 120
	b = 0
	BACKGROUND = "#%02X%02X%02X" % (r,g,b) #BACKGROUND = "#147800"?
	
	def __init__(self, mainroot, scale=1.0):
		#create queue to store changes to placings
		self.to_show_queue = _Queue.Queue(maxsize=0)
		
		#start the main window
		self.root = _tk.Toplevel(mainroot)
		self.root.title("OthelloReplayUserInterface")
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.bind("<Escape>", self.callback)
		self.root.resizable(False, False)
		
		#calculate sizes
		self.text_height = int(200 * scale)
		self.othello_size = int(800 * scale)
		
		#create main frame
		self.frame = _tk.Frame(self.root, width=self.othello_size, height=self.othello_size+self.text_height)
		self.frame.pack_propagate(0)
		self.frame.pack()
		
		#create board to hold references to othello-pieces
		self.white_board = [] # for storing references to create_image
		self.black_board = []
		self.white_ghost_board = []
		self.black_ghost_board = []
		self.img_refs = [] # for storing references to images - order: white, black
		
		#create and fill the canvas --> paintable area
		self.c = _tk.Canvas(self.frame, width=self.othello_size, height=self.othello_size, bg=self.BACKGROUND, bd=0, highlightthickness=0)
		self.c.pack()
		self.c.focus_set()
		self.fill_canvas()
		
		#create the textholder
		self.scrollbar = _tk.Scrollbar(self.frame)
		self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
		self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
		self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(state=_tk.DISABLED)
		
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def callback(self, event=None):
		self.root.destroy()
		_os._exit(0)
	
	def place(self, x, y, color):
		element = _OthelloReplayHolder(x, y, color)
		self.to_show_queue.put(element)
	
	def clear(self):
		for x in range(self.NUMBER_OF_COLUMNS):
			for y in range(self.NUMBER_OF_ROWS):
				self.place(x, y, self.EMPTY)
	
	def show(self):
		try:
			while True:
				element = self.to_show_queue.get_nowait()
				position = []
				position.append(self.white_board[element.x][element.y])
				position.append(self.black_board[element.x][element.y])
				position.append(self.white_ghost_board[element.x][element.y])
				position.append(self.black_ghost_board[element.x][element.y])
				for i in range(len(position)):
					if element.color == i+1:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.NORMAL)
					else:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.HIDDEN)
		except _Queue.Empty:
			pass
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def print_(self, text):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.insert(_tk.END, text)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def clear_text(self):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.delete(1.0, _tk.END)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def wait(self, ms):
		try:
		  _time.sleep(ms * 0.001)
		except:
		  self.close()
	
	def close(self):
		self.root.destroy()
		_os._exit(0)
	
	def create_othello_grid(self):
		for i in range(self.NUMBER_OF_COLUMNS+1):
			x0 = self.xpad + self.xstep * i
			y0 = self.ypad
			x1 = x0
			y1 = self.ypad + self.ystep * self.NUMBER_OF_ROWS + 1
			coords = x0, y0, x1, y1
			self.c.create_line(coords, fill='black')
		for j in range(self.NUMBER_OF_ROWS+1):
			x0 = self.xpad
			y0 = self.ypad + self.ystep * j
			x1 = self.xpad + self.xstep * self.NUMBER_OF_COLUMNS + 1
			y1 = y0
			coords = x0, y0, x1, y1
			self.c.create_line(coords, fill='black')
		for i in range(self.NUMBER_OF_COLUMNS):
			x0 = self.xpad + self.xstep / 2 + self.xstep * i
			y0 = self.ypad / 2
			x1 = x0
			y1 = self.othello_size - self.ystep / 2
			coords0 = x0, y0
			coords1 = x1, y1
			self.c.create_text(coords0, text=chr(ord('a')+i))
			self.c.create_text(coords1, text=chr(ord('a')+i))
		for j in range(self.NUMBER_OF_ROWS):
			x0 = self.xpad / 2
			y0 = self.ypad + self.ystep / 2 + self.ystep * j
			x1 = self.othello_size - self.xstep / 2
			y1 = y0
			coords0 = x0, y0
			coords1 = x1, y1
			self.c.create_text(coords0, text='%s'%(j+1))
			self.c.create_text(coords1, text='%s'%(j+1))
	
	def mix_color(self, c1, c2, mix):
		return c1 if mix == 0 else (c1 + c2) / 2
	
	def create_piece(self, x0, y0, img, mix):
		result = []
		if img == self.WHITE:
			r = self.mix_color(255, self.r, mix)
			g = self.mix_color(255, self.g, mix)
			b = self.mix_color(255, self.b, mix)
			scale = 0.8
			x1 = x0 + (1.0 - scale) / 2.0 * self.xstep
			y1 = y0 + (1.0 - scale) / 2.0 * self.ystep
			x2 = x0 + (1.0 - (1.0 - scale) / 2.0) * self.xstep
			y2 = y0 + (1.0 - (1.0 - scale) / 2.0) * self.ystep
			result.append(self.c.create_oval(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=0))
		if img == self.BLACK:
			r = self.mix_color(0, self.r, mix)
			g = self.mix_color(0, self.g, mix)
			b = self.mix_color(0, self.b, mix)
			scale = 0.8
			x1 = x0 + (1.0 - scale) / 2.0 * self.xstep
			y1 = y0 + (1.0 - scale) / 2.0 * self.ystep
			x2 = x0 + (1.0 - (1.0 - scale) / 2.0) * self.xstep
			y2 = y0 + (1.0 - (1.0 - scale) / 2.0) * self.ystep
			result.append(self.c.create_oval(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=0))
		
		return result
	
	def create_othello_pieces(self):
		mixer = 0, 0, 1, 1
		imgtype = self.WHITE, self.BLACK, self.WHITE, self.BLACK
		boards = self.white_board, self.black_board, self.white_ghost_board, self.black_ghost_board
		for n in range(len(boards)):
			for i in range(self.NUMBER_OF_COLUMNS):
				boards[n].append([])
				for j in range(self.NUMBER_OF_ROWS):
					x0 = self.xpad + self.xstep * i
					y0 = self.ypad + self.ystep * j
					img = self.create_piece(x0, y0, imgtype[n], mixer[n])
					boards[n][i].append(img)
	
	def fill_canvas(self):
		self.xstep = self.othello_size / (self.NUMBER_OF_COLUMNS + 2)
		self.ystep = self.othello_size / (self.NUMBER_OF_ROWS + 2)
		self.xpad = (self.othello_size - self.NUMBER_OF_COLUMNS * self.xstep) / 2
		self.ypad = (self.othello_size - self.NUMBER_OF_ROWS * self.ystep) / 2
		self.create_othello_grid()
		self.create_othello_pieces()

class BarChartUserInterface(object):
	def __init__(self, bar_count):
		"""This class starts the BarChartUserInterface.
		Constants: (none)
		
		Parameters for the class:
		- bar_count: at least 1
		
		Optional parameters: (none)
		"""
		_verify_int(bar_count, "Bar count", 1)
		global _ui_factory
		self.bar_chart = _BarChart(bar_count, _ui_factory.mainroot)
	
	def set_bar_name(self, bar_index, text):
		"""Set a name, provided by 'text', to a given bar_index.
		Note: this function's effects are visible without calling show.
		"""
		
		_verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
		_verify_str(text, "Text")
		self.bar_chart.set_bar_name(bar_index, text)
	
	def raise_bar(self, bar_index):
		"""Increment the given bar_index by 1.
		"""
		
		_verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
		self.bar_chart.raise_bar(bar_index)
	
	def show(self):
		"""Show the changes made to the display (i.e. after calling raise_bar).
		"""
		
		self.bar_chart.show()
	
	def show_names(self, value):
		"""Whether or not to show the names of the bars.
		Value given must be a boolean.
		Default at start is False.
		"""
		
		_verify_bool(value, "Show names")
		self.bar_chart.show_names(value)
	
	def show_values(self, value):
		"""Whether or not to show the values of the bars.
		Value given must be a boolean.
		Default at start is True.
		"""
		
		_verify_bool(value, "Show values")
		self.bar_chart.show_values(value)
	
	def wait(self, ms):
		"""Let your program wait for an amount of milliseconds.
		
		This function only guarantees that it will wait at least this amount of time.
		If the system, i.e., is too busy, then this time might increase.
		- Python time module.
		"""
		
		_verify_int(ms, "Waiting time", 0)
		self.bar_chart.wait(ms)
	
	def close(self):
		"""Closes the display and stops your program.
		"""
		
		self.bar_chart.close()
	
	def stay_open(self):
		"""Force the window to remain open.
		Only has effect on Mac OS to prevent the window from closing after the execution finishes.
		
		Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
		"""
		
		global _ui_factory
		_ui_factory.mainroot.mainloop()

class _BarChart(object):
	def __init__(self, bar_count, mainroot):
		#create queue to store changes to placings
		self.to_show_queue = _Queue.Queue(maxsize=0)
		
		#variables used to keep the number of refreshes of names and values in check
		self.show_names_bool = False
		self.show_values_bool = True
		
		self.bar_count = bar_count
		
		#start the main window
		self.root = _tk.Toplevel(mainroot)
		self.root.title("BarChartUserInterface")
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.bind("<Escape>", self.callback)
		self.frame = _tk.Frame(self.root)
		self.frame.pack(fill=_tk.BOTH, expand=_tk.YES)
		self.height = 575
		self.width = 400
		self.c = _tk.Canvas(self.frame, width=self.width, height=self.height, bg='white', bd=0, highlightthickness=0)
		self.c.pack(fill=_tk.BOTH, expand=_tk.YES)
		self.c.focus_set()
		self.c.bind('<Configure>', self.redraw)
		self.bar_max = 0
		self.bars = []
		self.names = []
		self.create_bars()
		self.redraw()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def callback(self, event=None):
		self.root.destroy()
		_os._exit(0)
	
	def set_bar_name(self, bar_index, text):
		self.names[bar_index] = text;
		self.redraw()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def raise_bar(self, bar_index):
		element = _BarChartHolder(bar_index)
		self.to_show_queue.put(element)
	
	def inc_bar(self, bar_index):
		if (self.bars[bar_index] + 1) > self.bar_max:
			self.bar_max = self.bars[bar_index] + 1
		self.bars[bar_index] += 1
	
	def show(self):
		try:
			while True:
				element = self.to_show_queue.get_nowait()
				self.inc_bar(element.bar_index)
		except _Queue.Empty:
			pass
		self.redraw()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def show_names(self, value):
		self.show_names_bool = value
		self.redraw()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def show_values(self, value):
		self.show_values_bool = value
		self.redraw()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def wait(self, ms):
		try:
		  _time.sleep(ms * 0.001)
		except:
		  self.close()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def close(self):
		self.root.destroy()
		_os._exit(0)
		return
	
	def create_bars(self):
		for i in range(self.bar_count): #@UnusedVariable
			self.bars.append(0)
			self.names.append('')
	
	def redraw(self, event=None):
		if event != None:
			self.width = event.width
			self.height = event.height
		for e in self.c.find_all():
			self.c.delete(e)
		self.fill_canvas()
	
	def fill_canvas(self):
		xstep = self.width / (self.bar_count + 2)
		xpad = (self.width - xstep * self.bar_count) / 2
		xspacing = xstep / 10
		ypad = self.height / 10
		ypadtext = ypad / 3
		for i in range(self.bar_count):
			#draw the bar
			x0 = xpad + xstep * i + xspacing
			y0 = self.height - ypad
			x1 = xpad + xstep * (i + 1) - xspacing
			y1 = self.height - ypad
			color = 0
			if self.bar_max > 0:
				y_len = self.bars[i] * (self.height - 2 * ypad) / self.bar_max
				y1 -= y_len
				color = self.bars[i] * 255 / self.bar_max
			coords = x0, y0, x1, y1
			hex_color = "#%02x%02x%02x" % (color, 0, 0) #red, green, blue
			self.c.create_rectangle(coords, fill=hex_color)
			
			#draw the values
			x1 = xpad + xstep * i + xstep / 2
			y1 -= ypadtext
			coords = x1, y1
			value = ("%d" % self.bars[i]) if self.show_values_bool else ''
			self.c.create_text(coords, text=value)
			
			#draw the names
			x0 = xpad + xstep * i + xstep / 2
			y0 += ypadtext
			coords = x0, y0
			name = self.names[i] if self.show_names_bool else ''
			self.c.create_text(coords, text=name)

class SnakeUserInterface(object):
	def __init__(self, width, height, scale=1.0):
		"""This class starts the SnakeUserInterface.
		Constants:
		- EMPTY
		- FOOD
		- SNAKE
		- WALL
		
		Parameters for the class:
		- width: at least 1
		- height: at least 1
		
		Optional parameters:
		- scale: 0.25 to 1.0
		"""
		
		_verify_int(width, "Width", 1)
		_verify_int(height, "Height", 1)
		_verify_float(scale, 'Scale', 0.25, 1.0)
		global _ui_factory
		self.snake_interface = _Snake(width, height, _ui_factory.mainroot, scale)
		self.EMPTY = _Snake.EMPTY
		self.FOOD = _Snake.FOOD
		self.SNAKE = _Snake.SNAKE
		self.WALL = _Snake.WALL
	
	def place(self, x, y, color):
		"""Place a Snake piece (defined by 'color') on the given X and Y coordinates.
		"""
		
		_verify_int(x, 'X', 0, self.snake_interface.width - 1)
		_verify_int(y, 'Y', 0, self.snake_interface.height - 1)
		# 0 = empty, 1 = food, 2 = snake, 3 = wall, 4 = food_t, 5 = snake_t, 6 = wall_t
		_verify_int(color, 'Color', 0, 6)
		self.snake_interface.place(x, y, color)
	
	def place_transparent(self, x, y, color):
		"""Place a semi-transparent Snake piece (defined by 'color') on the given X and Y coordinates.
		"""
		
		_verify_int(x, 'X', 0, self.snake_interface.width - 1)
		_verify_int(y, 'Y', 0, self.snake_interface.height - 1)
		# 0 = empty, 1 = food_t, 2 = snake_t, 3 = wall_t (before next step in code)
		_verify_int(color, 'Color', 0, 6)
		if color == self.EMPTY:
			self.place(x, y, self.EMPTY)
		else:
			self.place(x, y, color+3)
	
	def clear(self):
		"""Clears the display.
		Note: this does not clear the text area!
		"""
		
		self.snake_interface.clear()
	
	def show(self):
		"""Show the changes made to the display (i.e. after calling place or clear)
		"""
		
		self.snake_interface.show()
	
	def get_event(self):
		"""Returns an event generated from the display.
		The returned object has 2 properties:
		- name: holds the group which the event belongs to.
		- data: holds useful information for the user.
		"""
		
		return self.snake_interface.get_event()
	
	def set_animation_speed(self, fps):
		"""Set an event to repeat 'fps' times per second.
		If the value is set to 0 or less, the repeating will halt.
		In theory the maximum value is 1000, but this depends on activity of the system.
		
		The generated events (available by using get_event) have these properties:
		- name: 'alarm'.
		- data: 'refresh'.
		"""
		
		_verify_float(fps, "Animation speed")
		self.snake_interface.set_animation_speed(fps)
	
	def print_(self, text):
		"""Print text to the text area on the display.
		This function does not add a trailing newline by itself.
		"""
		
		_verify_str(text, "Text")
		self.snake_interface.print_(text)
	
	def clear_text(self):
		"""Clears the text area on the display.
		"""
		
		self.snake_interface.clear_text()
	
	def wait(self, ms):
		"""Let your program wait for an amount of milliseconds.
		
		This function only guarantees that it will wait at least this amount of time.
		If the system, i.e., is too busy, then this time might increase.
		- Python time module.
		"""
		
		_verify_int(ms, "Waiting time", 0)
		self.snake_interface.wait(ms)
	
	def random(self, maximum):
		"""Picks a random integer ranging from 0 <= x < maximum
		Minimum for maximum is 1
		"""
		
		_verify_int(maximum, 'Random', 1)
		return self.snake_interface.random(maximum)
	
	def close(self):
		"""Closes the display and stops your program.
		"""
		
		self.snake_interface.close()
	
	def stay_open(self):
		"""Force the window to remain open.
		Only has effect on Mac OS to prevent the window from closing after the execution finishes.
		
		Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
		"""
		
		global _ui_factory
		_ui_factory.mainroot.mainloop()

class _Snake(object):
	#one cannot prevent users from editing 'constants', as constants simply do not exist in Python
	EMPTY = 0
	FOOD = 1
	SNAKE = 2
	WALL = 3
	
	def __init__(self, width, height, mainroot, scale=1.0):
		#create queue to store changes to placings
		self.to_show_queue = _Queue.Queue(maxsize=0)
		self.event_queue = _Queue.Queue(maxsize=0)
		
		#copy params
		self.width = width
		self.height = height
		self.scale = scale
		
		self.closing_window = False
		
		#start the main window
		self.root = _tk.Toplevel(mainroot)
		self.root.title("SnakeUserInterface")
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.bind("<Escape>", self.callback)
		self.root.resizable(False, False)
		
		#calculate sizes
		self.size_per_coord = int(25 * scale)
		self.text_height = int(200 * scale)
		
		#create main frame
		self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
		self.frame.pack_propagate(0)
		self.frame.pack()
		
		#create board to hold references to snake-pieces
		self.food_board = [] # for storing references to create_image
		self.snake_board = []
		self.wall_board = []
		self.food_ghost_board = []
		self.snake_ghost_board = []
		self.wall_ghost_board = []
		self.img_refs = [] # for storing references to images - order: food, snake, wall, food_t, snake_t, wall_t
		
		#create and fill the canvas --> paintable area
		self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bg="black", bd=0, highlightthickness=0)
		self.c.pack()
		self.last_x = -1 # used to generate mouseOver/Exit events
		self.last_y = -1 # used to generate mouseOver/Exit events
		self.fill_canvas()
		
		#create the textholder
		self.scrollbar = _tk.Scrollbar(self.frame)
		self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
		self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
		self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(state=_tk.DISABLED)
		
		self.interval = 0
		self.alarm_speed = 0
		self.timer = self.milliseconds()
		
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def callback(self, event=None):
		self.root.destroy()
		_os._exit(0)
	
	def milliseconds(self):
		return _time.time() * 1000
	
	def place(self, x, y, color):
		element = _SnakeHolder(x, y, color)
		self.to_show_queue.put(element)
	
	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.place(x, y, self.EMPTY)
	
	def show(self):
		try:
			while True:
				element = self.to_show_queue.get_nowait()
				position = []
				position.append(self.food_board[element.x][element.y])
				position.append(self.snake_board[element.x][element.y])
				position.append(self.wall_board[element.x][element.y])
				position.append(self.food_ghost_board[element.x][element.y])
				position.append(self.snake_ghost_board[element.x][element.y])
				position.append(self.wall_ghost_board[element.x][element.y])
				for i in range(len(position)):
					# add 1 to i, because 0 is empty [same as doing color - 1]
					# thus, if 0, then it doesn't match with 1 to 6
					# therefore putting the whole position to hidden
					if element.color == i+1:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.NORMAL)
					else:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.HIDDEN)
		except _Queue.Empty:
			pass
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def get_event(self):
		global _ui_factory
		_ui_factory.mainroot.update()
		while True:
			try:
				self.refresh_event()
				event = self.event_queue.get_nowait()
				return event
			except _Queue.Empty:
				wait_time = min(self.interval, 10)
				self.wait(wait_time)
				_ui_factory.mainroot.update()
	
	def set_animation_speed(self, fps):
		current_time = self.milliseconds()
		if fps <= 0:
			self.interval = 0
			self.timer = current_time
			return
		if fps > 1000:
			fps = 1000
		self.interval = int(1000.0 / fps)
		self.refresh_event()
	
	def print_(self, text):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.insert(_tk.END, text)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def clear_text(self):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.delete(1.0, _tk.END)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def wait(self, ms):
		try:
		  _time.sleep(ms * 0.001)
		except:
		  self.close()
	
	def close(self):
		self.root.destroy()
		_os._exit(0)
	
	def random(self, maximum=1):
		return int(_random.random() * maximum)
	
	def create_piece(self, x0, y0, img, mix):
		result = []
		if img == self.FOOD:
			r = 255 / (1 + mix)
			g = 64 / (1 + mix)
			b = 64 / (1 + mix)
			scale = 0.8
			x1 = x0 + (1.0 - scale) / 2.0 * self.size_per_coord
			y1 = y0 + (1.0 - scale) * self.size_per_coord
			x2 = x0 + (1.0 - (1.0 - scale) / 2.0) * self.size_per_coord
			y2 = y0 + self.size_per_coord
			result.append(self.c.create_oval(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=0))
			r = 64 / (1 + mix)
			g = 255 / (1 + mix)
			b = 64 / (1 + mix)
			scale = 0.4
			x1 = x0 + self.size_per_coord / 2.0
			y1 = y0
			x2 = x1
			y2 = y0 + scale * self.size_per_coord
			result.append(self.c.create_line(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=2))
		if img == self.SNAKE:
			r = 32 / (1 + mix)
			g = 255 / (1 + mix)
			b = 0 / (1 + mix)
			x1 = x0
			y1 = y0
			x2 = x0 + self.size_per_coord
			y2 = y0 + self.size_per_coord
			result.append(self.c.create_oval(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=0))
		if img == self.WALL:
			r = 200 / (1 + mix)
			g = 100 / (1 + mix)
			b = 0 / (1 + mix)
			x1 = x0
			y1 = y0
			x2 = x0 + self.size_per_coord
			y2 = y0 + self.size_per_coord
			result.append(self.c.create_rectangle(x1, y1, x2, y2, state=_tk.HIDDEN, fill="#%02X%02X%02X" % (r, g, b), width=0))
		
		return result
	
	def create_snake_pieces(self):
		mixer = 0, 0, 0, 1, 1, 1
		imgtype = self.FOOD, self.SNAKE, self.WALL, self.FOOD, self.SNAKE, self.WALL
		boards = self.food_board, self.snake_board, self.wall_board, self.food_ghost_board, self.snake_ghost_board, self.wall_ghost_board
		for n in range(len(boards)):
			for i in range(self.width):
				boards[n].append([])
				for j in range(self.height):
					x0 = self.size_per_coord * i
					y0 = self.size_per_coord * j
					img = self.create_piece(x0, y0, imgtype[n], mixer[n])
					boards[n][i].append(img)
	
	def fill_canvas(self):
		self.bind_events()
		self.create_snake_pieces()
	
	def motion_event(self, event):
		if not self.mouse_on_screen:
			return
		x_old = self.last_x
		y_old = self.last_y
		x_new = event.x / self.size_per_coord
		y_new = event.y / self.size_per_coord
		x_change = int(x_old) != int(x_new)
		y_change = int(y_old) != int(y_new)
		if x_change or y_change:
			self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
			self.generate_event("mouseover", "%d %d"%(x_new,y_new))
			self.last_x = x_new
			self.last_y = y_new
	
	def enter_window_event(self, event):
		x_new = event.x / self.size_per_coord
		y_new = event.y / self.size_per_coord
		self.generate_event("mouseover", "%d %d"%(x_new,y_new))
		self.last_x = x_new
		self.last_y = y_new
		self.mouse_on_screen = True
	
	def leave_window_event(self, event):
		self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
		self.mouse_on_screen = False
	
	def alt_number_event(self, event):
		if event.char == event.keysym:
			if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
				self.generate_event("alt_number", event.char)
	
	def key_event(self, event):
		if event.char == event.keysym:
			if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
				self.generate_event("number", event.char)
			elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
				self.generate_event("letter", event.char)
			elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
				self.generate_event("letter", event.char)
			else:
				self.generate_event("other", event.char)
		elif event.keysym == 'Up':
			self.generate_event("arrow", "u")
		elif event.keysym == 'Down':
			self.generate_event("arrow", "d")
		elif event.keysym == 'Left':
			self.generate_event("arrow", "l")
		elif event.keysym == 'Right':
			self.generate_event("arrow", "r")
		elif event.keysym == 'Multi_Key':
			return
		elif event.keysym == 'Caps_Lock':
			self.generate_event("other", "caps lock")
		elif event.keysym == 'Num_Lock':
			self.generate_event("other", "num lock")
		elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
			self.generate_event("other", "shift")
		elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
			self.generate_event("other", "control")
		elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
			self.generate_event("other", "alt")
		else:
			self.generate_event("other", event.keysym)
	
	def click_event(self, event):
		x = event.x / self.size_per_coord
		y = event.y / self.size_per_coord
		self.generate_event("click", "%d %d"%(x,y))
	
	def refresh_event(self):
		current_time = self.milliseconds()
		threshold = current_time - self.timer - self.interval
		if threshold >= 0 and self.interval > 0:
			self.generate_event("alarm", "refresh")
			self.timer = current_time
	
	def generate_event(self, name, data):
		event = Event(name, data)
		self.event_queue.put(event)
	
	def bind_events(self):
		self.c.focus_set() # to redirect keyboard input to this widget
		self.c.bind("<Motion>", self.motion_event)
		self.c.bind("<Enter>", self.enter_window_event)
		self.c.bind("<Leave>", self.leave_window_event)
		self.c.bind("<Alt-Key>", self.alt_number_event)
		self.c.bind("<Key>", self.key_event)
		self.c.bind("<Button-1>", self.click_event)

class LifeUserInterface(object):
	def __init__(self, width, height, scale=1.0):
		"""This class starts the LifeUserInterface.
		Constants:
		- DEAD
		- ALIVE
		
		Parameters for the class:
		- width: at least 1
		- height: at least 1
		
		Optional parameters:
		- scale: 0.25 to 1.0
		"""
		
		_verify_int(width, "Width", 1)
		_verify_int(height, "Height", 1)
		_verify_float(scale, 'Scale', 0.25, 1.0)
		global _ui_factory
		self.life_interface = _Life(width, height, _ui_factory.mainroot, scale)
		self.DEAD = _Life.DEAD
		self.ALIVE = _Life.ALIVE
	
	def place(self, x, y, color):
		"""Place a Life piece (defined by 'color') on the given X and Y coordinates.
		"""
		
		_verify_int(x, 'X', 0, self.life_interface.width - 1)
		_verify_int(y, 'Y', 0, self.life_interface.height - 1)
		# 0 = empty, 1 = dead, 2 = alive
		_verify_int(color, 'Color', 0, 2)
		self.life_interface.place(x, y, color)
	
	def clear(self):
		"""Clears the display.
		Note: this does not clear the text area!
		"""
		
		self.life_interface.clear()
	
	def show(self):
		"""Show the changes made to the display (i.e. after calling place or clear)
		"""
		
		self.life_interface.show()
	
	def get_event(self):
		"""Returns an event generated from the display.
		The returned object has 2 properties:
		- name: holds the group which the event belongs to.
		- data: holds useful information for the user.
		"""
		
		return self.life_interface.get_event()
	
	def set_animation_speed(self, fps):
		"""Set an event to repeat 'fps' times per second.
		If the value is set to 0 or less, the repeating will halt.
		In theory the maximum value is 1000, but this depends on activity of the system.
		
		The generated events (available by using get_event) have these properties:
		- name: 'alarm'.
		- data: 'refresh'.
		"""
		
		_verify_float(fps, "Animation speed")
		self.life_interface.set_animation_speed(fps)
	
	def print_(self, text):
		"""Print text to the text area on the display.
		This function does not add a trailing newline by itself.
		"""
		
		_verify_str(text, "Text")
		self.life_interface.print_(text)
	
	def clear_text(self):
		"""Clears the text area on the display.
		"""
		
		self.life_interface.clear_text()
	
	def wait(self, ms):
		"""Let your program wait for an amount of milliseconds.
		
		This function only guarantees that it will wait at least this amount of time.
		If the system, i.e., is too busy, then this time might increase.
		- Python time module.
		"""
		
		_verify_int(ms, "Waiting time", 0)
		self.life_interface.wait(ms)
	
	def random(self, maximum):
		"""Picks a random integer ranging from 0 <= x < maximum
		Minimum for maximum is 1
		"""
		
		_verify_int(maximum, 'Random', 1)
		return self.life_interface.random(maximum)
	
	def close(self):
		"""Closes the display and stops your program.
		"""
		
		self.life_interface.close()
		
	def stay_open(self):
		"""Force the window to remain open.
		Only has effect on Mac OS to prevent the window from closing after the execution finishes.
		
		Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
		"""
		
		global _ui_factory
		_ui_factory.mainroot.mainloop()

class _Life(object):
	#one cannot prevent users from editing 'constants', as constants simply do not exist in Python
	DEAD = 0
	ALIVE = 1
	
	BACKGROUND = "#000000"
	
	def __init__(self, width, height, mainroot, scale=1.0):
		#create queue to store changes to placings
		self.to_show_queue = _Queue.Queue(maxsize=0)
		self.event_queue = _Queue.Queue(maxsize=0)
		
		#copy params
		self.width = width
		self.height = height
		self.scale = scale
		
		#start the main window
		self.root = _tk.Toplevel(mainroot)
		self.root.title("SnakeUserInterface")
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.bind("<Escape>", self.callback)
		self.root.resizable(False, False)
		
		#calculate sizes
		self.size_per_coord = int(25 * scale)
		self.text_height = int(200 * scale)
		
		#create main frame
		self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
		self.frame.pack_propagate(0)
		self.frame.pack()
		
		#create board to hold references to snake-pieces
		self.dead_board = [] # for storing references to create_image
		self.alive_board = []
		self.img_refs = [] # for storing references to images - order: dead, alive
		
		#create and fill the canvas --> paintable area
		self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bg=self.BACKGROUND, bd=0, highlightthickness=0)
		self.c.pack()
		self.last_x = -1 # used to generate mouseOver/Exit events
		self.last_y = -1 # used to generate mouseOver/Exit events
		self.fill_canvas()
		
		#create the textholder
		self.scrollbar = _tk.Scrollbar(self.frame)
		self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
		self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
		self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(state=_tk.DISABLED)
		
		self.interval = 0
		self.alarm_speed = 0
		self.timer = self.milliseconds()
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def callback(self, event=None):
		self.root.destroy()
		_os._exit(0)
	
	def milliseconds(self):
		return _time.time() * 1000
	
	def place(self, x, y, color):
		element = _LifeHolder(x, y, color)
		self.to_show_queue.put(element)
	
	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.place(x, y, self.DEAD)
	
	def show(self):
		try:
			while True:
				element = self.to_show_queue.get_nowait()
				position = []
				position.append(self.dead_board[element.x][element.y])
				position.append(self.alive_board[element.x][element.y])
				for i in range(len(position)):
					if element.color == i:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.NORMAL)
					else:
						for e in position[i]:
							self.c.itemconfig(e, state=_tk.HIDDEN)
		except _Queue.Empty:
			pass
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def get_event(self):
		global _ui_factory
		_ui_factory.mainroot.update()
		while True:
			try:
				self.refresh_event()
				event = self.event_queue.get_nowait()
				return event
			except _Queue.Empty:
				wait_time = min(self.interval, 10)
				self.wait(wait_time)
				_ui_factory.mainroot.update()
	
	def set_animation_speed(self, fps):
		current_time = self.milliseconds()
		if fps <= 0:
			self.interval = 0
			self.timer = current_time
			return
		if fps > 1000:
			fps = 1000
		self.interval = int(1000.0 / fps)
		self.refresh_event()
	
	def print_(self, text):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.insert(_tk.END, text)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def clear_text(self):
		self.textarea.config(state=_tk.NORMAL)
		self.textarea.delete(1.0, _tk.END)
		self.textarea.see(_tk.END)
		self.textarea.config(state=_tk.DISABLED)
		global _ui_factory
		_ui_factory.mainroot.update()
	
	def wait(self, ms):
		try:
		  _time.sleep(ms * 0.001)
		except:
		  self.close()
	
	def close(self):
		self.root.destroy()
		_os._exit(0)
	
	def random(self, maximum=1):
		return int(_random.random() * maximum)
	
	def create_piece(self, x0, y0, img, state_):
		result = []
		if img == self.DEAD:
			r = 255
			g = 255
			b = 255
			x1 = x0
			y1 = y0
			# -1 from the second coordinate because the bottom and right borders are 1 pixel outside the boundary
			x2 = x0 + self.size_per_coord - 1
			y2 = y0 + self.size_per_coord - 1
			result.append(self.c.create_rectangle(x1, y1, x2, y2, state=state_, fill="#%02X%02X%02X" % (r, g, b), width=1))
		if img == self.ALIVE:
			r = 0
			g = 0
			b = 255
			x1 = x0
			y1 = y0
			# -1 from the second coordinate because the bottom and right borders are 1 pixel outside the boundary
			x2 = x0 + self.size_per_coord - 1
			y2 = y0 + self.size_per_coord - 1
			result.append(self.c.create_rectangle(x1, y1, x2, y2, state=state_, fill="#%02X%02X%02X" % (r, g, b), width=1))
		
		return result
	
	def create_life_pieces(self):
		imgtype = self.DEAD, self.ALIVE
		boards = self.dead_board, self.alive_board
		for n in range(len(boards)):
			for i in range(self.width):
				boards[n].append([])
				for j in range(self.height):
					x0 = self.size_per_coord * i
					y0 = self.size_per_coord * j
					state_ = _tk.HIDDEN
					if n == 0:
						state_ = _tk.NORMAL
					img = self.create_piece(x0, y0, imgtype[n], state_)
					boards[n][i].append(img)
	
	def fill_canvas(self):
		self.bind_events()
		self.create_life_pieces()
	
	def motion_event(self, event):
		if not self.mouse_on_screen:
			return
		x_old = self.last_x
		y_old = self.last_y
		x_new = event.x / self.size_per_coord
		y_new = event.y / self.size_per_coord
		x_change = int(x_old) != int(x_new)
		y_change = int(y_old) != int(y_new)
		if x_change or y_change:
			self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
			self.generate_event("mouseover", "%d %d"%(x_new,y_new))
			self.last_x = x_new
			self.last_y = y_new
	
	def enter_window_event(self, event):
		x_new = event.x / self.size_per_coord
		y_new = event.y / self.size_per_coord
		self.generate_event("mouseover", "%d %d"%(x_new,y_new))
		self.last_x = x_new
		self.last_y = y_new
		self.mouse_on_screen = True
	
	def leave_window_event(self, event):
		self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
		self.mouse_on_screen = False
	
	def alt_number_event(self, event):
		if event.char == event.keysym:
			if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
				self.generate_event("alt_number", event.char)
	
	def key_event(self, event):
		if event.char == event.keysym:
			if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
				self.generate_event("number", event.char)
			elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
				self.generate_event("letter", event.char)
			elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
				self.generate_event("letter", event.char)
			else:
				self.generate_event("other", event.char)
		elif event.keysym == 'Up':
			self.generate_event("arrow", "u")
		elif event.keysym == 'Down':
			self.generate_event("arrow", "d")
		elif event.keysym == 'Left':
			self.generate_event("arrow", "l")
		elif event.keysym == 'Right':
			self.generate_event("arrow", "r")
		elif event.keysym == 'Multi_Key':
			return
		elif event.keysym == 'Caps_Lock':
			self.generate_event("other", "caps lock")
		elif event.keysym == 'Num_Lock':
			self.generate_event("other", "num lock")
		elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
			self.generate_event("other", "shift")
		elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
			self.generate_event("other", "control")
		elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
			self.generate_event("other", "alt")
		else:
			self.generate_event("other", event.keysym)
	
	def click_event(self, event):
		x = event.x / self.size_per_coord
		y = event.y / self.size_per_coord
		self.generate_event("click", "%d %d"%(x,y))
	
	def refresh_event(self):
		current_time = self.milliseconds()
		threshold = current_time - self.timer - self.interval
		if threshold >= 0 and self.interval > 0:
			self.generate_event("alarm", "refresh")
			self.timer = current_time
	
	def generate_event(self, name, data):
		event = Event(name, data)
		self.event_queue.put(event)
	
	def bind_events(self):
		self.c.focus_set() # to redirect keyboard input to this widget
		self.c.bind("<Motion>", self.motion_event)
		self.c.bind("<Enter>", self.enter_window_event)
		self.c.bind("<Leave>", self.leave_window_event)
		self.c.bind("<Alt-Key>", self.alt_number_event)
		self.c.bind("<Key>", self.key_event)
		self.c.bind("<Button-1>", self.click_event)

class Event(object):
	def __init__(self, name, data):
		"""This class holds the name and data for each event in their respective variables.
		Variables:
		- name
		- data
		
		Example to access with SnakeUserInterface:
		
		ui = SnakeUserInterface(5,5) # 5 by 5 grid for testing purposes
		your_variable = ui.get_event() # code will block untill an event comes
		# your_variable now points to an event
		print your_variable.name, your_variable.data
		
		List of events:
		- name: mouseover
		  data: x and y coordinates (as integers), separated by a space
			  generated when mouse goes over a coordinate on the window
		- name: mouseexit
		  data: x and y coordinates (as integers), separated by a space
			  generated when mouse exits a coordinate on the window
		- name: click
		  data: x and y coordinates (as integers), separated by a space
			  generated when the user clicks on a coordinate on the window
		- name: alarm
		  data: refresh
			  generated as often per second as the user set the animation speed to; note that the data is exactly as it says: "refresh"
		- name: letter
		  data: the letter that got pressed
			  generated when the user presses on a letter (A to Z; can be lowercase or uppercase depending on shift/caps lock)
		- name: number
		  data: the number (as a string) that got pressed
			  generated when the user presses on a number (0 to 9)
		- name: alt_number
		  data: the number (as a string) that got pressed
			  generated when the user presses on a number (0 to 9) while at the same time pressing the Alt key
		- name: arrow
		  data: the arrow key that got pressed, given by a single letter
			  generated when the user presses on an arrow key, data is then one of: l, r, u, d
		- name: other
		  data: data depends on key pressed
			  generated when the user pressed a different key than those described above
			  possible data:
			  - caps_lock
			  - num_lock
			  - alt
			  - control
			  - shift
			  more data can exist and are recorded (read: they generate events), but not documented
		"""
		self.name = name
		self.data = data

_ui_factory = _Factory()

class StockMarketUserInterface(object):
    def __init__(self, enable_cache=False):
        """
        User interface for the stocks assigment.

        Variables:
            enable_cache: if set to True retrieved data will be cached.
        """
        if not have_mpl:
            raise _IPyException('Use of HouseMarketUserInterface has been disabled.')
        self._enable_cache = enable_cache
        pass

    def _yql_query(self, q, _format, env):
        req = {
                'q': q,
                'format' : _format,
                'env': env
                }

        data = urllib.urlencode(req)
        whole_url = YAHOO_URL + '?' + data
        request = urllib2.Request(whole_url) 
        handler = urllib2.urlopen(request)
        response = json.loads(handler.read())
        return response


    def _check_time_interval(self, start, end):
        st = _time.strptime(start, "%Y-%m-%d")
        en = _time.strptime(end, "%Y-%m-%d")
        ds = _datetime.datetime.fromtimestamp(_time.mktime(st))
        de = _datetime.datetime.fromtimestamp(_time.mktime(en))
        ddays = (de - ds).days

        if ddays > 365:
            raise Exception("The largest time interval the API can handle is 365 days.")

    def _load_cache(self, key):
        try:
            fp = open(".stock_cache", "rb")
            db = _pickle.load(fp)
            return  db.get(key, None)
        except Exception:
            return None


    def _store_cache(self, key, value):
        db = {}
        try:
            with open(".stock_cache", "rb") as fp:
                try:
                    db = _pickle.load(fp)
                except Exception:
                    pass
        except Exception:
            pass

        with open(".stock_cache", "wb+") as fp:
            db[key] = value
            _pickle.dump(db, fp)

    def _cache_hash(self, symbol, start, end):
        return symbol + start + end



    def get_stock_quotes(self, symbol, start, end):
        """
        Returns a list of dictionaries containing Yahoo historical stock quotes for variable 'symbol'.

        Variables:
        - symbol: (stock symbol e.g. AAPL, IBM, MSFT)
        - start: start date of historical interval. Format: yyyy-mm-dd
        - end: end date of historical interval. Format: yyyy-mm-dd

        The Yahoo API supports a max time interval of 365 day, thus an exception is raised if
        the interval between start and end > 365 days.

        """
        self._check_time_interval(start, end)

        if self._enable_cache:
            cached = self._load_cache(self._cache_hash(symbol, start, end))
            if cached:
                return cached['query']['results']['quote'] 

        response = self._yql_query(
                'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%s" and endDate = "%s"' % (symbol, start, end),
                'json',
                'store://datatables.org/alltableswithkeys'
                )
        
        results =  response['query']['results']

        if results is None:
            raise Exception("No data avalable for quote symbol %s." % (symbol))
        quotes =  results['quote']
        if self._enable_cache:
            self._store_cache(self._cache_hash(symbol,start,end), response)
        return quotes

    def plot(self, prices, color, **kwargs):
        """
        Plots the list of prices. With the color specified by the string 'color'.

        Possible colors: 'b', 'g', 'r'
        Use show() to display the plotted data.

        Variables:
            prices: list of floats with prices to be plotted.
            **kwargs: (optional) additional kwargs.
        """
        t = plt.arange(0, len(prices), 1)
        lines = plt.plot(t, prices, c=color)
        kwargs['linewidth'] = 2.0
        plt.setp(lines, **kwargs)
        return lines

    def show(self):
        """
        Draw the current state of the ui.
        """
        plt.ylabel('Returns')
        plt.xlabel('Day')
        plt.show()


    
class HouseMarketUserInterface(object):
    def __init__(self):
        if not have_mpl:
            raise _IPyException('Use of HouseMarketUserInterface has been disabled.')
        self.max_x = 0 # Keep track of max observer x-value

    def plot_dot(self, x, y, color, **kwargs):
        """
        Plot the point (x,y) in the ui. With the color specified by the string 'color'.
        Possible colors: 'b', 'g', 'r'

        Arguments:
            x: float
            y: float

        Advanced functionality: a list of floats may be supplied to both x and y to draw many points in one step.
        
        """
        if isinstance(x, list):
            self.max_x = max(max(x), self.max_x)
        else:
            self.max_x = max(x, self.max_x)
        plt.plot(x,y, 'o', c=color, **kwargs)

    def plot_line(self, *args, **kwargs):
        """
        Plot the polynomial represented by the coefficients provided.

        E.g. plot_line(2,1) would plot the function '2 + 1 * x'
             plot_line(3,4,5) plots '5*x^2 + 4*x + 3'
        """
        t = plt.arange(0.0, self.max_x, 0.01)
        func = lambda x: sum([args[i] * (x ** i) for i in range(len(args))])
        return plt.plot(t, func(t), **kwargs)


    def show(self):
        """
        Draw the current state of the ui.
        """
        plt.ylabel('House Price')
        plt.xlabel('House Size (m^2)')
        orig_limit_x = plt.xlim()
        orig_limit_y = plt.ylim()
        a = plt.xlim(orig_limit_x[0], self.max_x + 0.1*self.max_x)
        a = plt.ylim(orig_limit_y[0] - 0.1* orig_limit_y[0], orig_limit_y[1] )
        plt.show()
