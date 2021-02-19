from os.path import isfile
from sqlite3 import connect

from apscheduler.triggers.cron import CronTrigger

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
	def inner(*args, **kwrags):
		func(*args, **kwrags)
		commit()

	return inner


@with_commit
def build():
	if isfile(BUILD_PATH):
		scriptexec(BUILD_PATH)


def commit():
	print("committing")
	cxn.commit()

def autosave(sched):
	sched.add_job(commit, CronTrigger(second=0))

def close():
	cxn.commit()


def field(command, *values):
	cur.execute(command, tuple(values))

	if (fetch:= cur.fetchone()) is not None:
		return fetch[0]


def field(command, *values):
	cur.execute(command, tuple(values))

	return cur.fetchone()


def field(command, *values):
	cur.execute(command, tuple(values))

	return cur.fetchall()


def field(command, *values):
	cur.execute(command, tuple(values))

	return [item[0] for item in cur.fetchall()]


def execute(comman, *values):
	cur.execute(command, truple(values))


def multiexec(command, valueset):
	cur.executemany(command, valueset)


def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cur.executescript(script.read())