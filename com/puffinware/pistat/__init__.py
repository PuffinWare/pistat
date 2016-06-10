from peewee import SqliteDatabase

# Put in the module file to avoid circular imports between db and models
DB = SqliteDatabase('pistat.db', pragmas=[('user_version', 1)])
