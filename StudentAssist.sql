BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users" (
	"userID"	INTEGER,
	"firstName"	TEXT,
	"lastName"	TEXT,
	"emailAddress"	TEXT,
	"phoneNumber"	TEXT,
	"passwordHash"	TEXT,
	"emailNotifs"	TEXT,
	"phoneNotifs"	TEXT,
	PRIMARY KEY("userID")
);
CREATE TABLE IF NOT EXISTS "Classes" (
	"userID"	INTEGER,
	"className"	TEXT,
	"classDates"	TEXT,
	"startTime"	TEXT,
	"endTime"	TEXT,
	FOREIGN KEY("userID") REFERENCES "Users"("userID"),
	PRIMARY KEY("userID","className")
);
CREATE TABLE IF NOT EXISTS "Tasks" (
	"userID"	INTEGER,
	"taskName"	TEXT,
	"taskStartDate"	TEXT,
	"taskDueDate"	TEXT,
	"taskProgress"	TEXT,
	"taskClass"	TEXT,
	FOREIGN KEY("userID") REFERENCES "Users"("userID"),
	PRIMARY KEY("userID","taskName")
);
COMMIT;
