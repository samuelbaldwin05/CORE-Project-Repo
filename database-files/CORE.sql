DROP DATABASE IF EXISTS `CORE_Database`;

CREATE DATABASE IF NOT EXISTS `CORE_Database`;

USE `CORE_Database`;

-- Step 1: Independent Tables
CREATE TABLE Location (
    LocationId INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    State VARCHAR(2),
    City VARCHAR(25),
    CountryCode VARCHAR(5),
    Address VARCHAR(100)
);

CREATE TABLE College (
    CollegeID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    CollegeName VARCHAR(50)
);

CREATE TABLE Advisor (
    AdvisorId INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    College VARCHAR(50),
    FirstName VARCHAR(25),
    LastName VARCHAR(25)
);

-- Step 2: Tables with Foreign Keys to Independent Tables
CREATE TABLE Company (
    CompanyID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    Name VARCHAR(25),
    Industry VARCHAR(20),
    CompanySize INT,
    LocationId INTEGER NOT NULL,
    CONSTRAINT CL1 FOREIGN KEY (LocationId)
        REFERENCES Location(LocationId)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE Majors (
    MajorID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    MajorName VARCHAR(50),
    Combined BOOL,
    CollegeID INT NOT NULL,
    CONSTRAINT PPS_Major FOREIGN KEY (CollegeID)
        REFERENCES College(CollegeID)
        ON UPDATE cascade ON DELETE restrict
);

-- Step 3: Tables with Foreign Keys to Tables in Step 2
CREATE TABLE Users (
    NUID INTEGER NOT NULL PRIMARY KEY UNIQUE,
    PositionId INT,
    Username VARCHAR(100) UNIQUE,
    MajorID INT,
    GPA FLOAT,
    AdvisorId INT,
    AppCount INT,
    OfferCount INT,
    PreviousCount INT,
    CONSTRAINT UA FOREIGN KEY (AdvisorId)
        REFERENCES Advisor(AdvisorId)
        ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT UM FOREIGN KEY (MajorID)
        REFERENCES Majors(MajorID)
        ON UPDATE cascade ON DELETE restrict
);

-- Step 4: Tables with Foreign Keys to Tables in Step 3
CREATE TABLE JobPosting (
    PostingID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    CompanyID INTEGER,
    DatePosted DATETIME,
    Status BOOL,
    CONSTRAINT JPC FOREIGN KEY (CompanyID)
        REFERENCES Company(CompanyID)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE PositionTable (
    PositionID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    PositionName VARCHAR(40),
    Description VARCHAR(300),
    Skills VARCHAR(300),
    Environment VARCHAR(20),
    AdditionalQuestions BOOL,
    CoverLetter BOOL,
    PostingID INT NOT NULL,
    CONSTRAINT PJP FOREIGN KEY (PostingID)
        REFERENCES JobPosting(PostingID)
        ON UPDATE cascade ON DELETE cascade
);

-- Step 5: Tables with Foreign Keys to Tables in Step 4
CREATE TABLE PositionReview (
    PosReviewID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    Description VARCHAR(255),
    Offer BOOL,
    ApplicationRating TINYINT(5),
    EnvironmentRating TINYINT(5),
    EducationRating TINYINT(5),
    ProfessionalRating TINYINT(5),
    Applied BOOL,
    AppliedDate DATETIME,
    ResponseDate DATETIME,
    PositionID INTEGER NOT NULL,
    CONSTRAINT fk_1 FOREIGN KEY (PositionID)
        REFERENCES PositionTable(PositionID)
        ON UPDATE CASCADE ON DELETE cascade
);


CREATE TABLE PositionReviewers (
    NUID INTEGER,
    PosReviewID INTEGER,
    PRIMARY KEY (NUID, PosReviewID),
    CONSTRAINT PRU FOREIGN KEY (NUID)
        REFERENCES Users(NUID)
        ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT PRPR FOREIGN KEY (PosReviewID)
        REFERENCES PositionReview(PosReviewID)
        ON UPDATE cascade ON DELETE cascade
);


CREATE TABLE CompanyReview (
    ComReviewID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    CompanyId INT NOT NULL,
    Type VARCHAR(50),
    Description VARCHAR(255),
    EnvironmentRating TINYINT(1),
    CultureRating TINYINT(1),
    CONSTRAINT CRC FOREIGN KEY (CompanyId)
        REFERENCES Company(CompanyID)
        ON UPDATE cascade ON DELETE RESTRICT
);

CREATE TABLE CompanyReviewers (
    NUID INTEGER,
    ComReviewID INTEGER,
    PRIMARY KEY (NUID, ComReviewID),
    CONSTRAINT CRU FOREIGN KEY (NUID)
        REFERENCES Users(NUID)
        ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT CRCR FOREIGN KEY (ComReviewID)
        REFERENCES CompanyReview(ComReviewID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE PosStats (
    PositionID INTEGER,
    PosStatID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    YieldRate FLOAT,
    AvgAppAmount INT,
    AvgInterview INT,
    AvgGpa INT,
    AvgLearning INT,
    AvgEnvironment INT,
    AvgInterviewTime Time,
    CONSTRAINT PSPR FOREIGN KEY (PositionID)
        REFERENCES PositionTable(PositionID)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE PostStats (
    PostingID INTEGER,
    PostStatID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    AppAmount FLOAT,
    InterviewAmount INT,
    OfferAmnt INT,
    AcceptAmnt INT,
    CallBackNum INT,
    MeanResponseTime Time,
    CONSTRAINT POS FOREIGN KEY (PostingID)
        REFERENCES JobPosting(PostingID)
        ON UPDATE cascade ON DELETE restrict
);

