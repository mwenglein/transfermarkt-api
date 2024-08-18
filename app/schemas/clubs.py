from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.base import TransfermarktBaseModel, IDMixin, AuditMixin


class ClubPlayer(TransfermarktBaseModel):
    name: str
    position: str
    dob: date = Field(alias="dateOfBirth")
    age: int
    nationality: list[str]
    current_club: Optional[str] = Field(alias="currentClub", default=None)
    height: Optional[int] = None
    foot: Optional[str] = None
    joined_on: Optional[date] = Field(alias="joinedOn", default=None)
    joined: Optional[str] = None
    signed_from: Optional[str] = Field(alias="signedFrom", default=None)
    contract: Optional[date] = Field(alias="contract", default=None)
    market_value: Optional[int] = Field(alias="marketValue", default=None)
    status: Optional[str] = None


class ClubPlayers(TransfermarktBaseModel):
    players: list[ClubPlayer]


class ClubSquad(BaseModel):
    size: int
    average_age: float = Field(alias="averageAge")
    foreigners: int
    national_team_players: int = Field(alias="nationalTeamPlayers")


class ClubLeague(BaseModel):
    id: str
    name: str
    country_id: str = Field(alias="countryID")
    country_name: str = Field(alias="countryName")
    tier: str


class ClubProfile(TransfermarktBaseModel):
    url: str
    name: str
    official_name: str = Field(alias="officialName")
    image: str
    legal_form: Optional[str] = Field(alias="legalForm", default=None)
    address_line_1: str = Field(alias="addressLine1")
    address_line_2: str = Field(alias="addressLine2")
    address_line_3: str = Field(alias="addressLine3")
    tel: str
    fax: str
    website: str
    founded_on: date = Field(alias="foundedOn")
    members: Optional[int] = None
    members_date: Optional[date] = Field(alias="membersDate", default=None)
    other_sports: Optional[list[str]] = Field(alias="otherSports", default=None)
    colors: Optional[list[str]] = None
    stadium_name: str = Field(alias="stadiumName")
    stadium_seats: int = Field(alias="stadiumSeats")
    current_transfer_record: int = Field(alias="currentTransferRecord")
    current_market_value: int = Field(alias="currentMarketValue")
    confederation: Optional[str] = None
    fifa_world_ranking: Optional[str] = Field(alias="fifaWorldRanking", default=None)
    squad: ClubSquad
    league: ClubLeague
    historical_crests: Optional[list[str]] = Field(alias="historicalCrests", default=None)

    @field_validator("members", mode="before")
    def members_format(cls, value: str):
        return int(value.replace(".", ""))

    @field_validator("current_transfer_record", mode="before", check_fields=False)
    def current_transfer_record_format(cls, value: str):
        return int(value.replace("m", "000000").replace("k", "000").replace("€", "").replace(".", "").replace("+", ""))


class ClubSearchResult(TransfermarktBaseModel, IDMixin):
    url: str
    name: str
    country: str
    squad: int
    market_value: Optional[int] = Field(alias="marketValue", default=None)


class ClubSearch(TransfermarktBaseModel, AuditMixin):
    query: str
    page_number: int = Field(alias="pageNumber")
    results: list[ClubSearchResult]
