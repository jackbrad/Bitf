# Bitf

BitFoon is a Coin trading game that is designed to show Google Spanner's functionality in a Gaming or Financials scenario. 

Game Sessions are created by the Host Player which provides a key to the rest of the players. 



Specifically: 
- Global Multiregion RDBMS with Acid transactions
- Auto-Scaling/Sharding
- Low Latency Query and Update times. 
- 99.999% High Availability

The project is broken into a few architectural components. 
- Spanner DB
- Cloud Functions Processing of Trading activity
- Pub/Sub queue of Trading objects
- CloudRun Deployment for UI 
- Automated Random Auto Trading Bot (Computer Player) 



Notes: 
Create project. 

Enable APIs for : 
- Cloud Build
- Cloud Run 
- Container Registry
- Resource Manager APIs
- Spanner 
- Cloud Functions


Create Spanner Instance
Create Spanner Database

Create Tables:

CREATE TABLE GameSession (
  SessionUUID STRING(36) NOT NULL,
  StartTime TIMESTAMP NOT NULL,
  EndTime TIMESTAMP NOT NULL,
  SessionKey STRING(36) NOT NULL
) PRIMARY KEY (SessionUUID);

CREATE TABLE Player (
  PlayerUUID STRING(36) NOT NULL,
  Name STRING(255) NOT NULL,
  PictureURL STRING(255),
  Location STRING(255),
  Preferences JSON
)PRIMARY KEY (PlayerUUID);

CREATE TABLE Coin (
  CoinUUID STRING(36) NOT NULL,
  Name STRING(255) NOT NULL,
  IconURL STRING(255),
)PRIMARY KEY (CoinUUID);

CREATE TABLE TradeOrder (
  SessionUUID STRING(36) NOT NULL,
  OrderUUID STRING(36)  NOT NULL,
  CoinUUID STRING(36)  NOT NULL,
  PlayerUUID STRING(36) NOT NULL,
  Placed TIMESTAMP NOT NULL,
  Ask BOOL NOT NULL,
  Price FLOAT64 NOT NULL,
  UnitSize FLOAT64 NOT NULL,
  Cancelled BOOL NOT NULL,
  Filled BOOL NOT NULL
)PRIMARY KEY (OrderUUID);

CREATE TABLE Trade (
  SessionUUID STRING(36) NOT NULL,
  TradeUUID STRING(36) NOT NULL,
  AskOrderUUID STRING(36) NOT NULL,
  BidOrderUUID STRING(36) NOT NULL,
  CoinUUID STRING(36) NOT NULL,
  Booked TIMESTAMP NOT NULL,
  Size FLOAT64 NOT NULL,
  Price FLOAT64 NOT NULL
)PRIMARY KEY (TradeUUID);
